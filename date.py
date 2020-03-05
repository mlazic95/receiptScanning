import behaviour_tree as bt
import prediction
import re
import util
from dateutil.parser import parse


dateFormats = [
    r'[0-9]{4}[-|.|\s|\\|/][0-9]{2}[-|.|\s|\\|/][0-9]{2}',
    r'[0-9]{2}[-|.|\s|\\|/][0-9]{2}[-|.|\s|\\|/][0-9]{4}',
    r'[0-9]{2}[-][0-9]{2}[-][0-9]{2}'
    ]

class Date(prediction.Prediction):
    def __init__(self, rawText, lines):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._result = None

    def generate_tree(self):
        tree = bt.FallBack()

        firstMatch = bt.Sequence()
        checkFirstMatch = self.FirstMatch(self)
        takeFirstMatch = self.TakeFirstMatch(self)

        firstMatch.add_child(checkFirstMatch)
        firstMatch.add_child(takeFirstMatch)

        secondMatch = bt.Sequence()
        checkSecondMatch = self.SecondMatch(self)
        takeSecondMatch = self.TakeSecondMatch(self)

        secondMatch.add_child(checkSecondMatch)
        secondMatch.add_child(takeSecondMatch)

        naiveTake = self.NaiveTake(self)
        tree.add_child(firstMatch)
        tree.add_child(secondMatch)
        tree.add_child(naiveTake)
        return tree


    class FirstMatch(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            m = re.findall(r'[0-9]{4}[-|.|\\][0-9]{2}[-|.|\\][0-9]{2}', text)
            return m != None

    class TakeFirstMatch(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            m = re.findall(r'[0-9]{4}[-|.|\\][0-9]{2}[-|.|\\][0-9]{2}', text)
            if m:
                self.__outer._result = m[0]
                self._status = bt.Status.SUCCESS
                return
            self._status = bt.Status.FAIL

    class SecondMatch(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            for month in util.months:
                m = re.findall(r'[0-9]{2}\s?' + month + r'\s?[\']?[0-9]{2}', text, flags=re.IGNORECASE)
            return m != None

    class TakeSecondMatch(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            for month in util.months:
                m = re.findall(r'[0-9]{2}\s?' + month + r'\s?[\']?\s?[0-9]{2}', text, flags=re.IGNORECASE)
                if m:
                    self.__outer._result = m[0]
                    self._status = bt.Status.SUCCESS
                    return
            self._status = bt.Status.FAIL


    class NaiveTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            for f in dateFormats:
                m = re.findall(f, text)
                if m:
                    self.__outer._result = m[0]
                    self._status = bt.Status.SUCCESS
                    return
            m = re.findall(r'\b[0-9]{6}\b', text)
            if m:
                for match in m:
                    try:
                        for b in [True, False]:
                            _ = parse(match, yearfirst=b)
                            self.__outer._result = match
                            self._status = bt.Status.SUCCESS
                            return
                    except:
                        continue
            m = re.findall(r'\b[0-9]{8}\b', text)
            if m:
                for match in m:
                    try:
                        for b in [True, False]:
                            _ = parse(match, yearfirst=b)
                            self.__outer._result = match
                            self._status = bt.Status.SUCCESS
                            return
                    except:
                        continue

            
            self._status = bt.Status.FAIL
            