import os
from bpemb import BPEmb
from dateutil.parser import parse
import util

multibpemb = BPEmb(lang="multi", vs=1000000, dim=300)

folderPath = '/Users/markolazic/Desktop/exjobb/project/data/gcn'
maxDate = parse('2020-03-15')
minDate = parse('2005-01-01')

def create(receipts, testFilePaths):
  testIndex = 0
  trainIndex = 0
  for receipt in receipts:
    receipt.filterWordsForGraph()
    receipt.createGraph()
    graph = receipt.graph
    if receipt.path in testFilePaths:
      with open(os.path.join(folderPath,'test', 'test'+ str(testIndex) + '.connections'), "w") as f:
        for key in graph.keys():
          t_id = str(key)
          for neighbourKey in graph[key]:
            other_id = str(graph[key][neighbourKey][1]['id'])
            f.write(t_id+ ' ' + other_id + '\n')
      with open(os.path.join(folderPath,'test', 'test' + str(testIndex) + '.values'), "w") as f:
        for word in receipt.graphWords:
          t_id = str(word['id'])
          t_value = word['text']
          t_features = feature_creation(t_value) + getNeighboursDistances(graph[int(t_id)]) 
          features = ' '.join([str(x) for x in t_features])
          t_label = word['label']
          f.write(t_id + ' ' + features + ' ' + t_label + '\n')
      testIndex+=1
        
    else:
      with open(os.path.join(folderPath,'train', 'train' + str(trainIndex) + '.connections'), "w") as f:
        for key in graph.keys():
          t_id = str(key)
          for neighbourKey in graph[key]:
            other_id = str(graph[key][neighbourKey][1]['id'])
            f.write(t_id+ ' ' + other_id + '\n')
      with open(os.path.join(folderPath,'train', 'train' + str(trainIndex) + '.values'), "w") as f:
        for word in receipt.graphWords:
          t_id = str(word['id'])
          t_value = word['text']
          t_features = feature_creation(t_value) + getNeighboursDistances(graph[int(t_id)]) 
          features = ' '.join([str(x) for x in t_features])
          t_label = word['label']
          f.write(t_id + ' ' + features + ' ' + t_label + '\n')
      trainIndex +=1
  return 0

def feature_creation(word):
  features = []
  features.append(1 if isDate(word) else 0)
  features.append(1 if isCity(word) else 0)
  features.append(1 if isCurrency(word) else 0)
  features.append(1 if isCountry(word) else 0)
  features.append(1 if isAlphabetic(word) else 0)
  features.append(1 if isNumeric(word) else 0)
  features.append(1 if isAlphaNumeric(word) else 0)
  features.append(1 if isNumberwithDecimal(word) else 0)
  for v in multibpemb.embed(word)[0]:
    features.append(v)
  return features

def isDate(word):
  if len(word) < 3 or util.isPriceFormat(word) or ':' in word or word.count('-') == 1 or word.count('/') == 1 or 'st' in word:
    return False
  try:
    date = parse(word)
    if date < minDate or date > maxDate:
      return False
    return True
  except:
    return False

def isCity(word):
  return word.lower() in util.cities

def isCountry(word):
  return word.lower() in util.countries

def isAlphabetic(word):
  for c in word:
    if not c.isalpha():
      return False
  return True

def isNumeric(word):
  for c in word:
    if not c.isdigit():
      return False
  return True

def isAlphaNumeric(word):
  for c in word:
    if not c.isdigit() and not c.isalpha():
      return False
  return True

def isNumberwithDecimal(word):
  return util.isPriceFormat(word, onlyFloats=True)

def isCurrency(word):
  return word.upper() in util.currencyList

def getNeighboursDistances(neighbours):
  RDt = 1
  RDl = 1
  RDr = 1
  RDb = 1
  if 'top' in neighbours:
    RDt = neighbours['top'][0]
  if 'left' in neighbours:
    RDl = neighbours['left'][0]
  if 'right' in neighbours:
    RDr = -neighbours['right'][0]
  if 'bottom' in neighbours:
    RDb = -neighbours['bottom'][0]
  return [RDt, RDl, RDr, RDb]
