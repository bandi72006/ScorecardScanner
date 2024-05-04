import re
from config import *
import pandas as pd

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
        print(hashKey)
        return hashKey

    def getResult(self):
        return self.__results
    
    def __editCSVFile(self, index, times):
        results = pd.read_csv("results.csv") 
        
        results.loc[index] = "time"
        
        results.to_csv("results.csv", index=False) 
        

    
class RoundResult:
    def __init__(self, round, times):
        self.__round = round
        self.__times = times #Composition using Result objects in has-a relationship
        self.__ranking = -1 #Not set yet
        self.__statistics = {}
    
    def getRound(self):
        return self.__round

    def getResults(self):
        return self.__times
    
    def getRanking(self):
        return self.__ranking
    
    def setRakning(self, rank):
        if rank >= 1:
            self.__ranking = rank
        else:
            raise ValueError("Invalid rank")
        
    def __calculateStatistics(self):
        pass

    def getStatistics(self, stat):
        if self.__times == []:
            raise ValueError("No times to calculate with")
        
        self.__calculateStatistics()

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

