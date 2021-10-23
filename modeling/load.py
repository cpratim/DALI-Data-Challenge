import json
from pprint import pprint
import numpy as np
import os
from util.helpers import *

data_dir = 'data'

n_rules = {
    'year': lambda x: int(x[1:]),
    'gender': lambda x: int(x == 'Male'),
    'phoneType': lambda x: int(x == 'iOS')
}

d_rules = {
    'birthday': {'age': difference},
    'American Indian or Alaska Native': {'race': lambda x: None if x == '' else x},
    'Asian': {'race': lambda x: None if x == '' else x},
    'Black or African American': {'race': lambda x: None if x == '' else x},
    'Hispanic or Latino': {'race': lambda x: None if x == '' else x},
    'Middle Eastern': {'race': lambda x: None if x == '' else x},
    'Native Hawaiian or Other Pacific Islander': {'race': lambda x: None if x == '' else x},
    'White': {'race': lambda x: None if x == '' else x},
    'Other': {'race': lambda x: None if x == '' else x},
    'year': lambda x: int(x[1:]),
}

def load_numerical(rules = n_rules):
    arr = []
    with open(f'{data_dir}/DALI_Data-Anon.json', 'r') as handle:
        dataframe = json.load(handle)
        for point in dataframe:
            n_point = []
            for key in point:
                if key in n_rules:
                    n_point.append(n_rules[key](point[key]))
                else:
                    n_point.append(point[key] if point[key] != None else 0)
            arr.append(n_point)

    return np.array(arr), list(dataframe[0].keys())

def load_descriptive():
    desc = []
    with open(f'{data_dir}/DALI_Data.json', 'r') as f:
        dataframe = json.load(f)
        for point in dataframe:
            feat = {}
            for key in point:
                if key in d_rules:
                    rules = d_rules[key]
                    if type(rules) == dict:
                        for nkey in rules:
                            t = rules[nkey](point[key])

                            if t != None: feat[nkey] = t
                    else:
                        feat[key] = rules(point[key])
                else:
                    feat[key] = point[key]
            desc.append(feat)
    return desc

def download_images():
    if not os.path.exists(f'{data_dir}/pictures'):
        os.mkdir(f'{data_dir}/pictures')
        
    data = load_descriptive()


if __name__ == '__main__':

    data, features = load_numerical()
    d = load_descriptive()
    print(len(data))

    print('First Numerical Point:')
    for f, p in zip(features, data[0]):
        print(f'{f}: {p}')

    print('\nFirst Descriptive Point:')
    pprint(d[0])
