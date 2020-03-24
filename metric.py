import compare
import util


def calculateLSTMaccuracy(receipts, results):
    total_price_total = 0
    total_price_found = 0
    total_price_correct = 0

    currency_total = 0
    currency_found = 0
    currency_correct = 0

    date_total = 0
    date_found = 0
    date_correct = 0

    vendor_total = 0
    vendor_found = 0
    vendor_correct = 0

    tax_rate_total = 0
    tax_rate_found = 0
    tax_rate_correct = 0

    address_total = 0
    address_found = 0
    address_correct = 0

    for i, receipt in enumerate(receipts):
      ## Check total price
        if 'total_price' in results[i]:
            price = results[i]['total_price'].replace(',','.')
            to_remove = []
            for p in price:
              if util.isInt(p) or p == '.':
                continue
              to_remove.append(p)
            for p in to_remove:
              price = price.replace(p,'')
        else:
            price = None
        if price and price != '':
            total_price_found+=1
        if 'total_price' in receipt.groundTruth:
            total_price_total+= 1
            if compare.totalPrice(receipt.groundTruth['total_price'], price):
                total_price_correct += 1
        ## Check currecy
        if 'currency' in results[i]:
            currency = results[i]['currency']
        else:
            currency = None
        if currency and currency != '':
            currency_found+=1
        if 'currency' in receipt.groundTruth:
            currency_total+=1
            if compare.currency(receipt.groundTruth['currency'], currency):
                currency_correct += 1
        ## Check date
        if 'date' in results[i]:
            date = results[i]['date']
        else:
            date = None
        if date and date != '':
            date_found+=1
        if 'date' in receipt.groundTruth:
            date_total+=1
            if compare.date(receipt.groundTruth['date'],date):
                date_correct += 1
        ## Check vendor
        if 'vendor' in results[i]:
            vendor = results[i]['vendor']
        else:
            vendor = None
        if vendor and vendor != '':
            vendor_found +=1
        if 'vendor' in receipt.groundTruth:
            vendor_total+=1
            if compare.vendor(receipt.groundTruth['vendor'], vendor):
                vendor_correct += 1
        ## Check tax rate
        if 'tax_rate' in results[i]:
            tax = results[i]['tax_rate']
        else:
            tax = None
        if tax and tax != '':
            tax_rate_found+=1
        if 'tax_rate' in receipt.groundTruth:
            tax_rate_total+=1
            if compare.taxRate(receipt.groundTruth['tax_rate'], tax):
                tax_rate_correct += 1
        ## Check address
        if 'address' in results[i]:
            address = results[i]['address']
        else:
            address = None
        if address and address != '':
            address_found += 1
        if 'address' in receipt.groundTruth:
            address_total+=1
            if compare.address(receipt.groundTruth['address'], address):
                address_correct += 1



    totalDataPoints = vendor_total + date_total + address_total + tax_rate_total +  total_price_total + currency_total
    totalDataPointsFound = vendor_found + date_found + address_found + tax_rate_found + total_price_found + currency_found
    totalCorrect = vendor_correct + date_correct + address_correct + tax_rate_correct + total_price_correct + currency_correct
      
    print('-----VENDORS-----')
    print(vendor_total, vendor_found, vendor_correct)
    precision = util.precision(vendor_correct, vendor_found)
    recall = util.recall(vendor_total, vendor_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----DATES-----')
    print(date_total, date_found, date_correct)
    precision = util.precision(date_correct, date_found)
    recall = util.recall(date_total, date_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----ADDRESSES-----')
    print(address_total, address_found, address_correct)
    precision = util.precision(address_correct, address_found)
    recall = util.recall(address_total, address_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----TAX RATES-----')
    print(tax_rate_total, tax_rate_found, tax_rate_correct)
    precision = util.precision(tax_rate_correct, tax_rate_found)
    recall = util.recall(tax_rate_total, tax_rate_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----PRICE-----')
    print(total_price_total, total_price_found, total_price_correct)
    precision = util.precision(total_price_correct, total_price_found)
    recall = util.recall(total_price_total, total_price_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----CURRENCY-----')
    print(currency_total, currency_found, currency_correct)
    precision = util.precision(currency_correct, currency_found)
    recall = util.recall(currency_total, currency_correct)
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

def calculateRuleBasedAccuracy(receipts):
    total_price_total = 0
    total_price_found = 0
    total_price_correct = 0

    currency_total = 0
    currency_found = 0
    currency_correct = 0

    date_total = 0
    date_found = 0
    date_correct = 0

    vendor_total = 0
    vendor_found = 0
    vendor_correct = 0

    tax_rate_total = 0
    tax_rate_found = 0
    tax_rate_correct = 0

    address_total = 0
    address_found = 0
    address_correct = 0

    for receipt in receipts:
        ## Check total price
        if 'total_price' in receipt.ruleBasedPrediction:
            price = receipt.ruleBasedPrediction['total_price']
        else:
            price = None
        if price:
            total_price_found+=1
        if 'total_price' in receipt.groundTruth:
            total_price_total+= 1
            if compare.totalPrice(receipt.groundTruth['total_price'], price):
                total_price_correct += 1
        ## Check currecy
        if 'currency' in receipt.ruleBasedPrediction:
            currency = receipt.ruleBasedPrediction['currency']
        else:
            currency = None
        if currency:
            currency_found+=1
        if 'currency' in receipt.groundTruth:
            currency_total+=1
            if compare.currency(receipt.groundTruth['currency'], currency):
                currency_correct += 1
        ## Check date
        if 'date' in receipt.ruleBasedPrediction:
            date = receipt.ruleBasedPrediction['date']
        else:
            date = None
        if date:
            date_found+=1
        if 'date' in receipt.groundTruth:
            date_total+=1
            if compare.date(receipt.groundTruth['date'],date):
                date_correct += 1
        ## Check vendor
        if 'vendor' in receipt.ruleBasedPrediction:
            vendor = receipt.ruleBasedPrediction['vendor']
        else:
            vendor = None
        if vendor:
            vendor_found +=1
        if 'vendor' in receipt.groundTruth:
            vendor_total+=1
            if compare.vendor(receipt.groundTruth['vendor'], vendor):
                vendor_correct += 1
        ## Check tax rate
        if 'tax_rate' in receipt.ruleBasedPrediction:
            tax = receipt.ruleBasedPrediction['tax_rate']
        else:
            tax = None
        if tax:
            tax_rate_found+=1
        if 'tax_rate' in receipt.groundTruth:
            tax_rate_total+=1
            if compare.taxRate(receipt.groundTruth['tax_rate'], tax):
                tax_rate_correct += 1
        ## Check address
        if 'address' in receipt.ruleBasedPrediction:
            address = receipt.ruleBasedPrediction['address']
        else:
            address = None
        if address:
            address_found += 1
        if 'address' in receipt.groundTruth:
            address_total+=1
            if compare.address(receipt.groundTruth['address'], address):
                address_correct += 1
    totalDataPoints = vendor_total + date_total + address_total + tax_rate_total +  total_price_total + currency_total
    totalDataPointsFound = vendor_found + date_found + address_found + tax_rate_found + total_price_found + currency_found
    totalCorrect = vendor_correct + date_correct + address_correct + tax_rate_correct + total_price_correct + currency_correct
      
    print('-----VENDORS-----')
    print(vendor_total, vendor_found, vendor_correct)
    precision = util.precision(vendor_correct, vendor_found)
    recall = util.recall(vendor_total, vendor_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----DATES-----')
    print(date_total, date_found, date_correct)
    precision = util.precision(date_correct, date_found)
    recall = util.recall(date_total, date_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----ADDRESSES-----')
    print(address_total, address_found, address_correct)
    precision = util.precision(address_correct, address_found)
    recall = util.recall(address_total, address_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----TAX RATES-----')
    print(tax_rate_total, tax_rate_found, tax_rate_correct)
    precision = util.precision(tax_rate_correct, tax_rate_found)
    recall = util.recall(tax_rate_total, tax_rate_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----PRICE-----')
    print(total_price_total, total_price_found, total_price_correct)
    precision = util.precision(total_price_correct, total_price_found)
    recall = util.recall(total_price_total, total_price_correct)
    print('Precision:', precision)
    print('Recall:', recall)
    print('F1:', util.fScore(precision, recall))
    print('-----CURRENCY-----')
    print(currency_total, currency_found, currency_correct)
    precision = util.precision(currency_correct, currency_found)
    recall = util.recall(currency_total, currency_correct)
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