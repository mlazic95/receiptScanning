import behaviour_tree as bt
import prediction
import re
import util

keyWords = ['moms', 'betala', 'summa', 'total', 'sek', 'kontokort', 'Kontantuttag', 'belopp', 'mons', 'kortkop', 'rabatt', 'mastercard', 'tillbaka', 'vaxel']
class Products(prediction.Prediction):
    def __init__(self, rawText, lines, linesText):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._linesText = linesText
        self._result = []

    def generate_tree(self):
        tree = bt.Sequence()
        t = self.OneLine(self)
        tree.add_child(t)
        return tree

    class OneLine(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            lines = self.__outer._lines
            potental_lines = []
            for i, line in enumerate(lines):
                line = [t['text'] for t in line]
                hasPrice = False
                hasPotentitalProduct = False
                for word in line:
                    if util.isPriceFormat(word, onlyFloats=True) and '-' not in word:
                        hasPrice = True
                    else:
                        hasPotentitalProduct = True
                if hasPotentitalProduct and hasPrice:
                    lineText = ''.join(line)
                    containtsKey = False
                    for key in keyWords:
                        if key in lineText.lower():
                            containtsKey = True
                    potentialName = line[0]
                    if not containtsKey and util.alphaRatio(line[0]) >= 0.7:
                        potental_lines.append(i)
            longest = util.findLongestConsecutive(potental_lines)
            if not longest:
                self.__outer._result = []
                self._status = bt.Status.FAIL
                return
            receipts = []
            for i in range(longest[0], longest[1] + 1):
                line = [t['text'] for t in lines[i]]
                receipts.append({'name': line[0], 'price': line[-1], 'amount': 1})
            self.__outer._result = receipts
            self._status = bt.Status.SUCCESS


            