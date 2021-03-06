#!/usr/bin python3.8.10
# -*- coding: utf-8 -*-

# third party import
import json

import pymongo
import nltk

# local import
from quantum_patent_analysis.src.database_manager import \
    get_wipo_single_collection, get_g06N1000_collection

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from datetime import datetime

from quantum_patent_analysis.src.plot_feature import bar_chart_plot


def count_keywords():
    patent_collection = get_wipo_single_collection()

    patents = patent_collection.find()

    stop_words = set(stopwords.words('english'))

    word_list = []

    ipc_list = []

    for patent in patents:
        title = patent['Title'].upper()

        tokenized_word = word_tokenize(title)

        filtered_words = [w.upper() for w in tokenized_word if not w.lower() in stop_words]
        # print(filtered_words)
        word_list += filtered_words

        # if unknown[0] in tokenized_word:
        #     print(title)

        res = [c.strip() for c in patent['I P C'].split(';')]

        for r in res:
            # print(r.split(' ')[0])
            ipc_list.append(r.split(' ')[0])
        # print(res)

    fdist = FreqDist(word_list)
    fdist2 = FreqDist(ipc_list)

    for freq in fdist2.most_common(200):
        print(freq)


keyword_list = [
    'DOT',
    'DOTS',
    'SEMICONDUCTOR',
    'LIGHT',
    'COMMUNICATION',
    'DISTRIBUTION',
    'OPTICAL',
    'LASER',
    'CHIP',
    ''
]

quantum_communication = [
    'COMMUNICATION',
    'NETWORK'
]

quantum_physical = [
    'SEMICONDUCTOR',
    'DOT',
    'DOTS',
    'LIGHT',
    'CARBON',
    'DIODE',
    'MATERIAL',
    'COMPOSITE',
    'LED',
    'OPTICAL',
    'LASER',
    'GRAPHENE',
    'LIQUID',
    'CELL',
    'CRYSTAL',
    'CHIP',
    'EPITAXIAL',
    'FLUORESCENCE',
    'SILICON',
    'QUANTUM-DOT',
    'SUPERCONDUCTING',
    'OXIDE',
    'SULFIDE',
    'PHOTON',
    'POLYMER',
    'ION',
    'ZINC',
    'SILVER'
]

quantum_cryptography = [
    'ENCRYPTION',
    'SECURITY',
    'AUTHENTICATION',
    'CHANNEL',
    'FIBER',
    'CRYPTOGRAPHY',
    'SECURE'
]


quantum_computing = [
    'COMPUTING',
    'COMPUTER',
    'CIRCUIT',
    'APPLICATION',
    'GATE',
    'PROGRAM',
    'SIMULATION',
    'ALGORITHM',
    'COMPUTATION'
]

unknown = [
    'SIGNAL',
    'LOGIC',
    'PROCESSOR',
    'MONITORING',
    'OPTIMIZATION'
]


ipc_classification = [
    'H01L', # SEMICONDUCTOR DEVICES; ELECTRIC SOLID STATE DEVICESs
    'C09K', # MATERIALS FOR APPLICATIONS NOT OTHERWISE PROVIDED FOR; APPLICATIONS OF MATERIALS NOT OTHERWISE PROVIDED FOR
    'B82Y', # SPECIFIC USES OR APPLICATIONS OF NANOSTRUCTURES; MEASUREMENT OR ANALYSIS OF NANOSTRUCTURES; MANUFACTURE  OR TREATMENT OF NANOSTRUCTURES
    'H04L', # TRANSMISSION OF DIGITAL INFORMATION, e.g. TELEGRAPHIC COMMUNICATION
    'G06N', # COMPUTER SYSTEMS BASED ON SPECIFIC COMPUTATIONAL MODELS
    'H01S', # DISPOSITIFS UTILISANT L'??MISSION STIMUL??E
    '',
    '',
    '',
    '',
    '',
    '',

]

ipc_precise_classification = [
    'G06N 10/00' #Quantum computers, i.e. computer systems based on quantum-mechanical phenomena
]


