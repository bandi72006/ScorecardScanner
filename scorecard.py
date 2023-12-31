#Import useful libraries

#Image processing
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from neuralNet import *


class scoreCard():
    def __init__(self):
        self.predictedResults = []
        self.reader = neuralNet()

    #Additional arguements for debugging
    def __preprocess(self, inputImage, dimensions = (310,400), saveImage = False, outputPath = "postProcess.jpg"):
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
        #Therefore downscaled to same aspect ratio (if default parameter is used)
        currImage = cv2.resize(currImage, dimensions)


        #Contours of rectangular boxes
        
        #RETR_TREE = retrieval mode of contours - tells when contours are children of other contours (within other contours)
        #CHAIN_APPROX_SIMPLE = returns only corners of contour rather than all points lying on contour

        contours, _ = cv2.findContours(currImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        #currImage = cv2.cvtColor(currImage,cv2.COLOR_GRAY2BGR)

        finalContours = []

        for cont in contours:
            if cv2.contourArea(cont) > 3800 and cv2.contourArea(cont) < 5000:
                rectangle = cv2.approxPolyDP(cont, 0.009 * cv2.arcLength(cont, True), True)
                
                #currImage = cv2.drawContours(currImage, rectangle, -1, (0,0,255), 2)


                rectangle = rectangle.ravel() #Flattens to 1D array
                #Containts (x,y) of top-left corner and bottom-corner
                rectanglePosition = [[rectangle[0], rectangle[1]], [rectangle[0], rectangle[1]]]
                for i in range(0, len(rectangle), 2):
                    #Flattened array now means that pairs of (x,y) are contiguous
                    x = rectangle[i]
                    y = rectangle[i+1]

                    #Updates the rectangle position if the x and/or y is outside the current tought-to-be correct rectangle
                    rectanglePosition[0][0] = min(rectanglePosition[0][0], x)
                    rectanglePosition[1][0] = max(rectanglePosition[1][0], x)
                    rectanglePosition[0][1] = min(rectanglePosition[0][1], y)
                    rectanglePosition[1][1] = max(rectanglePosition[1][1], y)
                    
                finalContours.append(rectanglePosition)

        
        if saveImage:
            cv2.imwrite((inputImage.replace(".jpg","") + outputPath), currImage)

        return finalContours, currImage
    

    def processCard(self, file):
        times, currImage = self.__preprocess(file) #Stores coordinates of rectangles surrounding times

        _, currImage = cv2.threshold(currImage, 200, 255, cv2.THRESH_BINARY) #Converts image to binary (purely black or white)

        #Loops over every time

        for time in times:
            #Isolates every digit by finding white columns after columns that have black pixels
            whiteColumns = []
            for column in range(time[0][0]+5, time[1][0]-5):
                columnHeight = time[1][1] - time[0][1]
                
                #Find longest contiguous section of white pixels in column
                whiteSpaces = 0
                currentStreak = 0
                for pixel in currImage[time[0][1]-5:time[1][1]+5, column]:
                    if pixel == 255:
                        currentStreak += 1
                        whiteSpaces = max(currentStreak, whiteSpaces)
                    else:
                        currentStreak = 0

                if whiteSpaces > columnHeight-10:
                    whiteColumns.append(column)
                    #cv2.line(currImage, (column,time[0][1]), (column, time[1][1]), (0,0,255), 1)

            
            #Find each digit that are in between whitespaces
            digitBoundaries = []
            for column in range(len(whiteColumns)-1):
                #print(whiteColumns[column]+1, whiteColumns[column+1])
                if whiteColumns[column]+1 != whiteColumns[column+1]: 
                    digitBoundaries.append([whiteColumns[column], whiteColumns[column+1]])

            #To splice out individual characters, use this format -- >
            #cv2.resize(currImage[time[0][1]:time[1][1], digitBoundaries[0][0]: digitBoundaries[0][1]], (28,28))
            #test = np.expand_dims(test,-1)
            #test = np.expand_dims(test, 0)
            
            #cv2.imwrite((file.replace(".jpg","") + "postProcess.jpg"), test)

            if len(digitBoundaries) > 0: #Skips any empty result boxex
                timeResult = ""
                for index in range(len(digitBoundaries)):
                    digit = cv2.resize(currImage[time[0][1]:time[1][1], digitBoundaries[index][0]: digitBoundaries[index][1]], (28,28))

                    #plt.imshow(digit, interpolation='nearest')

                    #digit = np.expand_dims(digit,-1)
                    #digit = np.expand_dims(digit, 0)


                    probabilities = self.reader.predict(digit)
                    
                    print(probabilities*100)
                    print(np.argmax(probabilities))
                    #plt.show()
                    #plt.close()


                    timeResult += str(np.argmax(probabilities)) #Argmax = index of largest value (highest probability)

                print(timeResult)

        

