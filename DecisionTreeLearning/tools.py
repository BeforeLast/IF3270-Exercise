from typing import Any
from classes.dataset import Dataset
from math import log2

def Gain(dataset:Dataset, label_fieldname:str, attribute_fieldname:str):
    global_e = Entropy(dataset,label_fieldname)
    sigma_e = 0

    # Get data
    data = dataset.get_data()

    # Count value occurence
    value_counter = {value:0 for value in dataset.get_field_values(attribute_fieldname)}
    attribute_idx = dataset.get_fields()[attribute_fieldname]
    for record in data:
        value_counter[record[attribute_idx]] += 1

    # Calculate sigma
    for value in value_counter:
        sigma_e += (value_counter[value]/len(data)) * (Entropy(dataset,label_fieldname,attribute_fieldname,value))

    # Return gain value
    return global_e - sigma_e

def Entropy(dataset:Dataset, label_fieldname:str, attribute_fieldname:str=None, selected_value:Any=None) -> float:
    # Select relevant data
    if selected_value is None and attribute_fieldname is None:
        data = dataset.get_data()
    else:
        data = dataset.get_specified_data(attribute_fieldname,selected_value)
    
    # Count label occurence
    label_counter = {label:0 for label in dataset.get_field_values(label_fieldname)} # {'val1': 2}
    label_index = dataset.get_fields()[label_fieldname] # label idx
    for record in data:
        label_counter[record[label_index]] += 1
    
    # Calculate entropy value
    e_val = 0
    for value in list(label_counter):
        try:
            e_val += -(label_counter[value]/len(data)) * log2(label_counter[value]/len(data))
        except ValueError:
            continue
    # print(e_val)
    return e_val

if __name__ == '__main__':
    dset = Dataset("./DecisionTreeLearning/data/kuis1.csv")
    print(Entropy(dset,'Class'))
