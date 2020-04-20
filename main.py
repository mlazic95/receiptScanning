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
from string import ascii_uppercase, digits, punctuation
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotData as plot

trainTextDir = "/Users/markolazic/Desktop/exjobb/project/data/train/text"
trainLabelsDir = "/Users/markolazic/Desktop/exjobb/project/data/train/labels"
lstmResultDir = '/Users/markolazic/Desktop/sroie-task3/src/results1000'

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


    if args[1] == 'plot_bert':
        d1 = pd.DataFrame({'train synthetic 10000': plot.train_10000_v2, 'validation synthetic 10000': plot.val_10000_v2}, index=range(1,31))
        d2 = pd.DataFrame({'train synthetic 1000': plot.train_1000, 'validation synthetic 1000': plot.val_1000})
        d3 = pd.DataFrame({'train real data': plot.train, 'validation real data': plot.val}, index=range(1,31))
        data = pd.concat([d1,d2,d3], axis=1)
        sns.set_style("darkgrid")
        ax = sns.lineplot(data=data)
        ax.set(xlabel='epoch', ylabel='loss')
        plt.show()

    if args[1] == 'plot_lstm':
        f1 = open('/Users/markolazic/Desktop/sroie-task3/data/trainLoss.txt','r')
        f2 = open('/Users/markolazic/Desktop/sroie-task3/data/valLoss.txt','r')
        f1Lines = f1.readlines()
        f2Lines = f2.readlines()
        trail_loss = []
        for line in f1Lines:
            trail_loss.append(float(line[:-1]))
        val_loss = []
        for line in f2Lines:
            val_loss.append(float(line[:-1]))

        print(trail_loss, val_loss)




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
        path = './data/results/10000_synt'
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
            for i, (words, labels) in enumerate(synthetic):
                train_data_dict[i + len(receipts)] = (words, labels)
        '''
        vocab = data_gen.createVocabulary(receipts + synthetic)
        f=open('./data/synt_vocab.txt',"w+")
        for w in vocab:
            f.write(w + '\n')
        f.write('[UNK]' + '\n')
        f.write('[CLS]' + '\n')
        f.write('[SEP]' + '\n')
        f.write('[MASK]' + '\n')
        f.close()
        '''
        torch.save(train_data_dict, "./data/synt_10000_train_data_dict.pth")
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
        generateSynthetic = True
        number = 10000
        train_data_dict = {}
        test_data_dict = {}
        for i, receipt in enumerate(receipts):
            if receipt.path in testFilePaths:
                test_data_dict[i] = data_gen.generateCharClasses(receipt, includeProducts=True)
            else:
                train_data_dict[i] = data_gen.generateCharClasses(receipt, includeProducts=True)
        if generateSynthetic:
            VOCAB = ascii_uppercase + digits + punctuation + " \t\n"
            for r in receipts:
                data_gen.generateWordClasses(r)
            synthetic = generateSintheticData(receipts, number)
            for i, (words, labels) in enumerate(synthetic):
                t_new_words = ''
                t_new_labels = []
                for w, l in zip(words, labels):
                    t_new_words += w.upper() + ' '
                    t_new_labels +=[util.getClassInt(l) for i in range(len(w))] + [0]
                new_words = ''
                new_labels = []
                for index in range(len(t_new_words)):
                    if t_new_words[index] in VOCAB:
                        new_words+= t_new_words[index]
                        new_labels.append(t_new_labels[index])
                new_words = new_words[0:-1]
                new_labels = new_labels[0:-1]
                for i in range(1, len(new_words) - 1):
                    if new_labels[i] == 0 and new_labels[i-1] == new_labels[i+1]:
                        new_labels[i] = new_labels[i-1]
                train_data_dict[len(receipts) + i] = (new_words, new_labels)
        print(train_data_dict)
        torch.save(train_data_dict, "/Users/markolazic/Desktop/sroie-task3/data/train_char_data_prod_synt10000.pth")
        torch.save(test_data_dict, "/Users/markolazic/Desktop/sroie-task3/data/test_char_data_prod_synt10000.pth")


if __name__ == '__main__':
    main(sys.argv)