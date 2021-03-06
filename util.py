import math
import text_processor as tx
import string
import re
import copy
import pandas as pd

currencyList = ['SEK', 'DKK','CHF', 'EUR', 'USD', 'GBP', 'IDR']
months = ['jan', 'feb', 'mar', 'apr', 'maj', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'okt']
totalKeywords = ['total', 'belopp', 'summa', 'betala', 'tot', 'kontokort', 'amount', 'net ']
vowels = ['a', 'e', 'i', 'o', 'u']
cities = ['stockholm','nacka','singapore', 'sppsala', 'engelberg', 'kobenhavn', 'danderyd', 'sundbyberg', 'copenhagen', 'skarholmen', 'johanneshov', 'solna', 'malmo', 'vasteras', 'norsborg', 'ronninge', 'hagersten', 'arsta', 'tyresa', 'farsta', 'varby', 'london', 'tignes']
countries = ['sweden']

def area(wordBox):
    x1 = float(wordBox["topLeft"][1:].split(',')[0])
    y1 = float(wordBox["topLeft"][:-1].split(',')[1])
    x2 = float(wordBox["bottomLeft"][1:].split(',')[0])
    y2 = float(wordBox["bottomLeft"][:-1].split(',')[1])
    x3 = float(wordBox["topRight"][1:].split(',')[0])
    y3 = float(wordBox["topRight"][:-1].split(',')[1])

    return pointDistance(x1,y1,x2,y2) * pointDistance(x1,y1,x3,y3)

def height(wordBox):
    y1 = float(wordBox["topLeft"][:-1].split(',')[1])
    y2 = float(wordBox["bottomLeft"][:-1].split(',')[1])

    return y1-y2

def isPriceFormat(s, onlyFloats=False):
    s = s.lower()
    replace = [(',', '.'), ('kr', '')]
    for r in replace:
        s = s.replace(r[0], r[1])
    try:
        i = int(s)
        return i < 99999 and not onlyFloats
    except:
        try:
            float(s)
            return True
        except:
            return False

    return False

def findLongestConsecutive(l):
    if len(l) == 0:
        return None
    if len(l) == 1:
        return (l[0],l[0])
    longest = (0, 0)
    current = (0, -1)
    for t in l:
        if t ==  current[1] + 1:
            current = (current[0],t)
            continue
        elif current[1] - current[0] >= longest[1] - longest[0]:
            longest = current
        current = (t,t)

    if current[1] - current[0] >= longest[1] - longest[0]:
        longest = current
    return longest

def floatCompare(f1, f2):
    if f1 == f2:
        return True
    if not f1 or not f2:
        return False
    return abs(f1-f2) <= 0.009

def getPriceFromLine(line):
    rawLine = ''
    for word in line:
        rawLine += word['text'] + ' '
    rawLine = rawLine[:-1]
    m = re.findall(r'[\d]\s?[0-9]+[\.|,]?[0-9]*', rawLine)
    m1 = re.findall(r'[\d],[0-9]+[\.|,]?[0-9]*', rawLine)
    m+=m1
    biggest = 0
    if m:
        for match in m:
            res = re.sub(r'\s', '', match)
            res = re.sub(r',', '.', res)
            if res.count('.') > 1:
                res = re.sub(r'\.', '', res, 1)
            res = float(res)
            if res > biggest:
                biggest = res
        if biggest > 0:
            return biggest
    return None

def neighbourContains(wordBox, s):
    s = s.lower()
    if 'bottom' in wordBox and s in wordBox['bottom']['text'].lower():
        return True
    #if 'top' in wordBox and  s in wordBox['top']['text'].lower():
        #return True
    if 'left' in wordBox and  s in wordBox['left']['text'].lower():
        return True
    if 'right' in wordBox and  s in wordBox['right']['text'].lower():
        return True
    return False

def stringInLine(line, s):
    s = s.lower()
    for word in line:
        if s in word['text'].lower():
            return True
    return False

def rolling_mean(data, axis=0):
    return data.rolling(4).mean(axis=axis)

def alphaRatio(s):
    alpha = 0.0
    for c in s:
        if c.isalpha():
            alpha+=1
    if alpha == 0:
        return 0 
    return alpha/len(s)

def pointDistance(x1,y1,x2,y2):
    return math.sqrt((x1 - x2)**2+(y1 - y2)**2)

