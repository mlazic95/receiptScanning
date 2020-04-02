import random
import numpy

def getRandomPrice():
  price = numpy.random.normal(100, 30,1)[0]
  if random.random() <= 0.6:
    p = str(int(price))
    if random.random() <= 0.5:
      p += '.00'
    return p
  return str(round(price,2))