import behaviour_tree as bt
import prediction
import re
import util

class TotalPrice(prediction.Prediction):
    def __init__(self, rawText, lines):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._result = None

    def generate_tree(self):
        tree = bt.FallBack()

        SEKMatchBefore = bt.Sequence()
        SEKcheckBefore = self.CheckForSEKBefore(self)
        SEKBeforeTake= self.SEKBeforeTake(self)
        SEKMatchBefore.add_child(SEKcheckBefore)
        SEKMatchBefore.add_child(SEKBeforeTake)

        keywordMatch = bt.Sequence()
        checkKeywordRow = self.CheckKeywordRow(self)
        takeByKeywordRow = self.KeywordTakeRow(self)
        keywordMatch.add_child(checkKeywordRow)
        keywordMatch.add_child(takeByKeywordRow)

        SEKMatchAfter = bt.Sequence()
        SEKcheckAfter = self.CheckForSEKAfter(self)
        SEKAfterTake = self.SEKAfterTake(self)
        SEKMatchAfter.add_child(SEKcheckAfter)
        SEKMatchAfter.add_child(SEKAfterTake)
        
        naiveTake = self.NaiveTake(self)

        tree.add_child(SEKMatchBefore)
        tree.add_child(keywordMatch)
        tree.add_child(SEKMatchAfter)
        tree.add_child(naiveTake)
        return tree


    class CheckForSEKBefore(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            m = re.findall(r'SEK\s[\d]\s?[0-9]+[\.|,]?[0-9]*', text)
            return m!=None

    class SEKBeforeTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            m = re.findall(r'SEK\s[\d]\s?[0-9]+[\.|,]?[0-9]*', text)
            if m:
                biggest = 0
                for match in m:
                    res = re.sub(r'SEK\s', '', match)
                    res = re.sub(r'\s', '', res)
                    res = re.sub(r',', '.', res)
                    res = float(res)
                    if res > biggest:
                        biggest = res
                self.__outer._result = biggest
                self._status = bt.Status.SUCCESS
                return
            self._status = bt.Status.FAIL
            return

    class CheckKeywordRow(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            for keyword in util.totalKeywords:
                m = re.findall(r'' + keyword + r'', text, flags=re.IGNORECASE)
            return m!=None

    class KeywordTakeRow(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            lines = self.__outer._lines
            biggest = 0
            for keyword in util.totalKeywords:
                for line in lines:
                    for word in line:
                        if keyword in word['text'].lower():
                            price = util.getPriceFromLine(line)
                            if price and price > biggest:
                                biggest = price
            if biggest > 0:
                self.__outer._result = biggest
                self._status = bt.Status.SUCCESS
                return

            self._status = bt.Status.FAIL

    class NaiveTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            m = re.findall(r'\d\s?[0-9]+[\.|,][0-9]{2}', text)
            if m:
                biggest = 0
                for potential_price in m:
                    potential_price = re.sub(r',', '.', potential_price)
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
            self._status = bt.Status.FAIL


    class CheckForSEKAfter(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            text = self.__outer._rawText
            m = re.findall(r'[\d]\s?[0-9]+[\.|,]?[0-9]*\sSEK', text)
            return m!=None

    class SEKAfterTake(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            text = self.__outer._rawText
            m = re.findall(r'[\d]\s?[0-9]+[\.|,]?[0-9]*\sSEK', text)
            if m:
                biggest = 0
                for match in m:
                    res = re.sub(r'\sSEK', '', match)
                    res = re.sub(r'\s', '', res)
                    res = re.sub(r',', '.', res)
                    res = float(res)
                    if res > biggest:
                        biggest = res
                self.__outer._result = biggest
                self._status = bt.Status.SUCCESS
                return
            self._status = bt.Status.FAIL
            return
            