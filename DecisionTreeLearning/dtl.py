from typing import Any

from classes.dataset import Dataset
from tools import Gain
import tools

class DTL():
    dataset:Dataset = None
    tree:dict[Any,Any] = None
    label_fieldname:str = None
    explored_field:list[str] = None
    
    def __init__(self,dir:str=None,label_fieldname:str=None,dataset:Dataset=None,tree:dict[Any,Any]=None,explored_field:Any=None):
        if dir is not None:
            self.dataset = Dataset(dir)
            self.tree = {}
            self.explored_field = [str]
        else:
            self.dataset = dataset
            self.tree = tree
            self.explored_field = explored_field
        self.label_fieldname = label_fieldname

    def generate(self) -> dict[Any,Any] or str:
        # print(f'explore {len(self.explored_field)}')
        max_gain_value, max_gain_fieldname = -1, None
        # print(self.dataset.get_fields())
        for key in self.dataset.get_fields():
            if key == self.label_fieldname or key in self.explored_field:
                continue
            if Gain(self.dataset,self.label_fieldname,key) > max_gain_value:
                max_gain_value = Gain(self.dataset,self.label_fieldname,key)
                max_gain_fieldname = key
        
        # Find field value correlation with labels
        if max_gain_fieldname is not None:
            field_values = self.dataset.get_field_values(max_gain_fieldname)
            for value in field_values:
                leaf_node = False
                sub_dtl = self.copy()
                sub_dtl.add_explored_field(max_gain_fieldname)
                sub_dtl.select_sub_dataset(max_gain_fieldname,value)
                
                label_counter = {val:0 for val in self.dataset.get_field_values(self.label_fieldname)}
                for record in sub_dtl.get_dataset().get_data():
                    label_value = record[sub_dtl.get_dataset().get_fields()[sub_dtl.get_label_fieldname()]]
                    label_counter[label_value] += 1
                    if label_counter[label_value] == len(sub_dtl.get_dataset().get_data()):
                        self.tree[str(max_gain_fieldname+'-'+str(value))] =  str(label_value)
                        leaf_node = True
                        break
                
                if not leaf_node:
                    self.tree[str(max_gain_fieldname+'-'+str(value))] = sub_dtl.generate()
            
            return self.tree
    
    def copy(self):
        return DTL(dataset=self.get_dataset(),
                   tree=self.get_tree(),
                   label_fieldname=self.label_fieldname,
                   explored_field=self.get_explored_field())

    def set_label_fieldname(self,fieldname:str):
        self.label_fieldname = fieldname

    def get_label_fieldname(self):
        return self.label_fieldname
    
    def get_explored_field(self):
        return self.explored_field.copy()

    def get_dataset(self):
        return self.dataset.copy()

    def get_tree(self):
        return self.tree.copy()
    
    def add_explored_field(self,explored_field:Any):
        self.explored_field.append(explored_field)

    def select_sub_dataset(self,fieldname:str,value:Any):
        self.dataset = self.dataset.separate_by_value(fieldname,value)

    def print(self,sub_tree:dict or str=None,depth:int=1):
        if type(sub_tree) is str:
            print(f'{"-"*depth*2}>{sub_tree}')
        elif not sub_tree:
            for key in self.tree:
                print(f'{"-"*depth*2}>{key}')
                self.print(self.tree[key],depth+1)
        else:
            for key in sub_tree:
                print(f'{"-"*depth*2}>{key}')
                self.print(sub_tree[key],depth+1)
        