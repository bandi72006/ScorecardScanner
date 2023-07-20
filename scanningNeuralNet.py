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

    def preprocess(self, inputImage):
        currImage = cv2.imread(inputImage)
        currImage = cv2.cvtColor(currImage, cv2.COLOR_BGR2GRAY)

        #Dimensions of scorecard ~310x400
        #Therefore downscaled to same aspect ratio
        currImage = cv2.resize(currImage, (310,400))

        cv2.imwrite((inputImage.replace(".jpg","") + "postProcess.jpg"), currImage)

        #INITIALIZE MODEL IF NOT FOUND IN FOLDERS USING PRIVATAE METHODS



    def generateCascadeDataset(self):
        #Dataset taken from:
        #https://www.kaggle.com/datasets/crawford/emnist

        #Dataset uses its own custom mapping for data-labelling (not the same as ASCII)
        #So we must synchronize the mappings given to us in a text file
        mappingsFile = open(r"C:\Users\bandi\OneDrive\Documents\Coding\Datasets\EMNIST\emnist-balanced-mapping.txt", "r")
        mappings = {}
        for line in mappingsFile:
            line = line.split()
            mappings.update({int(line[0]): int(line[1])})





        #Reading training data CSV file
        EMNISTfile = open(r"C:\Users\bandi\OneDrive\Documents\Coding\Datasets\EMNIST\emnist-balanced-train.csv")
        csvreader = csv.reader(EMNISTfile)
        EMNIST = []
        for i, row in enumerate(csvreader):
            EMNIST.append(row)
            if i > 100:
                break

        ele = 75

        ASCIIVal = mappings[int(EMNIST[ele].pop(0))]

        EMNIST = np.transpose(np.array([float(i) for i in EMNIST[ele]]).reshape(28,28))

        print(chr(ASCIIVal), ASCIIVal)


        # creating a plot
        plt.title("Dasda")
        plt.figure()
        
        # plotting a plot

        
        # customizing plot
        plt.imshow(EMNIST, interpolation="nearest")
        plt.show()
