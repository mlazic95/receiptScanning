import behaviour_tree as bt
import prediction
import re
import util

class Address(prediction.Prediction):
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
            ## GASTRIKEGATAN 1 113 22 STOCHOLM type \p{L}*\s[0-9]+\s[0-9]{3}\s[0-9]{2}\s\p{L}*
            m = re.findall(r'\b[\w]*\b \b[\w]*\b \b[\w]*\b\s[0-9]+\s\n?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            m = re.findall(r'\b[\w]*\b \b[\w]*\b\s[0-9]+\s\n?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            m = re.findall(r'\b[\w]*\b\s[0-9]+\s\n?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            ## GASTRIKEGATAN 1 11322 STOCHOLM type \p{L}*\s[0-9]+\s[0-9]{3}\s[0-9]{2}\s\p{L}*
            m = re.findall(r'\b[\w]*\b \b[\w]*\b \b[\w]*\b\s[0-9]+\s[0-9]{5}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            m = re.findall(r'\b[\w]*\b \b[\w]*\b\s[0-9]+\s[0-9]{5}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            m = re.findall(r'\b[\w]*\b\s[0-9]+\s[0-9]{5}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            ## GASTRIKEGATAN 1 SE-113 22 STOCHOLM type \p{L}*\s[0-9]+\s[0-9]{3}\s[0-9]{2}\s\p{L}*
            m = re.findall(r'\b[\w]*\b\s[0-9]+\s[SE-]?\s?[0-9]{3}\s[0-9]{2}\s\b[\w]*\b', text, flags=re.UNICODE)
            if m:
                tmp = re.sub(r'\n', '', m[0])
                self.__outer._result = tmp 
                self._status = bt.Status.SUCCESS
                return
            self._status = bt.Status.FAIL
            