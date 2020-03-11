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
    for reciept in reciepts:
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
            if tax == reciept.groundTruth['tax_rate'].lower():
                correctTaxes +=1
        price = getTotalPrice(reciept)
        if 'total_price' in reciept.groundTruth:
            prices += 1
        if price:
            pricesFound+=1
            if price == reciept.groundTruth['total_price'].lower():
                correctPrices +=1
        currency = getCurrency(reciept)
        if 'currency' in reciept.groundTruth:
            currencies += 1
        if currency:
            currenciesFound+=1
            if currency == reciept.groundTruth['currency'].lower():
                correctCurrencies +=1
        
        
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

def getDate(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'date':
            return v.lower()
    return None

def getTotalPrice(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'total_price':
            return v.lower()
    return None

def getTaxRate(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'tax_rate':
            return v.lower()
    return None

def getCurrency(reciept):
    for i, v in enumerate(reciept.dataWords):
        if reciept.dataLabels[i] == 'currency':
            return v.lower()
    return None
