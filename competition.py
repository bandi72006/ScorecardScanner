from competitor import *

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
    
#Initializes competition
competition = Competition()
