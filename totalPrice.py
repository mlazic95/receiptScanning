import behaviour_tree as bt
import prediction

class TotalPrice(prediction.Prediction):
    def __init__(self, rawText, lines):
        super().__init__()
        self._rawText = rawText
        self._lines = lines
        self._result = None

    def generate_tree(self):
        tree = bt.Sequence()
        take_first = self.TakeFirst(self)
        tree.add_child(take_first)
        return tree

    class TakeFirst(bt.Action):
        def __init__(self, outer):
            super().__init__()
            self.__outer = outer

        def action(self):
            self.__outer._result = self.__outer._lines[0][0]['text']   
            self._status = bt.Status.SUCCESS