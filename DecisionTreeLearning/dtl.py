from typing import Any
from DecisionTreeLearning.classes.dataset import Dataset
import tools

class DTL():
    dataset:Dataset = None
    tree:dict[Any,Any] = None

    def __init__(self,dir:str):
        self.dataset = Dataset(dir)
    
    def generate(self) -> dict[Any,Any]:
        dataset_copy = self.dataset.copy()

        # Find max(gain)

        # Find field value correlation with labels

        # Return result



