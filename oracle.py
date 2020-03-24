import os
import util


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
    for reciept in reciepts:
        getProducts(reciept)
        vendor = getVendor(reciept)
        if 'vendor' in reciept.groundTruth:
            vendors += 1
        if vendor:
            vendorsFound+=1
            if vendor == reciept.groundTruth['vendor'].lower():
                correctVendors +=1
        date = getDate(reciept)
        if 'date' in reciept.groundTruth:
            dates += 1
        if date:
            datesFound+=1
            if date == reciept.groundTruth['date'].lower():
                correctDates +=1
        address = getAddress(reciept)
        if 'address' in reciept.groundTruth:
            addresses += 1
        if address:
            addressesFound+=1
            if address == reciept.groundTruth['address'].lower():
                correctAddresses +=1
        tax = getTaxRate(reciept)
        if 'tax_rate' in reciept.groundTruth:
            taxes += 1
        if tax:
            taxesFound+=1
            real_tax = reciept.groundTruth['tax_rate'].lower().replace('%', '').replace('.', '')
            if tax == real_tax:
                correctTaxes +=1
        price = getTotalPrice(reciept)
        if 'total_price' in reciept.groundTruth:
            prices += 1
        if price:
            pricesFound+=1
            real_price = reciept.groundTruth['total_price'].lower().replace('.', '')
            if price == real_price:
                correctPrices +=1
        currency = getCurrency(reciept)
        if 'currency' in reciept.groundTruth:
            currencies += 1
        if currency:
            currenciesFound+=1
            if currency == reciept.groundTruth['currency'].lower():
                correctCurrencies +=1
        productsList = getProducts(reciept)
        if 'products' in reciept.groundTruth:
            for product in reciept.groundTruth['products']:
                products += 1
        ## TODO: Make sure no double match
        for product in productsList:
            productsFound+=1
            for real_product in reciept.groundTruth['products']:
                price = None
                if 'price' in product:
                    price = product['price'].replace(',', '.')
                    try:
                        price = float(price)
                    except:
                        price = None
                real_price = real_product['price']
                real_price = float(real_price)
                if product['name'].lower() == real_product['name'].lower():
                    if util.floatCompare(price, real_price):
                        correctProducts +=1
                    else:
                        print(price, real_price)
                
    totalDataPoints = vendors + dates + addresses + taxes +  prices + currencies
    totalDataPointsFound = vendorsFound + datesFound + addressesFound + taxesFound + pricesFound + currenciesFound
    totalCorrect = correctVendors + correctDates + correctAddresses + correctTaxes + correctPrices + correctCurrencies
        
    print('-----VENDORS-----')
    print(vendors, vendorsFound, correctVendors)
    precision = util.precision(correctVendors, vendorsFound)
    recall = util.recall(vendors, correctVendors)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----DATES-----')
    print(dates, datesFound, correctDates)
    precision = util.precision(correctDates, datesFound)
    recall = util.recall(dates, correctDates)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----ADDRESSES-----')
    print(addresses, addressesFound, correctAddresses)
    precision = util.precision(correctAddresses, addressesFound)
    recall = util.recall(addresses, correctAddresses)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----TAX RATES-----')
    print(taxes, taxesFound, correctTaxes)
    precision = util.precision(correctTaxes, taxesFound)
    recall = util.recall(taxes, correctTaxes)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----PRICE-----')
    print(prices, pricesFound, correctPrices)
    precision = util.precision(correctPrices, pricesFound)
    recall = util.recall(prices, correctPrices)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----CURRENCY-----')
    print(currencies, currenciesFound, correctCurrencies)
    precision = util.precision(correctCurrencies, currenciesFound)
    recall = util.recall(currencies, correctCurrencies)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----PRODUCTS-----')
    print(products, productsFound, correctProducts)
    precision = util.precision(correctProducts, productsFound)
    recall = util.recall(products, correctProducts)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----TOTAL-----')
    print(totalDataPoints, totalDataPointsFound, totalCorrect)
    precision = util.precision(totalCorrect, totalDataPointsFound)
    recall = util.recall(totalDataPoints, totalCorrect)
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
        if reciept.dataLabels[i] == 'product_name':
            product_name+=v.lower() + ' '
        elif product_name != '':
            product['name'] = product_name[:-1]
            for j in range(i, len(reciept.dataWords)):
                if reciept.dataLabels[j] == 'product_price':
                    product['price'] = reciept.dataWords[j]
                    break
                elif reciept.dataLabels[j] == 'product_name':
                    break
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
