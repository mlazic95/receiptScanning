from abc import ABC, abstractmethod

class Prediction(ABC):
    
    def __init__(self):
        self._tree = self.generate_tree()

    @abstractmethod
    def generate_tree(self):
        pass

    def run(self):
        return self._tree.run()