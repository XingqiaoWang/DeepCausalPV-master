import csv
import scipy.stats as st
import statistics
import math
import os
import argparse
from random import sample


class causal_cell():
    def __init__(self, Feature, value, z_score, probability_do, probability_not_do, p_value, support, condition_list):
        self.Feature = Feature
        self.value = value
        self.z_score = z_score
        self.probability_do = probability_do
        self.probability_not_do = probability_not_do
        self.probability_difference = probability_do - probability_not_do
        self.p_value = p_value
        self.support = support
        self.condition_list = condition_list

    def set_condition_list(condition_list):
        self.condition_list = condition_list

    def get_variable_list1(self):
        variable_list = [self.Feature, self.value, self.z_score, self.probability_do, self.probability_not_do,
                         self.probability_difference, self.p_value, self.support]
        return variable_list

    def get_variable_list2(self):
        variable_list = [self.Feature, self.value, self.z_score, self.probability_do, self.probability_not_do,
                         self.probability_difference, self.p_value, self.support, self.condition_list]
        return variable_list


def causal_tree(feature_file, probability_file, threshold, condition_list):
    gender_dict = {}
    gender_not_empty_dict = {}
    age_dict = {}
    age_not_empty_dict = {}
    ade_dict = {}
    ade_not_empty_dict = {}
    psd_dict = {}
    psd_not_empty_dict = {}
    dose_dict = {}
    dose_not_empty_dict = {}
    indication_dict = {}
    indication_not_empty_dict = {}
    outcome_dict = {}
    outcome_not_empty_dict = {}
    probability_dict = {}

    def condition(condition_list, line):

        all_term_in = True
        if condition_list == []:
            return False
        for term in condition_list:
            if not term in line:
                all_term_in = False
        if all_term_in:
            return False
        else:
            return True

    def put_in_dict(index, str, dict):
        a = str.split(', ')
        for item in a:
            if not item in dict:
                dict[item] = [index]
            else:
                dict[item].append(index)
        return dict

    def put_in_dict_psd(index, str, dict):
        a = str.split('; ')
        for item in a:
            if not item in dict:
                dict[item] = [index]
            else:
                dict[item].append(index)
        return dict

    with open(feature_file) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for index, line in enumerate(tsvreader):
            if index == 0:
                continue
            else:

                age, ade, dose, psd, gender, indication, outcome = line
                if condition(condition_list, line):
                    continue
                if dose != ' ':
                    dose_not_empty_dict[index] = True
                if age != ' ':
                    age_not_empty_dict[index] = True
                if ade != ' ':
                    ade_not_empty_dict[index] = True
                if psd != ' ':
                    psd_not_empty_dict[index] = True
                if gender != ' ':
                    gender_not_empty_dict[index] = True
                if indication != ' ':
                    indication_not_empty_dict[index] = True
                if outcome != ' ':
                    outcome_not_empty_dict[index] = True
                gender_dict = put_in_dict(index, gender, gender_dict)
                age_dict = put_in_dict(index, age, age_dict)
                psd_dict = put_in_dict(index, psd, psd_dict)
                dose_dict = put_in_dict(index, dose, dose_dict)
                indication_dict = put_in_dict(index, indication, indication_dict)
                ade_dict = put_in_dict(index, ade, ade_dict)
                outcome_dict = put_in_dict(index, outcome, outcome_dict)
    with open(probability_file) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in enumerate(tsvreader):
            probability_dict[line[0] + 1] = line[1]

    def compute_gap(feature_dict, p_dict, not_empty_dict):
        dict = {}
        dict_in = {}
        dict_out = {}

        def compute_Z_score(in_list, out_list):
            L1 = []
            for term in in_list:
                L1.append(float(term[1]))
            L2 = []
            for term in out_list:
                L2.append(float(term[1]))
            s1 = statistics.variance(L1)
            l1 = s1 / len(L1)
            s2 = statistics.variance(L2)
            l2 = s2 / len(L2)
            l = l1 + l2
            m = math.sqrt(l)
            m1 = statistics.mean(L1)
            m2 = statistics.mean(L2)
            return (m1 - m2) / m

        def compute_expecation(list):
            L = []
            for term in list:
                L.append(float(term[1]))
            if not len(L) == 0:
                return sum(L) / len(L)
            else:
                return 0

        for key in feature_dict.keys():
            l1 = feature_dict[key]
            In = []
            Out = []
            for index in p_dict.keys():
                if index in not_empty_dict:
                    if index in l1:
                        In.append(p_dict[index])
                    else:
                        Out.append(p_dict[index])

            if len(In) >= threshold and len(Out) >= threshold:
                dict[key] = compute_Z_score(In, Out)
                dict_in[key] = compute_expecation(In)
                dict_out[key] = compute_expecation(Out)

        return dict, dict_in, dict_out

    gender_gap_dict, gender_in_dict, gender_out_dict = compute_gap(gender_dict, probability_dict, gender_not_empty_dict)
    age_gap_dict, age_in_dict, age_out_dict = compute_gap(age_dict, probability_dict, age_not_empty_dict)
    psd_gap_dict, psd_in_dict, psd_out_dict = compute_gap(psd_dict, probability_dict, psd_not_empty_dict)
    dose_gap_dict, dose_in_dict, dose_out_dict = compute_gap(dose_dict, probability_dict, dose_not_empty_dict)
    indication_gap_dict, indication_in_dict, indication_out_dict = compute_gap(indication_dict, probability_dict,
                                                                               indication_not_empty_dict)
    ade_gap_dict,ade_in_dict,ade_out_dict=compute_gap(ade_dict,probability_dict,ade_not_empty_dict)

    total_dict = {**gender_gap_dict,
                  **age_gap_dict,
                  **psd_gap_dict,
                  **dose_gap_dict,
                  **indication_gap_dict,
                  **ade_gap_dict,
                  }
    cell_list = []
    for key in total_dict:

        z_score = total_dict[key]
        p_values = 1 - st.norm.cdf(z_score)
        if not p_values <= 0.05:
            continue

        if key in gender_gap_dict:
            cell = causal_cell('gender', key, total_dict[key], gender_in_dict[key], gender_out_dict[key], p_values,
                               len(gender_dict[key]), condition_list)
        if key in age_gap_dict:
            cell = causal_cell('age', key, total_dict[key], age_in_dict[key], age_out_dict[key], p_values,
                               len(age_dict[key]), condition_list)
        if key in psd_gap_dict:
            cell = causal_cell('psd', key, total_dict[key], psd_in_dict[key], psd_out_dict[key], p_values,
                               len(psd_dict[key]), condition_list)
        if key in dose_gap_dict:
            cell = causal_cell('dose', key, total_dict[key], dose_in_dict[key], dose_out_dict[key], p_values,
                               len(dose_dict[key]), condition_list)
        if key in indication_gap_dict:
            cell = causal_cell('indication', key, total_dict[key], indication_in_dict[key], indication_out_dict[key],
                               p_values, len(indication_dict[key]), condition_list)
        if key in ade_gap_dict:
            cell=causal_cell('adversary events',key,total_dict[key],ade_in_dict[key],ade_out_dict[key],p_values,len(ade_dict[key]),condition_list)

        cell_list.append(cell)
    return cell_list


