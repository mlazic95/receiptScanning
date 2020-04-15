import os
import text_processor as tx
import json
import receipt as rc
from ruleBased import predict
import enchant
import util
import sys
from dateutil.parser import parse
import create_bert_data as data_gen
import torch
from oracle import oracle
from data_extraction import extract, calculateMetrics
import random
from metric import calculateRuleBasedAccuracy, calculateLSTMaccuracy
from data_creator import generateSintheticData
import gcn_data_creator as gcn


trainTextDir = "/Users/markolazic/Desktop/exjobb/project/data/train/text"
trainLabelsDir = "/Users/markolazic/Desktop/exjobb/project/data/train/labels"
lstmResultDir = '/Users/markolazic/Desktop/sroie-task3/src/results'

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


    if args[1] == 'create_data_statistics':
        stats = util.create_data_statistics(receipts, 'vendor')
        for k, v in sorted(stats.items(), reverse = True, key=lambda item: item[1]):
                print(k, '---', v)

    if args[1] == 'generate_gcn_data':
        test_data_dict = {}
        train_data_dict = {}
        for i, receipt in enumerate(receipts):
            if receipt.path in testFilePaths:
                test_data_dict[i] = data_gen.generateWordClasses(receipt)
            else:
                train_data_dict[i] = data_gen.generateWordClasses(receipt, correcting=False)

        gcn.create(receipts, testFilePaths)

    if args[1] == 'create_result':
        path = './data/results/100epochv2_prod'
        test_dict_path = os.path.join(path, 'res_dict.pth')
        res_dict = torch.load(test_dict_path)
        result = list(res_dict.items())
        res_list = []
        for i, (_, (labels, words)) in enumerate(result):
            res = extract(labels,words)
            res_list.append(res)
        calculateMetrics(test_reciepts, res_list, writeToFile=True, path=path)

    if args[1] == 'generate_word_data':
        generateSynthetic = False
        if args[2] and util.isInt(args[2]):
            generateSynthetic = True
            number = int(args[2])
        train_data_dict = {}
        test_data_dict = {}
        for i, receipt in enumerate(receipts):
            if receipt.path in testFilePaths:
                test_data_dict[i] = data_gen.generateWordClasses(receipt)
            else:
                train_data_dict[i] = data_gen.generateWordClasses(receipt, correcting=False)
        if generateSynthetic:
            synthetic = generateSintheticData(receipts, number)
            for i, receipt in enumerate(synthetic):
                train_data_dict[i + len(receipts)] = (receipt.dataWords, receipt.dataLabels)
        vocab = data_gen.createVocabulary(receipts + synthetic)
        f=open('./data/synt_vocab.txt',"w+")
        for w in vocab:
            f.write(w + '\n')
        f.write('[UNK]' + '\n')
        f.write('[CLS]' + '\n')
        f.write('[SEP]' + '\n')
        f.write('[MASK]' + '\n')
        f.close()

        torch.save(train_data_dict, "./data/synt_train_data_dict.pth")
        torch.save(test_data_dict, "./data/synt_test_data_dict.pth")

    if args[1] == 'oracle':
        for i, receipt in enumerate(test_reciepts):
            _ = data_gen.generateWordClasses(receipt)
        oracle(test_reciepts)

    if args[1] == 'rule_based':
        for receipt in test_reciepts:
            predict(receipt)
        calculateRuleBasedAccuracy(test_reciepts)

    if args[1] == 'create_lstm_result':
        result_jsons = os.listdir(lstmResultDir)
        result_jsons = [i for i in result_jsons if (i.endswith('.json'))]
        result_jsons.sort(key=lambda r:int(r.split('.')[0]))
        results_dicts = []
        for fileName in result_jsons:
            with open(os.path.join(lstmResultDir, fileName)) as text_json:
                text_data = json.load(text_json)
                results_dicts+=[text_data]
        calculateLSTMaccuracy(test_reciepts, results_dicts)
                
    elif args[1] == 'create_char_data':
        train_data_dict = {}
        test_data_dict = {}
        for i, receipt in enumerate(receipts):
            if receipt.path in testFilePaths:
                test_data_dict[i] = data_gen.generateCharClasses(receipt, includeProducts=True)
            else:
                train_data_dict[i] = data_gen.generateCharClasses(receipt, includeProducts=True)
        torch.save(train_data_dict, "/Users/markolazic/Desktop/sroie-task3/data/train_char_data_prod.pth")
        torch.save(test_data_dict, "/Users/markolazic/Desktop/sroie-task3/data/test_char_data_prod.pth")


if __name__ == '__main__':
    main(sys.argv)