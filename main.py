import os
import text_processor as tx
import json
import receipt as rc
from ruleBased import predict
import compare
import enchant
import util
import sys
from dateutil.parser import parse
import create_bert_data as data_gen
import torch
from oracle import oracle
from data_extraction import extract, calculateMetrics
import random


trainTextDir = "/Users/markolazic/Desktop/exjobb/project/data/train/text"
trainLabelsDir = "/Users/markolazic/Desktop/exjobb/project/data/train/labels"

receipts = []
testFilePaths = []

def main(args):
    fileNames = os.listdir(trainTextDir)
    fileNames = [i for i in fileNames if (i.endswith('.json'))]
    for fileName in fileNames:
        with open(os.path.join(trainTextDir, fileName)) as text_json:
            text_data = json.load(text_json)
            text_data = tx.filterGarbage(text_data)
            tx.calculateAngles(text_data)
            tx.assignIds(text_data)
            tx.calculateCenterPoints(text_data)
            text_lines = tx.createLines(text_data)
            with open(os.path.join(trainLabelsDir, fileName.split('_')[0] + '_labels.json')) as ground_truth_json:
                truth = json.load(ground_truth_json)
                truth = tx.removeSwedishLetters(truth)
                receipt = rc.Receipt(fileName,text_lines, truth)
                receipts.append(receipt)
    
    f=open('./data/test/test.txt',"r")
    for line in f:
        testFilePaths.append(line[:-1])
    test_reciepts = []
    for receipt in receipts:
        if receipt.path in testFilePaths:
            test_reciepts.append(receipt)

    if args[1] == 'create_result':
        path = './data/results/10epochv2'
        test_dict_path = os.path.join(path, 'res_dict.pth')
        res_dict = torch.load(test_dict_path)
        result = list(res_dict.items())
        res_list = []
        for i, (_, (labels, words)) in enumerate(result):
            res = extract(labels,words)
            res_list.append(res)
        calculateMetrics(test_reciepts, res_list, writeToFile=True, path=path)
                

    if args[1] == 'generate_word_data':
        train_data_dict = {}
        test_data_dict = {}
        for i, receipt in enumerate(receipts):
            if receipt.path in testFilePaths:
                test_data_dict[i] = data_gen.generateWordClasses(receipt)
            else:
                train_data_dict[i] = data_gen.generateWordClasses(receipt, correcting=True)
        '''
        vocab = data_gen.createVocabulary(receipts)
        f=open('./data/my_vocab.txt',"w+")
        for w in vocab:
            f.write(w + '\n')
        f.write('[UNK]' + '\n')
        f.write('[CLS]' + '\n')
        f.write('[SEP]' + '\n')
        f.write('[MASK]' + '\n')
        f.close() '''

        torch.save(train_data_dict, "./data/corr_train_data_dict.pth")
        torch.save(test_data_dict, "./data/corr_test_data_dict.pth")

    if args[1] == 'oracle':
        for i, receipt in enumerate(test_reciepts):
            _ = data_gen.generateWordClasses(receipt)
        oracle(test_reciepts)

    if args[1] == 'rule_based':
        for receipt in receipts:
            predict(receipt)
        calculateAccuracy()

    elif args[1] == 'create_char_data':
        data_dict = {}
        for i, receipt in enumerate(receipts[:-10]):
            data_dict[i] = data_gen.generateCharClasses(receipt)
        torch.save(data_dict, "/Users/markolazic/Desktop/sroie-task3/data/data_dict_test.pth")

    elif args[1] == 'create_char_test_data':
        data_dict = {}
        for i, receipt in enumerate(receipts[-10:]):
            data_dict[i] = data_gen.generateCharClasses(receipt)[0]
        torch.save(data_dict, "/Users/markolazic/Desktop/sroie-task3/data/test_data_dict.pth")


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
            if compare.totalPrice(receipt.groundTruth['total_price'], receipt.ruleBasedPrediction['total_price']):
                total_price_correct += 1
        ## Check currecy
        if 'currency' in receipt.groundTruth:
            currency_total+=1
            if compare.currency(receipt.groundTruth['currency'], receipt.ruleBasedPrediction['currency']):
                currency_correct += 1
        ## Check date
        if 'date' in receipt.groundTruth:
            date_total+=1
            if compare.date(receipt.groundTruth['date'], receipt.ruleBasedPrediction['date'], receipt.rawText):
                date_correct += 1
        ## Check vendor
        if 'vendor' in receipt.groundTruth:
            vendor_total+=1
            if compare.vendor(receipt.groundTruth['vendor'], receipt.ruleBasedPrediction['vendor']):
                vendor_correct += 1
        ## Check tax rate
        if 'tax_rate' in receipt.groundTruth:
            tax_rate_total+=1
            if compare.taxRate(receipt.groundTruth['tax_rate'], receipt.ruleBasedPrediction['tax_rate']):
                tax_rate_correct += 1
        ## Check address
        if 'address' in receipt.groundTruth:
            address_total+=1
            if compare.address(receipt.groundTruth['address'], receipt.ruleBasedPrediction['address']):
                address_correct += 1
        ## Check products
        if 'products' in receipt.groundTruth:
            receiptProducts = receipt.groundTruth['products']
            if not receiptProducts:
                continue
            products_total+=1
            if compare.products(receiptProducts, receipt.ruleBasedPrediction['products']):
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
    main(sys.argv)