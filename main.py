from scorecard import *
from GUIHandler import *

scanNeuralNet = scoreCard()

window = GUI((1280,720))
window.draw()

scanNeuralNet.processCard("testCard.jpg")