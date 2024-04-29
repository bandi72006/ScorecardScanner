import pygame
import cv2
from scorecard import *
import numpy as np

class Camera:
    def __init__(self, screen, XY, dims):
        self.__screen = screen
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__dimensions = (dims[0], dims[1]) #(Width, height)
        self.__camera = cv2.VideoCapture(0)
        #Function code:
        # M0 - Menu change to menu #0
        # E - quit program

    def __getCameraInput(self):
        success, frame = self.__camera.read()

        if not success:
            return -1
        
        #if frame.shape[0] < frame.shape[1]:
        #    frame = cv2.transpose(frame) #Rotates image 90 degrees (as input is for some reason rotated)


        frame = np.fliplr(frame)
        
        if frame.shape[0] > frame.shape[1]:
            frame = np.rot90(frame)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converts to pygame recognizable format
        frame = cv2.resize(frame, self.__dimensions) #Resizes camera input
        

        return frame
        

    def draw(self, mousePos, isClick, setScreen, appendScreen, getElements): #Unused parameter to match draw calling in GUIHandler.py

        frame = self.__getCameraInput()
        surface = pygame.surfarray.make_surface(frame)
        self.__screen.blit(surface, self.__coordinates)

        #Draws 4 markers to indicate where scorecard should be
        markerOffset = 60
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + markerOffset, self.__coordinates[1] + markerOffset, 10, 10)) #Top left
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + self.__dimensions[1] - markerOffset - 10, self.__coordinates[1] + markerOffset, 10, 10)) #Top right
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + markerOffset, self.__coordinates[1] + self.__dimensions[0] - markerOffset - 10, 10, 10)) #Bottom left
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + self.__dimensions[1] - markerOffset - 10, self.__coordinates[1] + self.__dimensions[0] - markerOffset - 10, 10, 10)) #Bottom right


        #Checks if space has been pressed
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    times = Scorecard()
                    times.processCard(self.__getCameraInput(), save = True)
                    results = times.getResults()
                    setScreen(6)
                    resultCount = 0
                    for element in getElements():
                        if element.__class__.__name__ == "Button": #Updates text on buttons to results
                            element.text.setText(results[resultCount])
                            element.renderText()
                            resultCount += 1
                        
                        if resultCount == 5:
                            break
                    

