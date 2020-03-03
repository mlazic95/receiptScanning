import behaviour_tree as bt
import prediction
import re

class TaxRate(prediction.Prediction):
    def __init__(self, rawText, lines):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._result = None

    def generate_tree(self):
        tree = bt.FallBack()

        first_sequence = bt.Sequence()
        regular_format_match = self.RegularFormat(self)
        find_keyword = self.FindKeyword(self)
        first_sequence.add_child(regular_format_match)
        first_sequence.add_child(find_keyword)

        tree.add_child(first_sequence)
        return tree

    class RegularFormat(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            m = re.findall(r'\b[0-9]+[.]?[0-9]+%\s?', self.__outer._rawText)
            return m != None

    class FindKeyword(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            m = re.findall(r'\b[0-9]+[.]?[0-9]+%\s?', self.__outer._rawText)
            if m:
                for match in m:
                    x = 1
                self.__outer._result = m[0]
                self._status = bt.Status.SUCCESS
            else:
                self._status = bt.Status.FAIL