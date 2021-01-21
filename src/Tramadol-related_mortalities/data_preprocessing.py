import argparse
import pandas as pd
import numpy as np
import re
import csv
import os
import sys
import random


def _normalization(dict, index_dict):
    indication_index=index_dict['indication_index']
    dose_index=index_dict['dose_index']
    outcome_empty_list = []
    outcome_index=index_dict['outcome_index']
    for key in dict:
        if (dict[key][outcome_index] == ' '):
            outcome_empty_list.append(key)
    for key in outcome_empty_list:
        dict.pop(key)
    for key in dict:
        if ' UNK ' in dict[key][indication_index] or 'UNKNOWN' in dict[key][indication_index]:
            dict[key][indication_index] = ' '
        if ('UNK' in dict[key][dose_index] or 'UNKNOWN' in dict[key][dose_index] or '()' in dict[key][dose_index]):
            dict[key][dose_index] = ' '
    return dict


def _dose_unify(dict, index_dict):
    dose_index = index_dict['dose_index']
    for key in dict:
        if (dict[key][dose_index] == ' '):
            continue
        if 'MG' in str(dict[key][dose_index]):
            res = re.findall(r'\d+\.*\d*', dict[key][dose_index].split('MG')[0])
            if (len(res) == 0):
                value = dict[key]
                value[dose_index] = ' '
                continue
            if (float(max(res)) > 100):
                value = dict[key]
                value[dose_index] = 'larger than 100 MG'
            else:
                value = dict[key]
                value[dose_index] = 'equal or smaller than 100 MG'
            dict[key] = value
        elif 'mg' in str(dict[key][dose_index]):
            res = re.findall(r'\d+\.*\d*', dict[key][dose_index].split('mg')[0])
            if (len(res) == 0):
                value = dict[key]
                value[dose_index] = ' '
                continue
            if (float(max(res)) > 100):
                value = dict[key]
                value[dose_index] = 'larger than 100 MG'
            else:
                value = dict[key]
                value[dose_index] = 'equal or smaller than 100 MG'
            dict[key] = value
        elif 'MILLIGRAM' in str(dict[key][dose_index]):
            res = re.findall(r'\d+\.*\d*', dict[key][dose_index].split('MILLIGRAM')[0])
            if (len(res) == 0):
                value = dict[key]
                value[dose_index] = ' '
                continue
            if (float(max(res)) > 100):
                value = dict[key]
                value[dose_index] = 'larger than 100 MG'
            else:
                value = dict[key]
                value[dose_index] = 'equal or smaller than 100 MG'
            dict[key] = value
        elif 'MICROGRAM' in str(dict[key][dose_index]):
            value = dict[key]
            value[dose_index] = 'equal or smaller than 100 MG'
            dict[key] = value
        elif 'UG' in str(dict[key][dose_index]):
            res = re.findall(r'\d+\.*\d* UG', dict[key][dose_index])
            if len(res) > 0:
                value = dict[key]
                value[dose_index] = 'equal or smaller than 100 MG'
                dict[key] = value
        elif 'MCG' in str(dict[key][dose_index]):
            value = dict[key]
            value[dose_index] = 'equal or smaller than 100 MG'
            dict[key] = value
        elif 'GRAM' in str(dict[key][dose_index]):
            value = dict[key]
            value[dose_index] = 'larger than 100 MG'
            dict[key] = value
        elif 'G' in str(dict[key][dose_index]):
            res1 = re.findall(r'\d+\.*\d* G', dict[key][dose_index])
            res2 = re.findall(r'\d+\.*\d*G', dict[key][dose_index])
            if len(res1) > 0 or len(res2) > 0:
                value = dict[key]
                value[dose_index] = 'larger than 100 MG'
                dict[key] = value
    return dict


def _age_unify(dict, index_dict):
    def age_divide(age_year):
        if age_year < 18:
            age = 'younger than 18'
        elif age_year < 40:
            age = '18-39'
        elif age_year < 65:
            age = '40-64'
        elif age_year >= 65:
            age = 'older than 65'
        return age
    age_index = index_dict['age_index']
    age_unit_index = age_index + 1
    for key in dict:
        type = dict[key][age_unit_index]
        if type == ' ':
            continue
        if type == 'Day':
            age_year = float(dict[key][age_index]) / 365
            age = age_divide(age_year)
        elif type == 'Month':
            age_year = float(dict[key][age_index]) / 12
            age = age_divide(age_year)
        elif type == 'Week':
            age_year = float(dict[key][age_index]) / 52
            age = age_divide(age_year)
        elif type == 'Decade':
            age_year = float(dict[key][age_index]) * 10
            age = age_divide(age_year)
        elif type == 'Hour':
            age_year = float(dict[key][age_index]) / 8760
            age = age_divide(age_year)
        elif type == 'Year':
            age_year = float(dict[key][age_index])
            age = age_divide(age_year)

        case = dict[key]
        case[age_index] = age
        dict[key] = case
    return dict


