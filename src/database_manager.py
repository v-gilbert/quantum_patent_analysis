#!/usr/bin python3.8.10
# -*- coding: utf-8 -*-

# third party import

# local import
import pymongo
import sqlite3

from quantum_patent_analysis.src.constants import PATENT_DB, MONGO_CLIENT


def get_french_patent_collection():
    myclient = pymongo.MongoClient(MONGO_CLIENT)
    return myclient[PATENT_DB]['french_patent']


def get_wipo_single_collection():
    my_client = pymongo.MongoClient(MONGO_CLIENT)
    return my_client[PATENT_DB]['single_familly_patent']


def get_g06N1000_collection():
    my_client = pymongo.MongoClient(MONGO_CLIENT)
    return my_client[PATENT_DB]['patent_G06N1000']
