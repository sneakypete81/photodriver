#!/usr/bin/env python

from datetime import datetime
from pathlib import Path
import shutil

import piexif

DATES = [
    datetime(2018, 1, 1, 9, 0, 0),
    datetime(2018, 1, 1, 10, 0, 0),
    datetime(2018, 1, 2, 9, 0, 0),
    datetime(2018, 1, 31, 9, 0, 0),
    datetime(2018, 1, 31, 10, 0, 0),
    datetime(2018, 2, 1, 9, 0, 0),
    datetime(2018, 4, 2, 9, 0, 0),
    datetime(2018, 5, 31, 9, 0, 0),
    datetime(2018, 2, 2, 9, 0, 0),
    datetime(2018, 2, 3, 9, 0, 0),
    datetime(2018, 2, 3, 10, 0, 0),
    datetime(2018, 2, 3, 11, 0, 0),
    datetime(2018, 2, 3, 12, 0, 0),
    datetime(2018, 2, 4, 9, 0, 0),
    datetime(2018, 3, 4, 9, 0, 0),
    datetime(2018, 3, 5, 9, 0, 0),
    datetime(2018, 3, 6, 9, 0, 0),
    datetime(2018, 3, 7, 9, 0, 0),
    datetime(2018, 3, 7, 10, 0, 0),
    datetime(2018, 3, 8, 9, 0, 0),
    datetime(2018, 3, 8, 10, 0, 0),
    datetime(2018, 3, 8, 11, 0, 0),
    datetime(2018, 3, 9, 9, 0, 0),
    datetime(2018, 3, 10, 9, 0, 0),
    datetime(2018, 3, 11, 9, 0, 0),
    datetime(2018, 3, 11, 10, 0, 0),
    datetime(2018, 3, 11, 11, 0, 0),
    datetime(2018, 3, 11, 12, 0, 0),
    datetime(2018, 3, 11, 13, 0, 0),
    datetime(2018, 3, 11, 14, 0, 0),
    datetime(2018, 3, 12, 9, 0, 0),
    datetime(2018, 3, 13, 9, 0, 0),
    datetime(2018, 3, 14, 9, 0, 0),
    datetime(2018, 3, 15, 9, 0, 0),
    datetime(2018, 3, 16, 9, 0, 0),
    datetime(2018, 3, 17, 9, 0, 0),
    datetime(2018, 3, 18, 9, 0, 0),
]

THIS_DIR = Path(__file__).parent

for date in DATES:
    dest_file = THIS_DIR / date.strftime("test-%Y%m%d-%H%M%S.jpg")
    shutil.copyfile(THIS_DIR / "test.jpg", dest_file)
    exif = piexif.dump(
        {"0th": {piexif.ImageIFD.DateTime: date.strftime("%Y:%m:%d %H:%M:%S")}}
    )
    piexif.insert(exif, str(dest_file))
