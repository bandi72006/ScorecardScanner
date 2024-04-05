#Neural network libraries
import pickle
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import model_selection
from sklearn.metrics import accuracy_score
from collections import Counter
import keras.api._v2.keras as keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, InputLayer
from keras.layers import Activation, MaxPooling2D, Dropout, Flatten, Reshape
from keras.utils.np_utils import to_categorical 
#from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
import cv2
import tensorflow as tf
from tensorflow.keras.datasets import mnist #Imports dataset from library
import os

class neuralNet():
    def __init__(self):
        #Batch size = How many samples trained on before updating weights of network
        #Used to reduce memory requirements/lenght of training and also leads to more frequent update of weights
        self.batchSize = 1

        if os.path.isfile("neuralNet.keras"):
            self.model = tf.keras.models.load_model("neuralNet.keras")
        elif os.path.isfile("ScorecardScanner/neuralNet.keras"):
            self.model = tf.keras.models.load_model("ScorecardScanner/neuralNet.keras")
        else:
            self.model = self.createModel()
            self.trainModel()
            

        #self.model.build((200,100,100,1))
        #self.model.summary()


    def createModel(self):
        #Uses Convolutional Neural Network model (CNN)
        model = Sequential()
        model.add(Reshape((28,28,1)))
        model.add(Conv2D(64, (3, 3), padding = 'same', activation = "relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Dropout(0.1))

        model.add(Flatten())

        model.add(Dense(64, activation = "relu"))
        model.add(Dense(10, activation = "softmax")) #10 digits in final output (0-9)
        #Softmax activation function to return probability of each digit

        opt = keras.optimizers.RMSprop(learning_rate=0.0001)

        model.compile(loss='categorical_crossentropy',
                    optimizer=opt,
                    metrics=['accuracy'])

        return model


    def trainModel(self, epochs = 1, save = True):
        (trainX, trainY), (testX, testY) = mnist.load_data() #Loads dataset from library
        
        #Reshapes to add last single dimension and converts to accepted 32-bit float
        trainX = trainX.reshape((trainX.shape[0], 28, 28, 1)).astype('float32')[:10000]
        testX = testX.reshape((testX.shape[0], 28, 28, 1)).astype('float32')

        #Converts labels to categorial (one hot encoding)
        trainY = to_categorical(trainY)[:10000]
        testY = to_categorical(testY)

        print("Num GPUs Available: ", tf.config.list_physical_devices())

        print(tf.__version__)

        self.model.fit(trainX, trainY, validation_data=(testX,testY), batch_size = self.batchSize, verbose = 1, epochs = epochs) #Verbose = status updates on training
        
        if save:
            self.model.save("neuralNet.keras")

    def predict(self, image):

        return self.model.predict(image)

