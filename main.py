from scorecard import *
from GUIHandler import *
from competition import *

import os
import csv


#Initialize results csv 
if not os.path.isfile("results.csv"):
    emptyArray = [None]*10000 #Initalizes empty array
    with open("results.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(emptyArray)



window = GUI((1280,720))
window.draw()
