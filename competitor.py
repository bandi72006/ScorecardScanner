import re

class Comptetitor:
    def __init__(self, name, nationality):  
        self.__name = name
        self.__nationality = nationality
        self.__results = [] #Composition using RoundResult objects in has-a relationship

    def getWCAID(self):
        return self.__WCAID

    def getName(self):
        return self.__name
    
    def getNationality(self):
        return self.__nationality
    
    def addResult(self, roundResult):
        self.__results.append(roundResult)

    def getResult(self):
        return self.__results
    
class RoundResult:
    def __init__(self, round, times):
        self.__round = round
        self.__times = times #Composition using Result objects in has-a relationship
        self.__ranking = -1 #Not set yet
        self.__statistics = {}
    
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
        print(time)
        matchObject = re.search("((\d)*:)?\d?\d[.]\d\d", time) 
        if matchObject != None:
            if matchObject.span()[1]-matchObject.span()[0] == len(time):
                return True
            
        else:
            raise ValueError("Invalid time format")


    def getTime(self):
        return self.__time
    
class DNFResult(Result):
    def __init__(self):
        self.__time = "DNF"

