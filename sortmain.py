#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 22:43:56 2018

@author: david
pysort-pics

Usage:
"""

import os
import shutil
import PIL
import logging

sourcedir = '/Users/david/Documents/Handy'
outputdir = '/Users/david/Documents/Output/test'

# init Variables
copycounter = 0

# Set Loglevel to DEBUG.
logging.root.setLevel(logging.DEBUG)


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

            if len(mtime) == 19:
                return mtime
            else:
                logging.warning(fname + " has no correct EXIF-Data.")
                return -1
    else:
        logging.warning(fname + ": has no EXIF-Data.")
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
        logging.debug("Is JPEG")
        return 1
    else:
        logging.debug("Is NOT JPEG")
        return 0


# Für jede Datei etwas tun
for fname in os.listdir(sourcedir):
    logging.info("Found: " + fname)
    if is_jpg(fname) != 1:
        continue

    datestr = get_oldest_date(fname)

    if datestr == -1:
        continue

    logging.debug("Date from Picture is: " + datestr)
    if isinstance(datestr, str):
        logging.debug(datestr)
        yr, mon = str_to_year_month(datestr)
        copy_file_to_output(fname, yr, mon)
        copycounter += 1

str_bye = "I have copied and sorted " + str(copycounter) + " Pictures!"

logging.info(str_bye)
print(str_bye)
