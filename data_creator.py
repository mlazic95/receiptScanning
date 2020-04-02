from date_generator import getRandomDate
from price_generator import getRandomPrice
from address_generator import AddressGenerator
from vendor_generator import VendorGenerator
from products_generator import ProductsGenerator
import random
import copy

def generateSintheticData(receipts, number):
  synthetic_receipts = []
  address_generator = AddressGenerator()
  vendor_generator = VendorGenerator(receipts)
  products_generator = ProductsGenerator(receipts)
  for _ in range(number):
    synth = copy.deepcopy(random.choice(receipts))
    synth.path = 'synth'
    newDataWords = []
    newDataLabels = []
    index = 0
    new = {
      'vendor': vendor_generator.generateVendor(),
      'date': getRandomDate(),
      'price': getRandomPrice(),
      'address': address_generator.generateAddress()
      }
    for i, (w, l) in enumerate(zip(synth.dataWords, synth.dataLabels)):
      if i < index:
        continue
      if l == 'vendor' or l == 'date' or l == 'price' or l == 'address' or l =='product_name':
        if l == 'product_name':
          newDataPoint = products_generator.generateProducts()
        else:
          newDataPoint = new[l]
        for word in newDataPoint.split(' '):
          newDataWords.append(word)
          newDataLabels.append(l)
        index = i
        while index < len(synth.dataLabels) and synth.dataLabels[index] == l:
          index += 1
      else:
        newDataWords.append(w)
        newDataLabels.append(l)

    synth.dataLabel = newDataLabels
    synth.dataWords = newDataWords

    synthetic_receipts.append(synth)
  return synthetic_receipts