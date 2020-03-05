import os
import text_processor as tx
import json
import receipt as rc
from ruleBased import predict
import compare
import enchant
import util
from dateutil.parser import parse


textDir = "/Users/markolazic/Desktop/Receipt Labeler/MyFirstImageReader/labels/text"
labelsDir = "/Users/markolazic/Desktop/Receipt Labeler/MyFirstImageReader/labels/labels"
destDir = "/Users/markolazic/Desktop/Receipt Labeler/MyFirstImageReader/processedReceipts"

receipts = []

def main():
    fileNames = os.listdir(textDir)
    fileNames = [i for i in fileNames if (i.endswith('.json'))]
    for fileName in fileNames:
        with open(os.path.join(textDir, fileName)) as text_json:
            text_data = json.load(text_json)
            text_data = tx.filterGarbage(text_data)
            tx.calculateAngles(text_data)
            tx.assignIds(text_data)
            tx.calculateCenterPoints(text_data)
            text_lines = tx.createLines(text_data)
            with open(os.path.join(labelsDir, fileName.split('_')[0] + '_labels.json')) as ground_truth_json:
                truth = json.load(ground_truth_json)
                receipt = rc.Receipt(text_lines, truth)
                receipts.append(receipt) 
                if 'address' in truth and truth['address']== 'Kungsgatan 41':
                    print(fileName)
    for receipt in receipts:
        predict(receipt)

    calculateAccuracy()


def calculateAccuracy():
    total_price_total = 0
    total_price_correct = 0

    currency_total = 0
    currency_correct = 0

    date_total = 0
    date_correct = 0

    vendor_total = 0
    vendor_correct = 0

    tax_rate_total = 0
    tax_rate_correct = 0

    address_total = 0
    address_correct = 0

    products_total = 0
    products_correct = 0
    for receipt in receipts:
        ## Check total price
        if 'total_price' in receipt.groundTruth:
            total_price_total+= 1
            if compare.totalPrice(receipt.groundTruth['total_price'], receipt.prediction['total_price']):
                total_price_correct += 1
        ## Check currecy
        if 'currency' in receipt.groundTruth:
            currency_total+=1
            if compare.currency(receipt.groundTruth['currency'], receipt.prediction['currency']):
                currency_correct += 1
        ## Check date
        if 'date' in receipt.groundTruth:
            date_total+=1
            if compare.date(receipt.groundTruth['date'], receipt.prediction['date'], receipt.rawText):
                date_correct += 1
        ## Check vendor
        if 'vendor' in receipt.groundTruth:
            vendor_total+=1
            if compare.vendor(receipt.groundTruth['vendor'], receipt.prediction['vendor']):
                vendor_correct += 1
        ## Check tax rate
        if 'tax_rate' in receipt.groundTruth:
            tax_rate_total+=1
            if compare.taxRate(receipt.groundTruth['tax_rate'], receipt.prediction['tax_rate']):
                tax_rate_correct += 1
        ## Check address
        if 'address' in receipt.groundTruth:
            address_total+=1
            if compare.address(receipt.groundTruth['address'], receipt.prediction['address']):
                address_correct += 1
        ## Check products
        if 'products' in receipt.groundTruth:
            receiptProducts = receipt.groundTruth['products']
            if not receiptProducts:
                continue
            products_total+=1
            if compare.products(receiptProducts, receipt.prediction['products']):
                products_correct += 1
    print("----------- Results ----------- ")
    print("Total price result: %f  %d/%d" % (total_price_correct/total_price_total, total_price_correct, total_price_total))
    print("Currency result: %f  %d/%d" % (currency_correct/currency_total,currency_correct, currency_total))
    print("Date result: %f  %d/%d" % (date_correct/date_total, date_correct, date_total))
    print("Vendor result: %f  %d/%d" % (vendor_correct/vendor_total, vendor_correct, vendor_total))
    print("Tax rate result: %f  %d/%d" % (tax_rate_correct/tax_rate_total, tax_rate_correct, tax_rate_total))
    print("Address result: %f  %d/%d" % (address_correct/address_total, address_correct, address_total))
    print("Products result: %f  %d/%d" % (products_correct/products_total, products_correct, products_total))
    print("----------- END ----------- ")


if __name__ == '__main__':
    main()