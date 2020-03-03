import behaviour_tree as bt
import prediction
import re
import util

class Products(prediction.Prediction):
    def __init__(self, rawText):
        super().__init__()
        self._rawText = rawText
        self._result = None

    def generate_tree(self):
        tree = bt.Sequence()
        return tree


            