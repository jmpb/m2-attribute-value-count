import os
import pickle
import sys
import pandas as pd
import numpy as np

def pickle_to_file(obj, file_name):
    '''serialize an object to file'''
    try:
        with open(sys.path[0] + os.sep + file_name, 'wb') as write_to_file:
            pickle.dump(obj, write_to_file, pickle.HIGHEST_PROTOCOL)
    except FileNotFoundError:
        return None

def unpickle_from_file(file_name):
    '''desearialize an object from file'''
    try:
        with open(sys.path[0] + os.sep + file_name, 'rb') as read_from_file:
            return pickle.load(read_from_file)
    except FileNotFoundError:
        return None

def report_attribute_value_usage(attr_code, attr_val):
    '''
    Given the attribute code and the value, get all rows which use the
    value in that attribute and return a report.
    '''
    spreadsheet = pd.read_csv('all-products-attributes.csv', low_memory=False)
    rows_with_attribute_value = spreadsheet.loc[spreadsheet[attr_code] == attr_val]
    use_count = len(list(rows_with_attribute_value.sku.unique()))
    used_by_skus = list(rows_with_attribute_value.sku.unique())
    return (use_count, used_by_skus)

def collect_attributes_and_values():
    '''
    Collect and prepare a dictionary of attributes and a distinct list
    of its value options.
    '''
    attribute_dict = dict()
    spreadsheet = pd.read_csv('Attribute_value_list.csv', low_memory=False)

    unique_attributes = spreadsheet.attribute_code.unique()
    attribute_list = unique_attributes.tolist()

    for a in attribute_list:
        rows_with_attribute_code = spreadsheet.loc[spreadsheet['attribute_code'] == a]
        value_list = list(rows_with_attribute_code['option:value'].unique())
        # Replace nans (NaN) with empty str
        val = ["" if not isinstance(v, str) and np.isnan(v) else v for v in value_list]
        attribute_dict[a] = val

    return attribute_dict

if __name__ == "__main__":
    attr_dict = unpickle_from_file('attr_values.pickle') or collect_attributes_and_values()
    if attr_dict:
        pickle_to_file(attr_dict, 'attr_values.pickle')
    with open('unused_attribute_value.csv', 'w') as result_file:
        COL_LABELS = "attribute,value,use_count,used_by_skus\n"
        result_file.write(COL_LABELS)
        for attribute in attr_dict:
            for value in attr_dict[attribute]:
                if value:
                    report = report_attribute_value_usage(attribute, value.replace(',', '-'))
                    SKU_LIST = "|".join(report[1])
                    line = f"{attribute},{value},{report[0]},{SKU_LIST}\n"
                    result_file.write(line)
