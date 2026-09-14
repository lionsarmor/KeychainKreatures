# Upload SMT centroid; attach mixed operations

1. Upload **UPLOAD_SMT_CENTROID_MM.csv**: 104 positions classified SMT by the issued BOM.
2. Attach **ATTACH_THT_MIXED_OPERATIONS_MM.csv**: four connector positions J1–J4, all still fitted.
3. Provide **REFERENCE_ALL_108_NATIVE_POSITIONS.csv** if the assembler wants the complete native export.

J1 USB-C is mixed construction, including SMT contacts; coordinate its pick/place and secondary handling explicitly. It has not been deleted from the assembly request. SW1 is classified SMT in the issued BOM and remains in the 104-row centroid.

No coordinates or rotations were recalculated: these filtered exports preserve native KiCad **millimeters, Y-up (negative Y here), original origin and rotation**. Side is top. The original native export is retained byte-for-byte. REFERENCE_CAD_Y_DOWN_BOM_AND_PLACEMENT.csv is a human reference with the opposite Y convention; **do not substitute it for the upload centroid without conversion**.

PCBWay must validate part orientation, origin and polarity before machine programming. These are reviewed-input files, not claimed machine-calibrated placement programs. See CENTROID_VERIFICATION.json for the exact 104 + 4 = 108 reference-set check.
