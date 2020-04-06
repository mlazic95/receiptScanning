from itertools import chain
import util
import copy

class Receipt:
    def __init__(self, path, lines, groundTruth):
        self.path = path
        self.lines = lines
        self.groundTruth = groundTruth
        self.ruleBasedPrediction = {}
        self.rawText = self.concatinateText()
        self.words = self.createIndexedWordList(lines)
        self.sepWords = self.createIndexedWordList(lines, breakWords=True)
        #self.graph = self.createGraph()
        self.linesText = self.concatinateText(perserveLines=True)
        self.dataWords = []
        self.dataLabels = []

    def createIndexedWordList(self, lines, breakWords=False):
        words = []
        for i, line in enumerate(lines):
            for word in line:
                if breakWords:
                    breaked = word['text'].split(' ')
                    if len(breaked) > 1:
                        breaked = util.breakTextBox(word)
                        for subWord in breaked:
                            words.append(subWord)
                    else:
                        word['line'] = i
                        words.append(word)
                else:
                    word['line'] = i
                    words.append(word)
        for i, word in enumerate(words):
            word['id'] = i
        return words
    
    def concatinateText(self, perserveLines=False):
        text = ""
        for line in self.lines:
            for wordObject in line:
                text+=wordObject['text'] + " "
            if perserveLines:
                text+='\n'
        return text

    def filterWordsForGraph(self):
        words = []
        lastFound = 0
        finalWords = self.dataWords
        for i in range(len(finalWords)):
            for j in range(lastFound, len(self.sepWords)):
                if finalWords[i] == self.sepWords[j]['text']:
                    self.sepWords[j]['label'] = self.dataLabels[i]
                    words.append(self.sepWords[j])
                    lastFound = j + 1
                    break

        self.graphWords = words

    def createGraph(self):
        graph = {}
        for word in self.graphWords:
            graph[word['id']] = {}
            lineIndex = word['line']
            line = [w for w in self.graphWords if w['line'] == lineIndex]
            #print(word['text'])
            #print([t['text'] for t in line])
            previusLine = [w for w in self.graphWords if w['line'] == lineIndex - 1]
            nextLine = [w for w in self.graphWords if w['line'] == lineIndex + 1]
            ## Find neighbours
            top = util.getTopNeighbour(word, previusLine)
            if top[1]:
                graph[word['id']]['top'] = top
            
            bottom = util.getBottomNeighbour(word, nextLine)
            if bottom[1]:
                graph[word['id']]['bottom'] = bottom

            left = util.getLeftNeighbour(word, line)
            if left[1]:
                graph[word['id']]['left'] = left
            
            right = util.getRightNeighbour(word, line)
            if right[1]:
                graph[word['id']]['right'] = right
        self.graph = graph



                
