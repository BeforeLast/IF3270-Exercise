import csv
from typing import Any, List
class Dataset():
    def read_file(self, dir:str):
        self.data = []
        self.field = {}
        self.field_values = {}
        with open(dir,'r',newline='',encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            # Create temporary array
            temp = []
            for temp_v in reader:
                temp.append(temp_v)

            # Splitting field name with data
            for i in range(len(temp[0])):
                self.field[temp[0][i]] = i
                self.field_values[temp[0][i]] = []
                for j in range(1,len(temp)):
                    if temp[j][i] not in self.field_values[temp[0][i]]:
                        self.field_values[temp[0][i]].append(temp[j][i])
            for row in temp[1:]:
                self.data.append(row)

    def get_fields(self):
        return self.field

    def get_data(self):
        return self.data

    def get_field_values(self, fieldname:str) -> List:
        return self.field_values[fieldname]
    
    def get_specified_data(self,fieldname:str,value:Any) -> List:
        if fieldname is None or value is None:
            raise ValueError("fieldname or/and value required!")
        if fieldname and value:
            field_idx = self.field[fieldname]
            temp = []
            for record in self.data:
                if record[field_idx] == value:
                    temp.append(record)
            return temp