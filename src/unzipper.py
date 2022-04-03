#!/usr/bin python3.8.10
# -*- coding: utf-8 -*-

# third party import
import glob
import zipfile

# local import


def unzip_file_list(source, dest_path):
    for zipped_files in glob.glob(source):
        with zipfile.ZipFile(zipped_files, "r") as zip_ref:
            zip_ref.extractall(dest_path)
