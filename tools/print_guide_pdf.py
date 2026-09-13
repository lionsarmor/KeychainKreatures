"""Print local generated HTML with page numbers and unsplit measurement rows.

Private LibreOffice profile and named pipe; does not connect to the user's session.
"""
from pathlib import Path
import os, signal, subprocess, sys, tempfile, time, uuid
import uno

source=Path(sys.argv[1]).resolve();output=Path(sys.argv[2]).resolve();title=sys.argv[3]
assert source.is_file() and source.suffix=='.html'
def prop(name,value):
    p=uno.createUnoStruct('com.sun.star.beans.PropertyValue');p.Name=name;p.Value=value;return p
with tempfile.TemporaryDirectory(prefix='kk-guide-layout-') as tmp:
    pipe='kk_guide_'+uuid.uuid4().hex
    command=['libreoffice','-env:UserInstallation='+(Path(tmp)/'profile').as_uri(),
             '--headless','--nologo','--nodefault','--norestore',
             '--accept=pipe,name='+pipe+';urp;StarOffice.ComponentContext']
    proc=subprocess.Popen(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
    desktop=None;doc=None
    try:
        local=uno.getComponentContext()
        resolver=local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',local)
        deadline=time.monotonic()+15
        while True:
            try:ctx=resolver.resolve('uno:pipe,name='+pipe+';urp;StarOffice.ComponentContext');break
            except Exception:
                if time.monotonic()>deadline:raise
                time.sleep(.1)
        desktop=ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop',ctx)
        doc=desktop.loadComponentFromURL(source.as_uri(),'_blank',0,(prop('Hidden',True),prop('MacroExecutionMode',0),prop('UpdateDocMode',0)))
        assert doc is not None
        tables=doc.getTextTables();row_count=0
        for name in tables.getElementNames():
            table=tables.getByName(name)
            table.RepeatHeadline=True;table.HeaderRowCount=1
            for i in range(table.Rows.Count):
                row=table.Rows.getByIndex(i)
                assert row.PropertySetInfo.hasPropertyByName('IsSplitAllowed')
                row.IsSplitAllowed=False;row_count+=1
        page_styles=doc.StyleFamilies.getByName('PageStyles')
        for name in page_styles.getElementNames():
            style=page_styles.getByName(name)
            style.FooterIsOn=True
            footer=style.FooterText
            footer.setString(title+' | Page ')
            cursor=footer.createTextCursor();cursor.gotoEnd(False)
            number=doc.createInstance('com.sun.star.text.TextField.PageNumber')
            number.SubType=uno.Enum('com.sun.star.text.PageNumberType','CURRENT')
            number.NumberingType=uno.getConstantByName('com.sun.star.style.NumberingType.ARABIC')
            footer.insertTextContent(cursor,number,False)
            cursor.gotoEnd(False);footer.insertString(cursor,' | Guide v1',False)
            cursor.gotoStart(False);cursor.gotoEnd(True);cursor.CharHeight=8;cursor.CharFontName='Arial'
        temp_output=Path(tmp)/output.name
        doc.storeToURL(temp_output.as_uri(),(prop('FilterName','writer_pdf_Export'),prop('Overwrite',True)))
        assert temp_output.stat().st_size>10000
        output.parent.mkdir(parents=True,exist_ok=True)
        import shutil
        shutil.copy2(temp_output,output)
        print(f'Printed {output.name}; {row_count} table rows protected from splitting',flush=True)
    finally:
        if doc is not None:doc.close(True)
        if desktop is not None:desktop.terminate()
        try:proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            proc.wait(timeout=8)
