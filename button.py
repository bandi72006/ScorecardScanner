import pygame
from selectionMenu import *

class Button:
    def __init__(self, screen, XY, dims, text, function, colour = (255,242,204), hoverColour = (255,213,89), textSize = 32):
        self.__screen = screen
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__dimensions = (dims[0], dims[1])
        self.__colour = colour #Colour for neutral button
        self.__hoverColour = hoverColour #Colour for when mouse is hovering above button
        self.__font = pygame.font.Font('freesansbold.ttf', textSize)
        self.__renderFont(text)
        self.__function = function

        #Function code:
        # M0 - Menu change to menu #0
        #E - quit program
        #S"char" - selection menu related to char

    def __renderFont(self, textToRender):
        self.__text = self.__font.render(textToRender, False, (0,0,0))
        self.__textSize = (self.__text.get_width(), self.__text.get_height()) #Gets space taken by text

    def draw(self, mousePos, isClick, setScreen):
        #If the mouse is over the button
        if mousePos[0] > self.__coordinates[0] and mousePos[0] < (self.__coordinates[0] + self.__dimensions[0]) and mousePos[1] > (self.__coordinates[1]) and mousePos[1] < (self.__coordinates[1] + self.__dimensions[1]):
            pygame.draw.rect(self.__screen, self.__hoverColour, (self.__coordinates[0], self.__coordinates[1], self.__dimensions[0], self.__dimensions[1])) #Main button
            if isClick:
                self.__onClick(setScreen)
        else:
            pygame.draw.rect(self.__screen, self.__colour, (self.__coordinates[0], self.__coordinates[1], self.__dimensions[0], self.__dimensions[1])) #Main button
        
        pygame.draw.rect(self.__screen, (0,0,0), (self.__coordinates[0]-1, self.__coordinates[1]-1, self.__dimensions[0]+1, self.__dimensions[1]+1), 1) #Button border


        #Coordinate maths is to center text in middle of button
        self.__screen.blit(self.__text, (self.__coordinates[0] + (self.__dimensions[0] - self.__textSize[0])//2, self.__coordinates[1] + (self.__dimensions[1] - self.__textSize[1])//2))

    def __onClick(self, setScreen):
        if self.__function[0] == "M":
            setScreen(int(self.__function[-1]))
        
        elif self.__function[0] == "S":
            self.__selectionMenu = selectionMenu() #Talk about like static class or sumn (look at todo list)
            self.__selectionMenuOutput = self.__selectionMenu.draw(self.__function[-1])

            self.__renderFont(self.__selectionMenuOutput)
            return self.__selectionMenuOutput

        elif self.__function == "E":
            pygame.quit()
