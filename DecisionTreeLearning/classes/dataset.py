# Type Hint
from __future__ import annotations
from typing import Any

import csv

class Dataset:
    data: list[list[Any]] = None
    field: dict[Any,int] = None
    field_values: dict[Any,list[Any]] = None

    def __init__(self, dir:str=None):
        self.data = []
        self.field = {}
        if dir is not None:
            with open(dir,'r',newline='',encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                # Create temporary array
                temp = []
                for temp_v in reader:
                    temp.append(temp_v)

                # Mapping field index
                for i in range(len(temp[0])):
                    self.field[temp[0][i]] = i
                
                # Splitting data
                for row in temp[1:]:
                    self.data.append(row)
                
                # Generating field list values
                self.generate_fields_values()

    def generate_fields_values(self):
        self.field_values = {}
        temp = self.data.copy()
        data_value = [[temp[j][i] for j in range(len(temp))] for i in range(len(temp[0]))]
        for key in self.field:
            self.field_values[key] = list(set(data_value[self.field[key]]))

    def set_fields(self,field:dict):
        self.field = field

    def set_data(self,data:list):
        self.data = data

    def get_fields(self):
        return self.field.copy()

    def get_data(self):
        return self.data.copy()

    def get_field_values(self, fieldname:str) -> list:
        return self.field_values[fieldname].copy()
    
    def get_specified_data(self,fieldname:str,value:Any) -> list:
        if fieldname is None or value is None:
            raise ValueError("fieldname or/and value required!")
        if fieldname and value:
            field_idx = self.field[fieldname]
            temp = []
            for record in self.data:
                if record[field_idx] == value:
                    temp.append(record)
            return temp
    
    def separate_by_value(self,fieldname:str,value:Any) -> Dataset:
        data_copy = self.get_data()
        temp_data = []

        for record in data_copy:
            if record[self.field[fieldname]] == value:
                temp_data.append(record)
        
        return_dataset = Dataset()
        return_dataset.set_data(temp_data)
        return_dataset.set_fields(self.get_fields())
        return_dataset.generate_fields_values()

        return return_dataset
    
    def copy(self):
        return_dataset = Dataset()
        return_dataset.set_data(self.get_data())
        return_dataset.set_fields(self.get_fields())
        return_dataset.generate_fields_values()
        return return_dataset

if __name__=='__main__':
    test = Dataset('./DecisionTreeLearning/Data/ex1.csv')
    split_test = test.separate_by_value('PlayTennis','No')
    print(split_test.get_data())
    split_test_2 = split_test.separate_by_value('Outlook','Rain')
    print(split_test_2.get_data())