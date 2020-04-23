import util
import json
import os
from Levenshtein import distance as levenshtein_distance

def extract(labels, words):
  res_dict = {} 
  res_dict['currency'] = findCurrency(labels, words)
  res_dict['tax_rate'] = findTaxRate(labels, words)
  res_dict['total_price'] = findTotalPrice(labels, words)
  res_dict['date'] = findDate(labels, words)
  res_dict['address'] = findAddress(labels, words)
  res_dict['vendor'] = findVendor(labels, words)
  res_dict['products'] = findProducts(labels, words)
  return res_dict

def findCurrency(labels, words):
  pot_cur = []
  for i in range(len(labels)):
    if labels[i] == 'currency':
      return words[i]
      pot_cur.append(words[i])
  return None

def findProducts(labels, words):
    products = []
    product_name = ''
    product = {}
    for i, v in enumerate(words):
        if labels[i] == 'product_amount':
            product['amount'] = v
        if labels[i] == 'product_name':
            product_name+=v.lower() + ' '
        elif product_name != '':
            product['name'] = product_name[:-1]
            for j in range(i, len(words)):
                if labels[j] == 'product_amount':
                    if util.isInt(v):
                        product['amount'] = int(v)
                    else:
                        product['amount'] = v
                    if 'price' in product:
                        break
                if labels[j] == 'product_price':
                    product['price'] = words[j]
                    if 'amount' in product:
                        break
                elif labels[j] == 'product_name':
                    break
            if not 'amount' in product:
                product['amount'] = 1
            products.append(product)
            product = {}
            product_name = ''
    return products

def findTaxRate(labels, words):
  tax = None
  for i in range(len(labels)):
    if labels[i] == 'tax_rate':
      tax = words[i]
      break
  try:
    tax = int(tax)
    return tax
  except:
    return None

def findDate(labels, words):
  date = ''
  for i in range(len(labels)):
    if labels[i] == 'date':
      date += words[i]
    elif date != '':
      return date
  return None

def findAddress(labels, words):
  address = ''
  for i in range(len(labels)):
    if labels[i] == 'address':
      address += words[i] + ' '
    elif address != '':
      return address[:-1]
  return None

def findVendor(labels, words):
  vendor = ''
  for i in range(len(labels)):
    if labels[i] == 'vendor':
      vendor += words[i] + ' '
    elif vendor != '':
      return vendor[:-1]
  return None

def findTotalPrice(labels, words):
  pot_price = []
  for i in range(len(labels)):
    if labels[i] == 'total_price':
      pot_price.append(words[i])
  price = ''
  for p in pot_price:
    if price == '':
      price +=p
    elif price != '' and p == '.' and '.' not in price:
      price +=p
    elif '.' in price and util.isInt(p) and int(p) < 100:
      price+=p
      break
  
  if len(price) > 0 and price[-1] == '.':
    price = price[:-1]
  try:
    price = float(price)
    return price
  except:
    return None

