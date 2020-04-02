import os
#from bpemb import BPEmb
from dateutil.parser import parse
import util

#multibpemb = BPEmb(lang="multi", vs=1000000, dim=300)

folderPath = '/Users/markolazic/Desktop/exjobb/project/data/gcn'
maxDate = parse('2020-03-15')
minDate = parse('2005-01-01')

def create(receipts, testFilePaths):
  for receipt in receipts:
    receipt.filterWordsForGraph()
    receipt.createGraph()
    graph = receipt.graph
    if receipt.path in testFilePaths:
      if not os.path.exists(os.path.join(folderPath, 'test', receipt.path)):
        os.makedirs(os.path.join(folderPath,'test', receipt.path))
      with open(os.path.join(folderPath,'test', receipt.path, receipt.path + '.connections'), "w") as f:
        for key in graph.keys():
          t_id = str(key)
          for neighbourKey in graph[key]:
            other_id = str(graph[key][neighbourKey]['id'])
            f.write(t_id+ ' ' + other_id + '\n')
      with open(os.path.join(folderPath,'test', receipt.path, receipt.path + '.values'), "w") as f:
        for word in receipt.graphWords:
          t_id = str(word['id'])
          t_value = word['text']
          #print(feature_creation(t_value))
          t_label = word['label']
          if t_label == 'date':
            print(t_value, isDate(t_value))
          f.write(t_id + ' ' + t_value + ' ' + t_label + '\n')
        
    else:
      if not os.path.exists(os.path.join(folderPath,'train', receipt.path)):
        os.makedirs(os.path.join(folderPath,'train', receipt.path))
      with open(os.path.join(folderPath,'train', receipt.path, receipt.path + '.connections'), "w") as f:
        for key in graph.keys():
          t_id = str(key)
          for neighbourKey in graph[key]:
            other_id = str(graph[key][neighbourKey]['id'])
            f.write(t_id+ ' ' + other_id + '\n')
      with open(os.path.join(folderPath,'train', receipt.path, receipt.path + '.values'), "w") as f:
        for word in receipt.graphWords:
          t_id = str(word['id'])
          t_value = word['text']
          #print(feature_creation(t_value))
          t_label = word['label']
          if t_label == 'date':
            print(t_value, isDate(t_value))
          else:
            if isDate(t_value):
              print(t_value, parse(t_value))
          f.write(t_id + ' ' + t_value + ' ' + t_label + '\n')
  return 0

def feature_creation(word):
  features = []
  features.append(1 if isDate(word) else 0)
  return 0
  #return multibpemb.embed(word)

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
  return False

def isCurrency(word):
  return word.upper() in util.currencyList
