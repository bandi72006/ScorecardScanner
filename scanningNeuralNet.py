#Import useful libraries

#Image processing
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Dataset handling
import csv

class neuralNet():
    def __init__(self):
        pass

    def preprocess(self, inputImage, dimensions = (310,400), saveImage = False, outputPath = "postProcess.jpg"):
        currImage = cv2.imread(inputImage)

        #Cropping edges to include only scorecard

        #Top boundary
        meanRowVal = 0
        whiteThreshold = 200
        currentRow = 0
        while meanRowVal < whiteThreshold:
            meanRowVal = 0
            for pixel in range(len(currImage[currentRow])):
                meanRowVal += sum(currImage[currentRow][pixel])/3 #Mean brightness of each pixel accounting for RGB

            meanRowVal /= len(currImage[currentRow])
            currentRow += 1

        #Bottom boundary
        currImage = currImage[currentRow:]

        meanRowVal = 0
        currentRow = len(currImage)-1
        while meanRowVal < whiteThreshold:
            meanRowVal = 0
            for pixel in range(len(currImage[currentRow])):
                meanRowVal += sum(currImage[currentRow][pixel])/3 #Mean brightness of each pixel accounting for RGB

            meanRowVal /= len(currImage[currentRow])
            currentRow -= 1

        currImage = currImage[:currentRow]

        #Right boundary
        meanColVal = 0
        currentCol = 0
        while meanColVal < whiteThreshold:
            meanColVal = 0
            for pixel in range(len(currImage)):
                meanColVal += sum(currImage[pixel][currentCol])/3 #Mean brightness of each pixel accounting for RGB

            meanColVal /= len(currImage)
            currentCol += 1

        currImage = currImage[:, currentCol:]

        #Left boundary
        meanColVal = 0
        currentCol = len(currImage[0])-1
        while meanColVal < whiteThreshold:
            meanColVal = 0
            for pixel in range(len(currImage)):
                meanColVal += sum(currImage[pixel][currentCol])/3 #Mean brightness of each pixel accounting for RGB

            meanColVal /= len(currImage)
            currentCol -= 1

        currImage = currImage[:, :currentCol]


        
        currImage = cv2.cvtColor(currImage, cv2.COLOR_BGR2GRAY)

        _, currImage = cv2.threshold(currImage, 200, 255, cv2.THRESH_BINARY) #Converts image to binary (purely black or white)

        #Dimensions of scorecard ~310x400
        #Therefore downscaled to same aspect ratio
        currImage = cv2.resize(currImage, dimensions)


        #Contours of rectangular boxes
        
        #RETR_TREE = retrieval mode of contours - tells when contours are children of other contours (within other contours)
        #CHAIN_APPROX_SIMPLE = returns only corners of contour rather than all points lying on contour

        contours, _ = cv2.findContours(currImage, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        currImage = cv2.cvtColor(currImage,cv2.COLOR_GRAY2BGR)
        for cont in contours:
            if cv2.contourArea(cont) > 3500:
                contours = cv2.drawContours(currImage, cont, -1, (0,0,255), 20)
                print(cv2.contourArea(cont))
                print(cont)
        
        if saveImage:
            cv2.imwrite((inputImage.replace(".jpg","") + outputPath), currImage)
