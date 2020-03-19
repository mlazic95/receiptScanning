from Levenshtein import distance as levenshtein_distance
import util
import numpy
from string import ascii_uppercase, digits, punctuation
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
from transformers import BertTokenizer
import string

VOCAB = ascii_uppercase + digits + punctuation + " \t\n"
windowSizeOffsets = [-2, -1, 0, 1, 2]

def generateWordClasses(reciept, correcting=False):
  raw = reciept.rawText
  keys = reciept.groundTruth.keys()
  foundLabels = []
  spans = []
  index = 0
  for key in keys:
    if key == 'products':
      continue
    label = reciept.groundTruth[key]
    text = []
    for offset in windowSizeOffsets:
      l = len(label) + offset
      for i in range(0, len(raw) - l):
        text.append(raw[i:i+l])
    extracted = process.extractOne(label, text)
    t = extracted[0]
    if extracted[1] < 75:
      continue
    if label != t and correcting and key != 'tax_rate':
      specials = ['(', ')', '.', '*','/']
      for spec in specials:
        if spec in t:
          t = t.replace(spec, '\\' + spec)
      try:
        raw = re.sub(t, label, raw)
      except:
        print(raw)
        print(t)
        print(label)
        return
      t = label
    foundLabels.append((t, key))
    for offset in windowSizeOffsets:
      l = len(label) + offset
      for i in range(0, len(raw) - l):
        sub = raw[i:i+l]
        if sub == t:
          spans.append((i, i+l, index))
    index +=1

  words = []
  previous = 0
  for i in range(len(raw)):
    for span in spans:
      if i == span[0]:
        words.append((raw[previous:span[0]],'O'))
        words.append((raw[span[0]:span[1]], foundLabels[span[2]][1]))
        previous = span[1]
  textResult = []
  labelsResult = []
  for w in words:
    label = w[1]
    temp = w[0].split(' ')
    for t in temp:
      if t == ' ' or t == '':
        continue
      textResult.append(t)
      labelsResult.append(label)

  reciept.dataWords = textResult
  reciept.dataLabels = labelsResult
  return (textResult, labelsResult)

def createVocabulary(reciepts):
  vocab = set()
  for reciept in reciepts:
    words = reciept.dataWords
    for word in words:
      vocab.add(word)
  '''
  path = './data/new_vocab.txt'
  with open(path, 'r') as f:
    for line in f:
      vocab.add(line[:-1])
  tokenizer=BertTokenizer(vocab_file=path,do_lower_case=False)
  new_set = set()
  for word in vocab:
    token_list = tokenizer.tokenize(word)
    if '[UNK]' in token_list:
      print(word)
      t = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', word)
      for i, v in enumerate(token_list):
        if v == '[UNK]' and i < len(t):
          for x in t:
            new_set.add(x)
  with open('./data/new_vocab.txt', 'w+') as f:
    for word in (vocab.union(new_set)):
      f.write(word  + '\n')
  '''
  return vocab


def generateCharClasses(reciept, includeProducts=False):
    raw = reciept.rawText
    text = ''
    for c in raw:
      if c in VOCAB:
        text+=c
    classes = numpy.zeros(len(text), dtype=int)
    keys = reciept.groundTruth.keys()
    for key in keys:
      if key == 'products' and not includeProducts:
          continue
      classValue = reciept.groundTruth[key]
      l = len(classValue)
      minDist = l
      start = 0
      for i in range(len(text) - l):
        sub = text[i:i+l]
        dist = levenshtein_distance(sub, classValue)
        if dist < minDist:
          minDist = dist
          start = i
      for i in range(start, start + len(classValue)):
        classes[i] = util.getClassInt(key)
     
    return (text, classes)