def boxDistance(b1, b2):
    return math.sqrt((b1['center'][0] - b2['center'][0])**2+(b1['center'][1] - b2['center'][1])**2)

def fourInARow(s):
    s = s.lower()
    if len(s) < 3:
        return False
    start = s[0]
    count = 1
    for curr in s[1:]:
        if curr == start:
            count+=1
        else:
            count = 1
        if count == 4:
            return True
        start = curr
    return False

def isInt(s):
    try:
        s = int(s)
        return True
    except:
        return False

def isFloat(s):
    s = s.replace(',', '.')
    try:
        s = float(s)
        return True
    except:
        return False

def vowelRatio(s):
    s = s.lower()
    count = 0.0
    for w in s:
        if w in vowels:
            count+=1
    if count == 0:
        return 0
    return count/len(s)

def dubblePunctuation(s):
    punctuations = set()
    for w in s:
        if w in string.punctuation:
            punctuations.add(w)
    return len(punctuations) > 1


def alphaNumericRatio(s, includeSpace=False):
    alnum = 0.0
    for c in s:
        if c.isalnum() or (includeSpace and c == " "):
            alnum+=1
    if alnum == 0:
        return 0 
    return alnum/len(s)

def getTopNeighbour(word, words):
    best = (1, None)
    for other in words:
        if word == other:
            continue
        if word['center'][1] < other['center'][1] and tx.verticalOverlap(word, other) > 0:
            dist = boxDistance(word, other)
            if dist < best[0]:
                best = (dist, other)
    return best

def getBottomNeighbour(word, words):
    best = (1, None)
    for other in words:
        if word == other:
            continue
        if word['center'][1] > other['center'][1] and tx.verticalOverlap(word, other) > 0:
            dist = boxDistance(word, other)
            if dist < best[0]:
                best = (dist, other)
    return best

def getRightNeighbour(word, words):
    best = (1, None)
    for other in words:
        if word == other:
            continue
        if word['center'][0] < other['center'][0] and tx.horizontalOverlap(word, other) > 0:
            dist = boxDistance(word, other)
            if dist < best[0]:
                best = (dist, other)
    return best

def getLeftNeighbour(word, words):
    best = (1, None)
    for other in words:
        if word == other:
            continue
        if word['center'][0] > other['center'][0] and tx.horizontalOverlap(word, other) > 0:
            dist = boxDistance(word, other)
            if dist < best[0]:
                best = (dist, other)
    return best

def getLineForWord(word, lines):
    for i,line in enumerate(lines):
        if word in line:
            return i, line
    return None

def breakTextBox(box):
    boxes = []
    text = box['text']
    l = len(text)
    start = float(box["topLeft"][1:].split(',')[0])
    end = float(box["topRight"][1:].split(',')[0])
    width = end - start
    unitSize = width / l
    words = text.split(' ')
    breakPoints = [i for i in range(len(text)) if text[i] == ' ']
    breakPointsStarts = [i * unitSize + start for i in breakPoints]
    breakPointsStarts.append(end)
    breakPointsStarts.reverse()
    for word in words:
        if word == '' or word == ' ':
            continue
        new_box = copy.deepcopy(box)
        t_start = start
        t_end = breakPointsStarts.pop()
        new_box['center'] = ((t_start + t_end / 2), box['center'][1])
        new_box['text'] = word
        boxes.append(new_box)
        start = (t_end + unitSize)
    return boxes

def getClassInt(c):
    if c == 'vendor':
        return 1
    elif c == 'total_price':
        return 2
    elif c == 'date':
        return 3
    elif c == 'address':
        return 4
    elif c == 'tax_rate':
        return 5
    elif c == 'currency':
        return 6
    elif c == 'product_name':
        return 7
    elif c == 'product_price':
        return 8
    elif c == 'product_amount':
        return 9
    return 0


def precision(relevant, retrieved):
    if retrieved == 0:
        return 0
    return relevant / retrieved

def recall(relevant, retrieved):
    if relevant == 0:
        return 0
    return retrieved / relevant

def fScore(prec, rec):
    if prec == 0 and rec == 0:
        return 0
    return 2*(prec * rec) / (prec + rec)

def create_data_statistics(receipts, className):
    class_dict = {}
    for receipt in receipts:
        truth = receipt.groundTruth
        if className in truth:
            t_class = truth[className].lower()
            if t_class in class_dict:
                class_dict[t_class] +=1
            else:
                class_dict[t_class] = 1
    return class_dict