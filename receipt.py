from itertools import chain
import util

class Receipt:
    def __init__(self, lines, groundTruth):
        self.lines = lines
        self.groundTruth = groundTruth
        self.ruleBasedPrediction = {}
        self.rawText = self.concatinateText()
        self.words = list(chain.from_iterable(self.lines))
        self.graph = self.createGraph()
        self.linesText = self.concatinateText(perserveLines=True)
        self.dataWords = []
        self.dataLabels = []
    
    def concatinateText(self, perserveLines=False):
        text = ""
        for line in self.lines:
            for wordObject in line:
                text+=wordObject['text'] + " "
            if perserveLines:
                text+='\n'
        return text

    def createGraph(self):
        graph = {}
        for word in self.words:
            graph[word['id']] = {}
            lineIndex, line = util.getLineForWord(word, self.lines)
            ## Find neighbours
            top = util.getTopNeighbour(word, self.lines[lineIndex-1] if lineIndex > 0 else [])
            if top:
                graph[word['id']]['top'] = top
            
            bottom = util.getBottomNeighbour(word, self.lines[lineIndex+1] if lineIndex < len(self.lines) - 1 else [])
            if bottom:
                graph[word['id']]['bottom'] = bottom

            left = util.getLeftNeighbour(word, line)
            if left:
                graph[word['id']]['left'] = left
            
            right = util.getRightNeighbour(word, line)
            if right:
                graph[word['id']]['right'] = right
        return graph



                
