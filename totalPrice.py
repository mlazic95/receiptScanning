import behaviour_tree as bt
import prediction
import re

class TotalPrice(prediction.Prediction):
    def __init__(self, rawText, lines):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
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
            m = re.findall(r'[0-9]+\.[0-9]{2}', text)
            if m:
                biggest = 0
                for potential_price in m:
                    try:
                        potential_price = float(potential_price)
                        if potential_price > biggest:
                            biggest = potential_price
                    except:
                        continue
                if biggest > 0:
                    self.__outer._result = biggest
                    self._status = bt.Status.SUCCESS
                    return 
            m = re.findall(r'(?<=TOTAL\s)(\w+)', text)
            if m:
                self.__outer._result = m[0]  
                self._status = bt.Status.SUCCESS
                return
            self._status = bt.Status.FAIL
            