def calculateMetrics(reciepts, result, writeToFile=False, path=None):
  correctVendors = 0
  vendorsFound = 0
  vendors = 0

  correctDates = 0
  datesFound = 0
  dates = 0

  correctAddresses = 0
  addressesFound = 0
  addresses = 0

  correctTaxes = 0
  taxesFound = 0
  taxes = 0

  correctPrices = 0
  pricesFound = 0
  prices = 0

  correctCurrencies = 0
  currenciesFound = 0
  currencies = 0

  correctProducts = 0
  productsFound = 0
  products = 0

  result_dict = {}
  count = 0
  for i, reciept in enumerate(reciepts):
      corr = True
      vendor = result[i]['vendor']
      result_dict['vendor'] = vendor
      if vendor:
          vendorsFound+=1
          vendor = vendor.lower()
      if 'vendor' in reciept.groundTruth:
        vendors += 1     
        if vendor and levenshtein_distance(vendor, reciept.groundTruth['vendor'].lower()) <= 0:
            correctVendors +=1
        else:
            corr = False
      date = result[i]['date']
      result_dict['date'] = date
      if date:
          datesFound+=1
          date = date.lower()
      if 'date' in reciept.groundTruth:
          dates += 1
          if date == reciept.groundTruth['date'].lower() or date == reciept.groundTruth['date'].lower().replace(' ', ''):
              correctDates +=1
          else:
              corr = False
      address = result[i]['address']
      result_dict['address'] = address
      if address:
          addressesFound+=1
          address = address.lower()
      if 'address' in reciept.groundTruth:
          addresses += 1
          if address and levenshtein_distance(address, reciept.groundTruth['address'].lower()) <= 0:
              correctAddresses +=1
          else:
              corr = False
      tax = result[i]['tax_rate']
      result_dict['tax_rate'] = tax
      if tax != None:
          taxesFound+=1
      if 'tax_rate' in reciept.groundTruth:
          taxes += 1
          real_tax = int(float(reciept.groundTruth['tax_rate'].lower().replace('%', '')))
          if tax == real_tax:
              correctTaxes +=1
          else:
              corr = False
      price = result[i]['total_price']
      result_dict['total_price'] = price
      if price:
          pricesFound+=1
      if 'total_price' in reciept.groundTruth:
          prices += 1
          real_price = float(reciept.groundTruth['total_price'].lower())
          if price == real_price:
              correctPrices +=1
          else:
              corr = False
      currency = result[i]['currency']
      result_dict['currency'] = currency
      if currency:
          currenciesFound+=1
          currency = currency.lower()
      if 'currency' in reciept.groundTruth:
          currencies += 1
          if currency == reciept.groundTruth['currency'].lower():
              correctCurrencies +=1
          else:
              corr = False
      productsList = result[i]['products']
      result_dict['products'] = productsList
      if 'products' in reciept.groundTruth:
          for product in reciept.groundTruth['products']:
                products += 1
      checkedIndexes = []
      for product in productsList:
          productsFound+=1
          for i, real_product in enumerate(reciept.groundTruth['products']):
              if i in checkedIndexes:
                  continue
              price = None
              if 'price' in product:
                  price = product['price'].replace(',', '.')
                  try:
                      price = float(price)
                  except:
                      price = None
              real_price = real_product['price']
              real_price = float(real_price)
              if levenshtein_distance(product['name'].lower(), real_product['name'].lower()) <= 0:
                if util.floatCompare(price, real_price):
                    if product['amount'] == real_product['amount']:
                        correctProducts +=1
                        checkedIndexes.append(i)
                        break
      if len(checkedIndexes) < len(reciept.groundTruth['products']):
          corr |= False
      if corr:
          count +=1

      if writeToFile:
        with open(os.path.join(path, reciept.path), 'w') as fp:
            json.dump(result_dict, fp, indent=1)
    
  totalDataPoints = vendors + dates + addresses + taxes + prices + currencies + products
  totalDataPointsFound = vendorsFound + datesFound + addressesFound + taxesFound + pricesFound + currenciesFound + productsFound
  totalCorrect = correctVendors + correctDates + correctAddresses + correctTaxes + correctPrices + correctCurrencies + correctProducts
  
  total_precision = 0
  total_recall = 0

  print('-----TOTAL CORRECT RECEIPTS-----')
  print(count, 'of', len(reciepts))
  print('-----VENDORS-----')
  print(vendors, vendorsFound, correctVendors)
  precision = util.precision(correctVendors, vendorsFound)
  recall = util.recall(vendors, correctVendors)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----DATES-----')
  print(dates, datesFound, correctDates)
  precision = util.precision(correctDates, datesFound)
  recall = util.recall(dates, correctDates)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----ADDRESSES-----')
  print(addresses, addressesFound, correctAddresses)
  precision = util.precision(correctAddresses, addressesFound)
  recall = util.recall(addresses, correctAddresses)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----TAX RATES-----')
  print(taxes, taxesFound, correctTaxes)
  precision = util.precision(correctTaxes, taxesFound)
  recall = util.recall(taxes, correctTaxes)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----PRICE-----')
  print(prices, pricesFound, correctPrices)
  precision = util.precision(correctPrices, pricesFound)
  recall = util.recall(prices, correctPrices)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----CURRENCY-----')
  print(currencies, currenciesFound, correctCurrencies)
  precision = util.precision(correctCurrencies, currenciesFound)
  recall = util.recall(currencies, correctCurrencies)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----PRODUCTS-----')
  print(products, productsFound, correctProducts)
  precision = util.precision(correctProducts, productsFound)
  recall = util.recall(products, correctProducts)
  total_precision += precision
  total_recall += recall
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----MICRO AVG-----')
  print(totalDataPoints, totalDataPointsFound, totalCorrect)
  precision = util.precision(totalCorrect, totalDataPointsFound)
  recall = util.recall(totalDataPoints, totalCorrect)
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
  print('-----MACRO AVG-----')
  print(totalDataPoints, totalDataPointsFound, totalCorrect)
  precision = total_precision / 7.0
  recall = total_recall / 7.0
  print('Precision:', precision)
  print('Recall:', recall)
  print('F1:', util.fScore(precision, recall))
    