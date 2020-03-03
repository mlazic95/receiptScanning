import behaviour_tree as bt
import prediction
import re
import util

class Date(prediction.Prediction):
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
            m = re.findall(r'[0-9]{4}[-|.|\s|\\][0-9]{2}[-|.|\s|\\][0-9]{2}', text)
            if m:
                self.__outer._result = m[0]
                self._status = bt.Status.SUCCESS
                return
            m = re.findall(r'[0-9]{2}[-|.|\s|\\][0-9]{2}[-|.|\s|\\][0-9]{4}', text)
            if m:
                self.__outer._result = m[0]
                self._status = bt.Status.SUCCESS
                return
            for month in util.months:
                m = re.findall(r'[0-9]{2}\s?' + month + r'\s?[\']?[0-9]{2}', text, flags=re.IGNORECASE)
                if m:
                    self.__outer._result = m[0]
                    self._status = bt.Status.SUCCESS
                    return
            self._status = bt.Status.FAIL
            