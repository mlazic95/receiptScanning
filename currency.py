import behaviour_tree as bt
import prediction
import re
import util

class Currency(prediction.Prediction):
    def __init__(self, rawText):
        super().__init__()
        self._rawText = rawText
        self._result = None

    def generate_tree(self):
        tree = bt.Sequence()
        naiveTake = self.NaiveTake(self)
        tree.add_child(naiveTake)
        return tree

    class NaiveTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            for currency in util.currencyList:
                m = re.findall(r"\b" + currency  + r"\b", text)
                if m:
                    self.__outer._result = m[0]  
                    self._status = bt.Status.SUCCESS
                    return
            for currency in util.currencyList:
                m = re.findall(currency, text)
                if m:
                    self.__outer._result = m[0]  
                    self._status = bt.Status.SUCCESS
                    return
            self._status = bt.Status.FAIL
            