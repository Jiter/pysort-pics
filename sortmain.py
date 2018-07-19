#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 22:43:56 2018

@author: david
pysort-pics
"""

import os
import shutil
import PIL

sourcedir = '/Users/david/Documents/Handy/'
outputdir = '/Users/david/Documents/Output/test'

copycounter = 0

def get_oldest_date(fname):
    src = sourcedir + "/" + fname

    img = PIL.Image.open(src)
    exif_data = img._getexif()

    if(isinstance(exif_data, dict)):
            mtime = "?"
            if 306 in exif_data and exif_data[306] < mtime:  # 306 = DateTime
                mtime = exif_data[306]
            if 36867 in exif_data and exif_data[36867] < mtime:  # 36867 = DTOriginal
                mtime = exif_data[36867]
            if 36868 in exif_data and exif_data[36868] < mtime:  # 36868 = DTDigitized
                mtime = exif_data[36868]
            return mtime
    else:
        print(fname + " has no EXIF-Data, skipping!")
        return -1


# Checks if Directory exists, if not it spawns it.
def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


# Copies the file (fname) from source to outputdirectory/year/month
def copy_file_to_output(fname, year, month):
    src = sourcedir + "/" + fname
    dst = outputdir + "/" + str(year) + "/" + str(month) + "/"

    ensure_dir(dst)

    shutil.copy2(src, dst)

# splits string and gives back year and month
def str_to_year_month(inp):
    out = inp.split(":")
    return out[0], out[1]

# checks wheter it is jpeg or not
def is_jpg(fname):
    split = fname.split(".")
    if split[1] == "jpg":
        return 1
    else:
        return 0


# Für jede Datei etwas tun
for fname in os.listdir(sourcedir):
    print(fname)
    if is_jpg(fname) != 1:
        continue

    datestr = get_oldest_date(fname)
    print(datestr)
    if isinstance(datestr, str):
        yr, mon = str_to_year_month(datestr)
        copy_file_to_output(fname, yr, mon)
        copycounter+=1

print("I have copied and sorted " + str(copycounter) + " Pictures!")

# nach Datum sortieren in Ordner packen mit Jahr und dann Monat
