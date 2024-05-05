from competitor import *
import numpy as np
import math

class Competition:
    def __init__(self):
        self.__competitors = []

    def addCompetitor(self, name):
        self.__competitors.append(Comptetitor(name))

    def getCompetitorByName(self, name):
        for person in self.__competitors:
            if person.getName() == name:
                return person

        raise IndexError("Person not found")
    
    def getRoundStats(self, event):

        stats = {}

        #Grabs all times from competitors
        times = {} #Dictionary of person : time
        allTimes = [] #Array of everyones times
        with open("results.csv") as file:
            content = file.readline()
            content = content.split(",")

        for person in config.getCompetitors():
            resultIndex = Comptetitor.generateHashKey(person, event)
            result = []
            if float(content[resultIndex]) != 0: #If result is NOT empty (there is data on competitor)
                for i in range(5):
                    time = content[resultIndex+i]
                    time = time.split(":")
                    if len(time) == 2: #If there is a minute part
                        time = int(time[0])*60 + float(time[1])
                    else: #If there is no minute part
                        time = float(time[0])

                    result.append(time)
                    allTimes.append(time)


                times[person] = result

        #Graphs
        stats["timeTrendGraph"] = self.__genGraph("timeTrend", times)
        stats["AO5Graph"] = self.__genGraph("histogramAO5", times)

        #General stats
        stats["Mean time"] = round(sum(allTimes)/len(allTimes),2)
        stats["Fastest single"] = min(allTimes)
        stats["STD"] = round(np.std(allTimes),2)

        #Rankings
        averages = {}
        for person in times:
            averages[person] = (round((sum(times[person])-max(times[person])-min(times[person]))/3,2))

        #Sorts the averages
        keys = list(averages.keys())
        values = list(averages.values())
        sortedValues = np.argsort(values)
        stats["ranking"] = {keys[i]: values[i] for i in sortedValues}

        return stats
        

    def __genGraph(self, graphType, times):
        if graphType == "timeTrend":
            #Plots time trend across all solves
            x = [i for i in range(1,6)]
            for person in times:
                plt.plot(x, times[person], label=person, marker = "x")

            plt.xlabel("Solve #")
            plt.ylabel("Time (s)")
            plt.title("All competitors 5 solves")
            plt.legend() 

            plt.savefig("tempTimeTrend.png")
            plt.close()
            return "tempTimeTrend.png"
        

        elif graphType == "histogramAO5":
            #Plots histograms of AO5s
            averages = []
            for person in times:
                averages.append(round((sum(times[person])-max(times[person])-min(times[person]))/3,2))

            meanTime = round(sum(averages)/len(averages), 2)
            std = np.std(averages)

            #normal distribution
            x = np.linspace(1, math.ceil(max(averages)),500) #X values for plotting normal distribution
            normalDist = (1/(((2*np.pi)**0.5)*std)) * np.exp(-0.5*((x-meanTime)/std)**2) #Equation of normal distribution applied to x values
            plt.hist(averages)
            plt.plot(x,normalDist*5) #Multiplication to scale distribution


            plt.xlabel("Time (s)")
            plt.ylabel("Density")
            plt.title("Average of 5s")
        
            plt.savefig("tempHistogramAO5.png")
            plt.close()
            return "tempHistogramAO5.png"
        
            

#Initializes competition
competition = Competition()
