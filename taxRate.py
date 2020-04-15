import behaviour_tree as bt
import prediction
import re
import util

class TaxRate(prediction.Prediction):
    def __init__(self, rawText, lines, graph, words):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._graph = graph
        self._result = None
        self._words = words

    def generate_tree(self):
        tree = bt.FallBack()

        first_sequence = bt.Sequence()
        regular_format_match = self.RegularFormat(self)
        find_keyword = self.FindKeywordFirst(self)
        first_sequence.add_child(regular_format_match)
        first_sequence.add_child(find_keyword)

        tree.add_child(first_sequence)

        second_sequence = bt.Sequence()
        regular_format_match = self.NoPercentage(self)
        find_keyword = self.FindKeywordSecond(self)
        second_sequence.add_child(regular_format_match)
        second_sequence.add_child(find_keyword)

        tree.add_child(second_sequence)
        return tree

    class RegularFormat(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            m = re.findall(r'\b[0-9]+[.|,]?[0-9]+%\s?', self.__outer._rawText)
            return m != None


    class NoPercentage(bt.Condition):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def condition(self):
            m = re.findall(r'[0-9]{1,2}[.|,]?[0-9]+?', self.__outer._rawText)
            return m != None

    class FindKeywordFirst(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            m = re.findall(r'[0-9]+[.|,]?[0-9]+\s?%', self.__outer._rawText)
            if m:
                for i, match in enumerate(m):
                    for line in self.__outer._lines:
                        for word in line:
                            if match in word['text']:
                                temp = re.sub(r'%', '', match)
                                temp = re.sub(r',', '.', temp)
                                if util.stringInLine(line, 'Moms') and float(temp) < 30.0:
                                    #print([t['text'] for t in line])
                                    self.__outer._result = m[i]
                                    self._status = bt.Status.SUCCESS
                                    return
                    for elem in self.__outer._words:
                        if match in elem['text']:
                            temp = re.sub(r'%', '', match)
                            temp = re.sub(r',', '.', temp)
                            #if util.neighbourContains(self.__outer._graph[elem['id']], 'Moms') and float(temp) < 30.0:
                                #self.__outer._result = m[i]
                                #self._status = bt.Status.SUCCESS
                                #return
                for match in m:
                    match = re.sub(r'%', '', match)
                    match = re.sub(r',', '.', match)
                    if float(match) == 12.0 or float(match) == 25.0:
                        self.__outer._result = match
                        self._status = bt.Status.SUCCESS
                        return
                self.__outer._result = m[0]
                self._status = bt.Status.FAIL
            else:
                self._status = bt.Status.FAIL


    class FindKeywordSecond(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            m = re.findall(r'[0-9]{1,2}[.|,]?[0-9]+', self.__outer._rawText)
            if m:
                for i, match in enumerate(m):
                    for line in self.__outer._lines:
                        for word in line:
                            if match in word['text']:
                                temp = re.sub(r',', '.', match)
                                if util.stringInLine(line, 'Moms') and float(temp) < 30.0:
                                    self.__outer._result = m[i]
                                    self._status = bt.Status.SUCCESS
                                    return
                    for elem in self.__outer._words:
                        if match in elem['text']:
                            temp = re.sub(r',', '.', match)
                            #if util.neighbourContains(self.__outer._graph[elem['id']], 'Moms') and float(temp) < 30.0:
                                #self.__outer._result = m[i]
                                #self._status = bt.Status.SUCCESS
                                #return
                for match in m:
                    match = re.sub(r'%', '', match)
                    match = re.sub(r',', '.', match)
                    if float(match) == 12.0 or float(match) == 25.0:
                        self.__outer._result = match
                        self._status = bt.Status.SUCCESS
                        return
                self.__outer._result = m[0]
                self._status = bt.Status.SUCCESS
            else:
                self._status = bt.Status.FAIL