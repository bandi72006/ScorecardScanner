import pygame
from GUIComponents.selectionMenu import *
from GUIComponents.text import *
from competitor import *
from config import *
from competition import *
import tkinter as tk

class Button:
    def __init__(self, screen, XY, dims, text, function, colour = (255,242,204), hoverColour = (255,213,89), textSize = 32):
        self.__screen = screen
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__dimensions = (dims[0], dims[1])
        self.__colour = colour #Colour for neutral button
        self.__hoverColour = hoverColour #Colour for when mouse is hovering above button
        
        self.text = Text(screen, text, self.__coordinates, textSize)
        self.renderText()
        
        self.__function = function

        #Function code:
        # M0 - Menu change to menu #0
        # E - quit program
        # S"char" - selection menu related to char
        # C - Confirm time

    def renderText(self):
        textSize = self.text.getSize() #Maths to align text
        self.text.setCoordinates((self.__coordinates[0] + (self.__dimensions[0] - textSize[0])//2, self.__coordinates[1] + (self.__dimensions[1] - textSize[1])//2))


    def draw(self, mousePos, isClick, setScreen, appendScreen, getElements): #Unused parameter to match draw calling in GUIHandler.py
        #If the mouse is over the button
        if mousePos[0] > self.__coordinates[0] and mousePos[0] < (self.__coordinates[0] + self.__dimensions[0]) and mousePos[1] > (self.__coordinates[1]) and mousePos[1] < (self.__coordinates[1] + self.__dimensions[1]):
            pygame.draw.rect(self.__screen, self.__hoverColour, (self.__coordinates[0], self.__coordinates[1], self.__dimensions[0], self.__dimensions[1])) #Main button
            if isClick:
                self.__onClick(setScreen, getElements)
        else: 
            pygame.draw.rect(self.__screen, self.__colour, (self.__coordinates[0], self.__coordinates[1], self.__dimensions[0], self.__dimensions[1])) #Main button
        
        pygame.draw.rect(self.__screen, (0,0,0), (self.__coordinates[0]-1, self.__coordinates[1]-1, self.__dimensions[0]+1, self.__dimensions[1]+1), 1) #Button border


        #Coordinate maths is to center text in middle of button

        self.text.draw(mousePos, isClick, setScreen, appendScreen, getElements)

    def __raiseError(self, message):
        window = tk.Tk() 
        window.title('WCA Scorecard scanner') 
        window.geometry('300x70') 
        label = tk.Label(window, text = message)
        label.pack()
        window.mainloop()

    def __onClick(self, setScreen, getElements):
        if self.__function[0] == "M":
            setScreen(int(self.__function[-1]))

        elif self.__function[0] == "C":
            isValidTimes = True #Used to check if can move onto next competitor
            results = []
            resultCount = 0

            for element in getElements():

                if element.__class__.__name__ == "Button": #Loops over first 5 buttons (that contain the time)
                    try:
                        results.append(Result(element.text.getText()) if element.text.getText != "DNF" else DNFResult())
                    
                    except ValueError as error:
                        self.__raiseError(repr(error) + " --> " + element.text.getText())
                        isValidTimes = False
                    resultCount += 1

                if resultCount == 5:
                    break

            if isValidTimes == True: #If all 5 times are valid
                currentCompetitor = config.getCurrentCompetitor()
                
                try: #Case: competitor already in array of competitors
                    currentCompetitor = competition.getCompetitorByName(currentCompetitor["competitor"]) #Object of competitor
                    currentCompetitor.addResult(RoundResult(config.getCurrentCompetitor()["event"], results))

                except IndexError: #Case: creates object for competitor not yet in array of competitors
                    competition.addCompetitor(currentCompetitor["competitor"]) #Creates new competitor object
                    currentCompetitor = competition.getCompetitorByName(currentCompetitor["competitor"])
                    currentCompetitor.addResult(RoundResult(config.getCurrentCompetitor()["event"], results))

                setScreen(5) #Returns back to competitor scanner menu

        
        elif self.__function[0] == "S":

            self.__selectionMenu = selectionMenu() #Talk about like static class or sumn (look at todo list)
            self.__selectionMenuOutput = self.__selectionMenu.draw(self.__function[1:], self.text.getText, self.text.setText)
            
            if self.__function[-1] == "C": #Competitor selection
                currentCompetitor = config.getCurrentCompetitor()
                currentCompetitor["competitor"] = self.__selectionMenuOutput
                config.editYAMLFile("currentCompetitor", currentCompetitor)
            if self.__function[-1] == "E": #Event selection
                currentCompetitor = config.getCurrentCompetitor()
                currentCompetitor["event"] = self.__selectionMenuOutput
                config.editYAMLFile("currentCompetitor", currentCompetitor)

            return self.__selectionMenuOutput

        elif self.__function == "E":
            pygame.quit()
