import behaviour_tree as bt
import prediction
import re
import util


formats = [
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{3}\s[0-9]{2},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{5},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?-[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{3}\s[0-9]{2},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?-[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{5},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?SE?-\s?[0-9]{3}?\s[0-9]{2},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?SE?-\s?[0-9]{5},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{3}\s[0-9]{2}',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{5}',
    r'[^,|.|\n]*\b[\w]*\b[a-zA-Z]?,?\s\n?\s?SE?-\s?[0-9]{3}?\s[0-9]{2},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b[a-zA-Z]?,?\s\n?\s?\s?[0-9]{3}?\s[0-9]{2},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b[a-zA-Z]?,?\s\n?\s?\s?[0-9]{5},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b[a-zA-Z]?,?\s\n?\s?\s?[0-9]{4},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?,?\s\n?\s?[0-9]{2}\s[0-9]{3},?\s\b[\w]*\b',
    r'[^,|.|\n]*\b[\w]*\b\s[0-9]+[a-zA-Z]?\s\b[\w]*\b'
    ]

class Address(prediction.Prediction):
    def __init__(self, rawText):
        super().__init__()
        self._rawText = rawText
        self._result = None

    def generate_tree(self):
        tree = bt.FallBack()

        specialCase = bt.Sequence()
        specalCaseCheck = self.SpecialCaseCheck(self)
        specalCaseTake = self.SpecialCaseTake(self)
        specialCase.add_child(specalCaseCheck)
        specialCase.add_child(specalCaseTake)

        formatCase = bt.Sequence()
        formatCheck = self.FormatsCheck(self)
        formatTake = self.FormatsTake(self)
        formatCase.add_child(formatCheck)
        formatCase.add_child(formatTake)

        tree.add_child(specialCase)
        tree.add_child(formatCase)
        return tree

    
    class SpecialCaseCheck(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            m = re.findall(r'\b[\w]*\b - \b[\w]*\b [\d]{1,5}', text)
            for match in m:
                m1 = re.findall(r'gata', match.lower())
                if m1:
                    return True
            return False

    class SpecialCaseTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            m = re.findall(r'\b[\w]*\b - \b[\w]*\b [\d]{1,5}', text)
            for match in m:
                m1 = re.findall(r'gata', match.lower())
                if m1:
                    tmp = re.sub(r'\n', '', match)
                    self.__outer._result = tmp 
                    self._status = bt.Status.SUCCESS
                    return
            self._status = bt.Status.FAIL

    class FormatsCheck(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            for f in formats:
                m = re.findall(f, text, flags=re.UNICODE)
                if m:
                    return True
            return False

    class FormatsTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            for f in formats:
                m = re.findall(f, text, flags=re.UNICODE)
                if m:
                    tmp = re.sub(r'\n', '', m[0])
                    if util.alphaRatio(tmp) > 0.5:
                        self.__outer._result = tmp 
                        self._status = bt.Status.SUCCESS
                        return
            self._status = bt.Status.FAIL
            