def causal_inference(probability_file, feature_file, out_dir, threshold=100):
    condition_list = []
    cell_list = causal_tree(feature_file, probability_file, threshold, condition_list)

    def myFunc(e):
        return e.get_variable_list1()[2]

    cell_list.sort(reverse=True, key=myFunc)
    # write csv file
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    title = ['Feature', 'value', 'z score', 'probability of do value', 'probability of not do value',
             'probability difference', 'p value', 'support']
    with open(out_dir + '/root' + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(title)
        for cell in cell_list:
            a_list = cell.get_variable_list1()
            spamwriter.writerow(a_list)


def generate_causal_tree(probability_file, feature_file, out_dir, threshold=100):
    def myFunc(e):
        return e.get_variable_list1()[2]

    condition_list = []
    cell_list = causal_tree(feature_file, probability_file, threshold, condition_list)
    cell_list.sort(reverse=True, key=myFunc)
    stack = cell_list
    total_cell_list = []

    while not stack == []:
        one_cell = stack[0]
        condition_term = one_cell.get_variable_list2()[1]
        condition_list = one_cell.get_variable_list2()[8].copy()
        if one_cell.get_variable_list2()[3] >= 0.5:
            condition_list.append(condition_term)
            if len(condition_list) > 3:
                stack.pop(0)
                continue
            cell_list = causal_tree(feature_file, probability_file, threshold, condition_list)
            cell_list.sort(reverse=True, key=myFunc)
            total_cell_list.append(one_cell)
            stack.pop(0)
            stack = stack + cell_list
        else:
            stack.pop(0)

    title = ['level', 'route', 'Feature', 'value', 'z score', 'probability of do value', 'probability of not do value',
             'probability difference', 'p value', 'support']
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    with open(out_dir + '/causal_tree.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(title)
        current_level = 0
        for cell in total_cell_list:
            a_list = cell.get_variable_list2()
            route = '->'.join(a_list[-1])
            line = []
            line.append(len(a_list[-1]))
            line.append(route)
            line = line + cell.get_variable_list1()
            if current_level < len(a_list[-1]):
                current_level = len(a_list[-1])
                spamwriter.writerow([])
            spamwriter.writerow(line)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--probability-file', type=str, default='')
    parser.add_argument('--feature-file', type=str, default='')
    parser.add_argument('--out-dir', type=str, default='')

    args = parser.parse_args()
    causal_inference(args.probability_file, args.feature_file, args.out_dir)
    generate_causal_tree(args.probability_file, args.feature_file, args.out_dir)


if __name__ == "__main__":
    main()
