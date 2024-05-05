import re
from config import *
import csv
import numpy as np
import matplotlib.pyplot as plt
import os

class Comptetitor:
    def __init__(self, name):  
        self.__name = name
        self.__results = [] #Composition using RoundResult objects in has-a relationship

    def getName(self):
        return self.__name
    
    def addResult(self, roundResult):
        self.__results.append(roundResult)

        #add to CSV file for O(1) access
        times = []
        for time in roundResult.getResults():
            times.append(time.getTime())


        #Hashing key: 
        #(sum ASCII of competitor name)*1234 + (sum ASCII of event name)*2006*(roundNumber)
        #Modulo 10,001 (size of CSV file + 1)

        competitorInfo = config.getCurrentCompetitor()
        competitorHash = Comptetitor.generateHashKey(self.__name, competitorInfo["event"])
        self.__editCSVFile(competitorHash, times)
    
    @staticmethod
    def generateHashKey(name, event):
        hashKey = 0
        for char in name:
            hashKey += ord(char)*1234
        
        for char in event:
            hashKey += ord(char)*2006*int(event[-1])
        
        hashKey = hashKey%10001
        return hashKey

    def getResult(self, event):
        if event == -1: #All results
            return self.__results

        for result in self.__results:
            if result.getRound() == event:
                return result

    def __editCSVFile(self, index, times):
        with open("results.csv") as file:
            content = file.readline()
        content = content.split(",")

        os.remove("results.csv") #Removes old version of the file

        for i in range(len(times)):
            content[index+i] = times[i]
        with open("results.csv", "w") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(content)


    
class RoundResult:
    def __init__(self, round, times):
        self.__round = round
        self.__times = times #Composition using Result objects in has-a relationship
        self.__statistics = {}
    
    def getRound(self):
        return self.__round

    def getResults(self):
        return self.__times
    
    def getRanking(self):
        return self.__ranking
    
        
    def __calculateStatistics(self, includeGraph):
        #Converts time to float representation to make it easy to work with
        times = []
        for time in self.__times:
            time = time.getTime()
            time = time.split(":")
            if len(time) == 2: #If there is a minute part
                time = int(time[0])*60 + float(time[1])
            else: #If there is no minute part
                time = float(time[0])

            times.append(time)

        #Render graphs
        if includeGraph:
            xPoints = [i for i in range(1,6)]
            yPoints = times
            plt.plot(xPoints, yPoints, "rx-")
            plt.title("Times progression")
            plt.xlabel("Solve #")
            plt.ylabel("Time (s)")
            plt.savefig("temp1.png")
            self.__statistics["graphsLocation"] = "temp1.png"

        
        #Fastest solve
        self.__statistics["Fastest"] = round(min(times),2)

        #Standard deviation
        self.__statistics["STD"] = round(np.std(times),2)


        #AO5
 
        self.__statistics["AO5"] = round((sum(times)-min(times)-max(times))/3,2)

        

    def getStatistics(self, stat, includeGraph = True):
        if self.__times == []:
            raise ValueError("No times to calculate with")
        
        self.__calculateStatistics(includeGraph)

        if stat == -1: #Return all statistics
            return self.__statistics
        else:
            return self.__statistics[stat]
        
class Result:
    def __init__(self, time):
        if self.__checkTime(time):
            self.__time = time


    def __checkTime(self, time):
        #Regular expression for WCA valid time
        matchObject = re.search("((\d)*:)?\d?\d[.]\d\d(\d)?", time) 
        if matchObject != None:
            if matchObject.span()[1]-matchObject.span()[0] == len(time):
                return True
            
        #Raised if either condition is false
        raise ValueError("Invalid time format")

    def getTime(self):
        return self.__time
    
class DNFResult(Result):
    def __init__(self):
        self.__time = "DNF"