def get_major_applicants(collection):
    """
    Get the major applicants of quantum technologies patentss
    """

    with open('./patent_study/principal_applicants.json', 'r') as f:
        major_applicants = json.load(f)

    major_applicant_dict = {}

    for applicant_label, applicant in major_applicants.items():
        regex_list = []
        for applicant_name in applicant['names']:
            regex_list.append({'Applicants': {'$regex': applicant_name, '$options': 'i'}})

        patent_count = collection.count_documents({
            '$or': regex_list
        })

        if patent_count >= 30:
            major_applicant_dict[applicant_label] = patent_count

        patent_list = collection.find({
            '$or': regex_list
        })

        earliest_date = None

        for patent in patent_list:
            if earliest_date is None:
                earliest_date = datetime.strptime(patent['Publication Date'], '%d.%m.%Y')

            else:
                current_date = datetime.strptime(patent['Publication Date'], '%d.%m.%Y')
                if current_date < earliest_date:
                    earliest_date = current_date

        applicant['earliest_date'] = earliest_date

    # Sort the final dictionary:
    sorted_dict = dict(sorted(major_applicant_dict.items(), key=lambda item: -item[1]))
    print(sorted_dict)

    print('| Rank | Company name | Number of families of patent | Headquarter | First patent published on |')
    print('| ---- | ------------ | ---------------------------- | ----------- | ------------------------- |')
    rank = 1
    for company, patent_family_count in sorted_dict.items():
        print(f'| {rank} | [{company}]({major_applicants[company]["website"]}) '
              f'| {patent_family_count} | {major_applicants[company]["headquarters"]} '
              f'| {major_applicants[company]["earliest_date"].strftime("%d/%m/%Y")}')
        rank += 1

    # patents = patent_collection.find()
    #
    # applicants = []
    #
    # for patent in patents:
    #     applicants += [a.strip().upper() for a in patent['Applicants'].split(';')]
    #
    # fdist2 = FreqDist(applicants)
    #
    # for dist in fdist2.most_common(100):
    #     print(dist)


applicants_replacement = {
    '????????????????????????????????????????????????': 'Hefei Benyuan Quantum Computing Technology Co., Ltd.',
    '????????????????????????????????????': 'Beijing Baidu Netcom Technology Co., Ltd.',
    '????????????????????????': 'University of Science and Technology of China',
    '????????????': 'Tsinghua University',
    '????????????????????????????????????????????????': 'Jinan Inspur High-tech Investment Development Co., Ltd.',
    '??????': '?',
    '????????????????????????????????????': 'Tencent Technology (Shenzhen) Co., Ltd.',
    '?????????????????????????????????????????????????????????': 'Chinese People\'s Liberation Army Strategic Support Force Information Engineering University',
    '??????????????????': 'Southern University of Science and Technology',
    '????????????????????????': 'Huawei Technologies Co., Ltd',
    '???????????????????????????????????????': 'Shandong Inspur Scientific Research Institute Co., Ltd.',
    '???????????????': 'Intel Corporation',
    '?????????????????????': 'Harbin Engineering University',
    '????????????????????????????????????': 'Suzhou Inspur Intelligent Technology Co., Ltd.',
    '??????????????????': 'Chongqing University of Posts and Telecommunications',
    '?????????????????????': 'FUJITSU LIMITED',
    '????????????????????????': 'NEC',
    '????????????': 'Southeast University',
    '??????????????????': 'Nanjing Normal University',
    '????????????????????????????????????????????????': 'Guo Kaike Quantum Technology (Beijing) Co., Ltd.',
    '??????????????????????????????': 'Shenzhen Liangxuan Technology Co., Ltd.',
    '????????????': 'Shenzhen University',
    '?????????????????????????????????????????????': 'Shenzhen Yongda Electronic Information Co., Ltd.',
    '?????????????????????????????????': 'Beijing Institute of Quantum Information Science',
    '????????????????????????': 'Chengdu University of Information Technology',
    '????????????????????????': 'Nanjing University of Aeronautics and Astronautics',
    '??????????????????????????????': 'Rupan Quantum Technology Co., Ltd.',
    '??????????????????????????????': 'Shirong Energy Technology Co., Ltd.',
    '??????????????????': 'Zhejiang University of Commerce and Industry',
    '????????????': 'Sichuan University',
    '??????????????????????????????': 'Nippon Telegraph and Telephone Co., Ltd.'
}


