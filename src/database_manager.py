#!/usr/bin python3.8.10
# -*- coding: utf-8 -*-

# third party import

# local import
import pymongo

from quantum_patent_analysis.src.constants import PATENT_DB, MONGO_CLIENT


def get_french_patent_collection():
    myclient = pymongo.MongoClient(MONGO_CLIENT)
    return myclient[PATENT_DB]['french_patent']
