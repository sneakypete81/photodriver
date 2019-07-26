#!/usr/bin/env python

from pathlib import Path
import shutil

import piexif

import photo_list

THIS_DIR = Path(__file__).parent

for (date, filename) in zip(photo_list.DATETIMES, photo_list.FILENAMES):
    dest_file = THIS_DIR / filename
    shutil.copyfile(THIS_DIR / "test.jpg", dest_file)
    exif = piexif.dump(
        {"0th": {piexif.ImageIFD.DateTime: date.strftime("%Y:%m:%d %H:%M:%S")}}
    )
    piexif.insert(exif, str(dest_file))
