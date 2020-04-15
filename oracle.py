import os
import util
from Levenshtein import distance as levenshtein_distance


def oracle(reciepts):
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

    count = 0
    for reciept in reciepts:
        corr = True
        getProducts(reciept)
        vendor = getVendor(reciept)
        if 'vendor' in reciept.groundTruth:
            vendors += 1
        if vendor:
            vendorsFound+=1
            if levenshtein_distance(vendor, reciept.groundTruth['vendor'].lower()) <= 0:
                correctVendors +=1
            else:
                corr = False
        elif 'vendor' in reciept.groundTruth:
            corr = False
        date = getDate(reciept)
        if 'date' in reciept.groundTruth:
            dates += 1
        if date:
            datesFound+=1
            if date == reciept.groundTruth['date'].lower():
                correctDates +=1
            else:
                corr = False
        elif 'date' in reciept.groundTruth:
            corr = False
        address = getAddress(reciept)
        if 'address' in reciept.groundTruth:
            addresses += 1
        if address:
            addressesFound+=1
            if levenshtein_distance(address, reciept.groundTruth['address'].lower()) <= 0:
                correctAddresses +=1
            else:
                corr = False
        elif 'address' in reciept.groundTruth:
            corr = False
        tax = getTaxRate(reciept)
        if 'tax_rate' in reciept.groundTruth:
            taxes += 1
        if tax:
            taxesFound+=1
            real_tax = reciept.groundTruth['tax_rate'].lower().replace('%', '').replace('.', '')
            if tax == real_tax:
                correctTaxes +=1
            else:
                corr = False
        elif 'tax_rate' in reciept.groundTruth:
            corr = False
        price = getTotalPrice(reciept)
        if 'total_price' in reciept.groundTruth:
            prices += 1
        if price:
            pricesFound+=1
            real_price = reciept.groundTruth['total_price'].lower().replace('.', '')
            if price == real_price:
                correctPrices +=1
            else:
                corr = False
        elif 'total_price' in reciept.groundTruth:
            corr = False
        currency = getCurrency(reciept)
        if 'currency' in reciept.groundTruth:
            currencies += 1
        if currency:
            currenciesFound+=1
            if currency == reciept.groundTruth['currency'].lower():
                correctCurrencies +=1
            else:
                corr = False
        elif 'currency' in reciept.groundTruth:
            corr = False
        productsList = getProducts(reciept)
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
        if 'products' in reciept.groundTruth:
            if len(checkedIndexes) < len(reciept.groundTruth['products']):
                corr = False
        if corr:
            count += 1

                
    totalDataPoints = vendors + dates + addresses + taxes +  prices + currencies + products
    totalDataPointsFound = vendorsFound + datesFound + addressesFound + taxesFound + pricesFound + currenciesFound + productsFound
    totalCorrect = correctVendors + correctDates + correctAddresses + correctTaxes + correctPrices + correctCurrencies + correctProducts

    print('-----TOTAL CORRECT RECEIPTS-----')
    print(count, 'of', len(reciepts))
    total_precision = 0
    total_recall = 0
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
    print('----- MICRO TOTAL-----')
    print(totalDataPoints, totalDataPointsFound, totalCorrect)
    precision = util.precision(totalCorrect, totalDataPointsFound)
    recall = util.recall(totalDataPoints, totalCorrect)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('----- MACRO TOTAL-----')
    print(totalDataPoints, totalDataPointsFound, totalCorrect)
    precision = total_precision / 7.0
    recall = total_recall / 7.0
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))


def getVendor(reciept):
    vendor = ''
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'vendor' and v not in vendor:
            vendor += v + ' '
    if vendor == '':
        return None
    return vendor[:-1].lower()

def getAddress(reciept):
    address = ''
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'address':
            address += v + ' '
    if address == '':
        return None
    return address[:-1].lower()

def getProducts(reciept):
    products = []
    product_name = ''
    product = {}
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'product_amount':
            product['amount'] = v
        if reciept.dataLabels[i] == 'product_name':
            product_name+=v.lower() + ' '
        elif product_name != '':
            product['name'] = product_name[:-1]
            for j in range(i, len(reciept.dataWords)):
                if reciept.dataLabels[j] == 'product_amount':
                    if util.isInt(v):
                        product['amount'] = int(v)
                    else:
                        product['amount'] = v
                    if 'price' in product:
                        break
                if reciept.dataLabels[j] == 'product_price':
                    product['price'] = reciept.dataWords[j]
                    if 'amount' in product:
                        break
                elif reciept.dataLabels[j] == 'product_name':
                    break
            if not 'amount' in product:
                product['amount'] = 1
            products.append(product)
            product = {}
            product_name = ''
    return products

def getDate(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'date':
            return v.lower()
    return None

def getTotalPrice(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'total_price':
            return v.lower().replace(',', '').replace('.', '')
    return None

def getTaxRate(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'tax_rate':
            return v.lower().replace(',', '').replace('.', '')
    return None

def getCurrency(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'currency':
            return v.lower()
    return None