def patent_per_year():
    """
    Compute and plot the amount of patents published per year
    """
    patent_collection = get_g06N1000_collection()
    patents = patent_collection.find()

    year_range = range(2002, 2022)
    year_dict = {}

    for year in year_range:
        year_dict[year] = 0

    for patent in patents:
        year = int(patent['Publication Date'].split('.')[2])

        if year in year_dict:
            year_dict[year] += 1

    x_axis = [str(int(year)) for year in year_range]
    y_axis = []

    for year in year_range:
        y_axis.append(year_dict[year])

    item_dict = {
        'xlabel': 'Year',
        'ylabel': 'Number of patent family',
        'x_rotate': True,
        'yscale': 'log',
        'title': 'Number of patents family published per year',
        'items': [
            {
                'type': 'bar',
                'x_axis': x_axis,
                'y_axis': y_axis
            }
        ]
    }

    bar_chart_plot(item_dict, './patent_study/patents_per_year')

# def check_tuple_list(company1, company2):

def generate_tuples(applicants):
    tuple_list = []

    for i, a in enumerate(applicants):
        for b in applicants[i:]:
            if b != a:
                tuple_list.append((b, a))
    return tuple_list


def get_couples():
    patent_collection = get_g06N1000_collection()
    patents = patent_collection.find()

    final_tuple_dict = {}

    for patent in patents:
        applicants = [a.strip().upper() for a in patent['Applicants'].split(';')]

        for i, applicant in enumerate(applicants):
            if applicant in applicants_replacement:
                applicants[i] = applicants_replacement[applicant]

        tuple_list = generate_tuples(applicants)

        for m_tuple in tuple_list:
            tmp_tuple = (m_tuple[1], m_tuple[0])
            if m_tuple in final_tuple_dict:
                final_tuple_dict[m_tuple] += 1
            elif tmp_tuple in final_tuple_dict:
                final_tuple_dict[tmp_tuple] += 1
            else:
                final_tuple_dict[m_tuple] = 1

    # print(final_tuple_dict)

    res = dict(sorted(final_tuple_dict.items(), key=lambda item: item[1]))

    for k, v in res.items():
        print(k, v)
    # print(res)
# TODO: Faire un croisement entre les brevets crois??s entre plusieurs entit??s

# TODO: Faire une ??tude d??taill??e des brevets pour entreprises publiant bcp


def get_target_countries(collection):
    """
    Get the repartition of the family of patents per country.
    The dictionary of countries is stored in "patent_countries.json"
    The list of codes can be found on:
    https://www.iso.org/obp/ui/#iso:code:3166:NL

    We only retrieved the codes having 1 or more family of patents
    """
    target_countries = collection.aggregate([
        {
            '$group': {
                '_id': '$Country',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'count': -1}
        }
    ])

    with open('./patent_study/patent_countries.json') as f:
        countries = json.load(f)

    print('| Region of application | Number of patent families |')
    print('| --------------------- | ------------------------- |')
    for target in target_countries:
        if target['count'] > 1:
            if target['_id'] in countries:
                print(f'| {countries[target["_id"]]} | {target["count"]} |')


if __name__ == '__main__':
    patent_collection = get_g06N1000_collection()

    # count_keywords()
    # count_applicants()

    # plot the amount of patent per year
    # patent_per_year()

    # Retrieve the major applicants
    get_major_applicants(patent_collection)

    # print(len(quantum_principal_actors))

    # Get the couples
    # get_couples()

    # Get the markdown table returning effecting zone for families of
    # patents
    # get_target_countries(patent_collection)
