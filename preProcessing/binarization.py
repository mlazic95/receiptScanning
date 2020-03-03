import matplotlib.pyplot as plt

from skimage import (data, io, img_as_uint)
from skimage.color import rgb2gray
from skimage.filters import (threshold_sauvola)
from skimage.transform import rotate
import cv2
import os
import numpy as np
import math

receiptDir = "/Users/markolazic/Desktop/Receipt Labeler/MyFirstImageReader/receipts"
destDir = "/Users/markolazic/Desktop/Receipt Labeler/MyFirstImageReader/processedReceipts"
failed = "/Users/markolazic/Desktop/Receipt Labeler/MyFirstImageReader/failed"

def performRotation():
    fileNames = os.listdir(destDir)
    fileNames = [i for i in fileNames if (i.endswith('.jpg'))]
    for fileName in fileNames:
        image = io.imread(os.path.join(destDir,fileName), plugin='matplotlib')
        if image.shape[1] > image.shape[0]:
            rotated = rotate(image, -90, resize=True)
            io.imsave(os.path.join(destDir,fileName), rotated)

def main():
    fileNames = os.listdir(receiptDir)
    fileNames = [i for i in fileNames if (i.endswith('.png') or i.endswith('.jpg') or i.endswith('.jpeg') or i.endswith('.JPG'))]
    fileNames.sort()
    failed = 0
    for fileName in fileNames:
        try:
            image = io.imread(os.path.join(receiptDir,fileName), plugin='matplotlib')
            image = rgb2gray(image)
            window_size = 25
            thresh_sauvola = threshold_sauvola(image, window_size=window_size)
            binary_sauvola = image > thresh_sauvola
            io.imsave(os.path.join(destDir,fileName), img_as_uint(binary_sauvola))
        except:
            os.rename(os.path.join(receiptDir,fileName), os.path.join(failed,fileName))
            failed += 1
    print(failed)


if __name__ == '__main__':
    performRotation()