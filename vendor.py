import behaviour_tree as bt
import prediction
from itertools import chain
import util

specials = ['(', ')', '#', '*', '!']


class Vendor(prediction.Prediction):
    def __init__(self, rawText, lines):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._result = None
        self._topIndex = 0

    def generate_tree(self):
        tree = bt.Sequence()

        checkTopWordFallback = bt.FallBack()
        checkFirstWord = self.CheckFirstWord(self)
        removeTopWord = self.RemoveTopWord(self)
        checkTopWordFallback.add_child(checkFirstWord)
        checkTopWordFallback.add_child(removeTopWord)

        takeTopWord = self.TakeTopWord(self)
        
        tree.add_child(checkTopWordFallback)
        tree.add_child(takeTopWord)
        return tree

    class TakeTopWord(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            topWord = list(chain.from_iterable(self.__outer._lines))[self.__outer._topIndex]
            self.__outer._result = topWord['text']
            self._status = bt.Status.SUCCESS


    class CheckFirstWord(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            firstWord = self.__outer._lines[0][0]['text']
            includeSpecial = False
            for special in specials:
                if special in firstWord:
                    includeSpecial = True
                    break
            return firstWord.lower() != 'kvitto' and not includeSpecial and util.alphaRatio(firstWord) > 0 and len(firstWord) > 2

    class RemoveTopWord(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            words = list(chain.from_iterable(self.__outer._lines))
            while True:
                topWord = words[self.__outer._topIndex]['text']
                includeSpecial = False
                for special in specials:
                    if special in topWord:
                        includeSpecial = True
                        break
                if topWord.lower() != 'kvitto' and not includeSpecial and util.alphaRatio(topWord) > 0 and len(topWord) > 2:
                    break
                else:
                    self.__outer._topIndex+=1

            self._status = bt.Status.SUCCESS