def _generate_ALBERT_dataset(dict, target_list, out_dir, index_dict):
    def _generate_dataset(dict, target_list, index_dict):
        value_list = []
        rows_list = []
        rows_list2 = []
        dose_index = index_dict['dose_index']
        age_index = index_dict['age_index']
        psd_index = index_dict['psd_index']
        ade_index = index_dict['ade_index']
        gender_index = index_dict['gender_index']
        indication_index = index_dict['indication_index']
        outcome_index= index_dict['outcome_index']
        for item in dict.values():
            value_list.append(item)
        for inx, case in enumerate(value_list):
            dose = case[dose_index].replace('\n', '')
            age = case[age_index].replace('\n', '')
            psd = case[psd_index].replace('\n', '')
            ade = case[ade_index].replace('\n', '')
            gender = case[gender_index].replace('\n', '')
            indication = case[indication_index].replace('\n', '')
            outcome = case[outcome_index].replace('\n', '')
            if gender != ' ':
                if age != ' ':
                    tmp = 'Patient (' + gender + ', ' + age + ')'
                else:
                    tmp = 'Patient (' + gender + ')'
            elif age != ' ':
                tmp = 'Patient (' + age + ')'
            else:
                tmp = 'Patient '
            part1 = tmp
            if dose != 'larger than 100 MG' and dose != 'equal or smaller than 100 MG':
                part2 = ' took ' + psd
            else:
                part2 = ' took ' + psd + ' with ' + dose
            if indication == ' ':
                part3 = ''
            else:
                part3 = ' to treat ' + indication
            if ade == ' ':
                part4 = ''
            else:
                part4 = ', caused ' + ade
            s = part1 + part2 + part3 + part4 + '.'
            if '00:00:00' in s:
                continue
            label = ''
            for index, target_term in enumerate(target_list):
                for term in outcome.split(', '):
                    if term == target_term:
                        label = '1'
                        break
                if not label == '1':
                    label = '0'

            dict1 = {}
            dict2 = {}

            dict1['sentence'] = s
            dict1['label'] = label

            dict2['age'] = age
            dict2['ade'] = ade
            dict2['dose'] = dose
            dict2['psd'] = psd
            dict2['gender'] = gender
            dict2['indication'] = indication
            dict2['outcome'] = outcome

            rows_list.append(dict1)
            rows_list2.append(dict2)
        df1 = pd.DataFrame(rows_list)
        df2 = pd.DataFrame(rows_list2)

        return df1, df2

    df1, df2 = _generate_dataset(dict, target_list,index_dict)
    train_dev = df1.sample(frac=0.8)
    train = train_dev.sample(frac=0.8)
    dev = train_dev.drop(train.index)
    test = df1.drop(train_dev.index)

    with open(out_dir + '/train.tsv', 'w', newline='') as write_tsv:
        write_tsv.write(train.to_csv(sep='\t', index=False))
    with open(out_dir + '/dev.tsv', 'w', newline='') as write_tsv:
        write_tsv.write(dev.to_csv(sep='\t', index=False))
    with open(out_dir + '/test.tsv', 'w', newline='') as write_tsv:
        write_tsv.write(test.to_csv(sep='\t', index=False))
    with open(out_dir + '/all.tsv', 'w', newline='') as write_tsv:
        write_tsv.write(df1.to_csv(sep='\t', index=False))
    with open(out_dir + '/feature.tsv', 'w', newline='') as write_tsv:
        write_tsv.write(df2.to_csv(sep='\t', index=False))


def preprocess(dataset_dir, dataset_name, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    article_read = pd.read_csv(dataset_dir + '/' + dataset_name, delimiter=',')
    dataset = article_read.to_numpy()
    target_list = ['Death']
    dict = {}
    for case in dataset:
        if str(case[0]) not in dict:
            dict[str(case[0])] = case.copy()
    index_dict = {'ade_index':5,
                  'age_index':9,
                  'dose_index':4,
                  'gender_index':8,
                  'indication_index':11,
                  'outcome_index':6,
                  'psd_index':2,
                  'target_index':6}
    dict = _normalization(dict, index_dict)
    dict = _dose_unify(dict, index_dict)
    dict = _age_unify(dict, index_dict)
    _generate_ALBERT_dataset(dict, target_list, out_dir,index_dict)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset-dir', type=str, default='../../dat/Tramadol-related_mortalities/dataset')
    parser.add_argument('--dataset-name', type=str, default='dataset.csv')
    parser.add_argument('--out-dir', type=str, default='../../dat/Tramadol-related_mortalities/proc')

    args = parser.parse_args()
    preprocess(args.dataset_dir,args.dataset_name,args.out_dir)


if __name__ == "__main__":
    main()
