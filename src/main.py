#!/usr/bin python3.8.10
# -*- coding: utf-8 -*-

# third party import
import glob
import xmltodict
import logging

# local import
from quantum_patent_analysis.src.database_manager import get_french_patent_collection
from quantum_patent_analysis.src.unzipper import unzip_file_list

# Base path to load the files into the database
BASE_PATH = "/home/valentin/Bureau/projects/brevets/brevet_database"

# Year of the loaded patent
YEAR_RANGE = range(2010, 2023)


def unzip_french_patents():
    """
    Unzip all the french patents
    """
    # for year in YEAR_RANGE:
    #     unzip_file_list(f'{BASE_PATH}/{year}/*NEW*.zip',
    #                     f'{BASE_PATH}/unzipped/{year}/')

    for year in range(2010, 2019):
        unzip_file_list(f'{BASE_PATH}/unzipped/{year}/doc/*.zip',
                        f'{BASE_PATH}/unzipped/{year}/doc/')


def load_french_patents_in_db():
    """
    Load the list of unzipped patents into the database
    """
    patent_collection = get_french_patent_collection()

    # Load years from 2010 to 2018
    for year in range(2010, 2019):
        print(f'Loading year {year}...')
        document_list = []

        for xml_file in glob.glob(f'{BASE_PATH}/unzipped/{year}/doc/*.xml'):
            with open(xml_file, "r") as myfile:
                data = ' '.join(myfile.readlines())
                res = xmltodict.parse(data)
                document_list.append(res)

        if len(document_list) != 0:
            patent_collection.insert_many(document_list)

    # Load year from 2019 to 2022
    for year in range(2019, 2023):
        print(f'Loading year {year}...')
        for directory in glob.glob(f'{BASE_PATH}/unzipped/{year}/*'):
            document_list = []
            for xml_file in glob.glob(f'{directory}/doc/*.xml'):
                with open(xml_file, "r") as myfile:
                    data = ' '.join(myfile.readlines())

                    res = xmltodict.parse(data)
                    document_list.append(res)

            if len(document_list) != 0:
                patent_collection.insert_many(document_list)


def request():
    patent_collection = get_french_patent_collection()
    # print(patent_collection.find_one())
    nb_doc = patent_collection.count_documents({})
    print(f'Nombre documents: {nb_doc}')

    nb_doc_with_title = patent_collection.count_documents({
        "fr-patent-document.fr-bibliographic-data.invention-title.#text": {'$exists': True}
    })
    print(f'Nombre documents with title: {nb_doc_with_title}')

    nb_doc_fr = patent_collection.count_documents({'fr-patent-document.fr-bibliographic-data.invention-title.@lang': 'fr'})
    print(f'Nombre documents français: {nb_doc_fr}')

    cursor = patent_collection.find(
        {
            '$or': [
                {"fr-patent-document.fr-bibliographic-data.invention-title.#text": {'$regex': 'quantique',
                                                                                    '$options': 'i'}},
                {"fr-patent-document.abstract.p" : {'$regex': 'quantique', '$options': 'i'}}
            ]
        }

    )
    res_list = list(cursor)

    print(len(res_list))
    print(res_list[0])

    company_list = {}
    for res in res_list:
        print(res['fr-patent-document']['fr-bibliographic-data']['invention-title']['#text'])
        applicant = res['fr-patent-document']['fr-bibliographic-data']['parties']['applicants']['applicant']
        if type(applicant) == list:
            for app in applicant:
                if 'last-name' in app['addressbook']:
                    name = app['addressbook']['last-name']
                elif 'orgname' in app['addressbook']:
                    name = app['addressbook']['orgname']

                if name in company_list:
                    company_list[name] += 1
                else:
                    company_list[name] = 1


        else:
            if 'last-name' in applicant['addressbook']:
                name = applicant['addressbook']['last-name']
            elif 'orgname' in applicant['addressbook']:
                name = applicant['addressbook']['orgname']

            if name in company_list:
                company_list[name] += 1
            else:
                company_list[name] = 1
    print(company_list)


if __name__ == '__main__':
    # Unzip all the french patents
    # unzip_french_patents()

    # load the french patents into MongoDB
    # load_french_patents_in_db()

    request()