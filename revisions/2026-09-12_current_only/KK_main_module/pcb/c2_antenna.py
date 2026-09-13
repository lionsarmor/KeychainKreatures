"""Compatibility entry point for the C.2 antenna-aware DSN generator.
The fresh-board SES importer installs the identical native KiCad rule area.
No routed board is deleted or edited by this wrapper.
"""
from pathlib import Path
import subprocess
subprocess.run(['node',str(Path(__file__).with_name('c2_antenna_dsn.mjs'))],check=True)
