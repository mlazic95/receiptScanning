import os
import json
import functools
import math
import numpy as np
import cv2
import ruleBased
from skimage import io
import receipt
import util
import re

def calculateAngles(data):
    for box in data:
        x1 = float(box["topLeft"][1:].split(',')[0])
        y1 = float(box["topLeft"][:-1].split(',')[1])
        x2 = float(box["bottomLeft"][1:].split(',')[0])
        y2 = float(box["bottomLeft"][:-1].split(',')[1])
        diffs = (x1-x2, y1-y2)
        rotation = math.atan(diffs[0]/diffs[1])
        box['angle'] = rotation

def assignIds(data):
    for i, word in enumerate(data):
        word['id'] = i

def calculateCenterPoints(data):
    for box in data:
        x1 = float(box["topLeft"][1:].split(',')[0])
        y1 = float(box["topLeft"][:-1].split(',')[1])
        x2 = float(box["bottomRight"][1:].split(',')[0])
        y2 = float(box["bottomRight"][:-1].split(',')[1])
        center = ((x1+x2)/2,(y1+y2)/2)
        box['center'] = center

'''
def rotateImage(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result
'''

def removeSwedishLetters(data):
    keys = data.keys()
    for key in keys:
        if key == 'products':
            continue
        text = re.sub(r'ä|Ä','a', data[key])
        text = re.sub(r'ö|Ö','o',text)
        text = re.sub(r'å|Å','a',text)
        data[key] = text
    return data


def verticalCompare(box1, box2):
    top1 = (float(box1["topLeft"][:-1].split(',')[1]) + float(box1["topRight"][:-1].split(',')[1])) / 2
    top2 = (float(box2["topLeft"][:-1].split(',')[1]) + float(box2["topRight"][:-1].split(',')[1])) / 2
    return top2 - top1

def horizontalCompare(box1, box2):
    top1 = float(box1["topLeft"][1:].split(',')[0])
    top2 = float(box2["topLeft"][1:].split(',')[0])
    return top1 - top2

def horizontalOverlap(box1, box2):

    top1 = (float(box1["topLeft"][:-1].split(',')[1]) + float(box1["topRight"][:-1].split(',')[1]))/ 2
    bottom1 = (float(box1["bottomLeft"][:-1].split(',')[1]) + float(box1["bottomRight"][:-1].split(',')[1]))/ 2
    height1 = top1 - bottom1

    top2 = (float(box2["topLeft"][:-1].split(',')[1]) + float(box2["topRight"][:-1].split(',')[1]))/ 2
    bottom2 = (float(box2["bottomLeft"][:-1].split(',')[1]) + float(box2["bottomRight"][:-1].split(',')[1]))/ 2
    height2 = top2 - bottom2
    if top1 >= top2:
        if bottom1 <= bottom2:
            overlap = height2
        else:
            overlap = top2 - bottom1
    else:
        if bottom1 >= bottom2:
            overlap = height1
        else:
            overlap = top1 - bottom2
    
    return overlap

def verticalOverlap(box1, box2):
    left1 = float(box1["topLeft"][1:].split(',')[0])
    rigt1 = float(box1["topRight"][1:].split(',')[0])
    width1 = rigt1 - left1

    left2 = float(box2["topLeft"][1:].split(',')[0])
    right2 = float(box2["topRight"][1:].split(',')[0])
    width2 = right2 - left2

    if rigt1 >= right2:
        if left1 <= left2:
            overlap = width2
        else:
            overlap = right2 - left1
    else:
        if left1 >= left2:
            overlap = width1
        else:
            overlap = rigt1 - left2
    return overlap


def filterGarbage(data):
    filtered = []
    for box in data:
        top = (float(box["topLeft"][:-1].split(',')[1]) + float(box["topRight"][:-1].split(',')[1]))/2
        bottom = (float(box["bottomLeft"][:-1].split(',')[1]) + float(box["bottomRight"][:-1].split(',')[1]))/2
        left = float(box["topLeft"][1:].split(',')[0])
        rigt = float(box["topRight"][1:].split(',')[0])
        width = rigt - left
        height = top - bottom
        text = box['text']
        if height <= 0 or width <= 0:
            continue
        if len(text) <= 1 or len(text) > 40:
            continue
        if util.fourInARow(text):
            continue
        if util.alphaNumericRatio(text) <= 0.5:
            continue
        vowelRatio = util.vowelRatio(text)
        if text.isalpha() and vowelRatio < 0.1 or vowelRatio > 0.9:
            continue
        filtered.append(box)
    return filtered

def wordToLineOverlap(word, line):
    maxOverlap = 0
    for el in line:
        if word == el:
            continue
        currentOverlap = horizontalOverlap(word, el)
        if verticalOverlap(word, el) > 0:
            return 0
        if currentOverlap > maxOverlap:
            maxOverlap = currentOverlap
    return maxOverlap

def createLines(data):
    boxes = sorted(data, key=functools.cmp_to_key(verticalCompare))
    boxes = boxes
    lines = []
    i = 0
    while i < len(boxes):
        line = []
        line.append(boxes[i])
        plus = True
        for j in range(i+1, len(boxes)):
            if horizontalOverlap(boxes[i], boxes[j]) > 0 and verticalOverlap(boxes[i], boxes[j]) < 0.1:
                line.append(boxes[j])
            else:
                plus = False
                i = j
                break
        line = sorted(line, key=functools.cmp_to_key(horizontalCompare))
        lines.append(line)
        if plus:
            i += 1
    for i in range(0, len(lines)):
            upMoved = []
            downMoved = []
            for word in lines[i]:
                currentMaxOverlap = wordToLineOverlap(word, lines[i])
                if i > 0:
                    potentialMaxOverlap = wordToLineOverlap(word, lines[i - 1])
                    if potentialMaxOverlap > currentMaxOverlap:
                        upMoved.append(word)
                        continue
                if i < len(lines) - 1:
                    potentialMaxOverlap = wordToLineOverlap(word, lines[i + 1])
                    if potentialMaxOverlap > currentMaxOverlap:
                        downMoved.append(word)
            for word in upMoved:
                lines[i].remove(word)
                lines[i-1].append(word)
            if upMoved:
                lines[i-1] = sorted(lines[i-1], key=functools.cmp_to_key(horizontalCompare))
                upMoved.clear()
            for word in downMoved:
                lines[i].remove(word)
                lines[i+1].append(word)
            if downMoved:
                lines[i+1] = sorted(lines[i+1], key=functools.cmp_to_key(horizontalCompare))
                downMoved.clear()
    return lines