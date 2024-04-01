import pygame
import cv2

class Camera:
    def __init__(self, screen, XY, dims):
        self.__screen = screen
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__dimensions = (dims[0], dims[1])
        self.__camera = cv2.VideoCapture(0)
        #Function code:
        # M0 - Menu change to menu #0
        #E - quit program

    def __getCameraInput(self):
        success, frame = self.__camera.read()
        if not success:
            return -1
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #Converts to pygame recognizable format
        #frame = cv2.transpose(frame) #Rotates image 90 degrees (as input is for some reason rotated)
        frame = cv2.resize(frame, self.__dimensions) #Resizes camera input
        return frame
        

    def draw(self, mousePos, isClick, setScreen): #Unused parameter to match draw calling in GUIHandler.py

        frame = self.__getCameraInput()
        surface = pygame.surfarray.make_surface(frame)
        self.__screen.blit(surface, self.__coordinates)

        #Draws 4 markers to indicate where scorecard should be
        markerOffset = 60
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + markerOffset, self.__coordinates[1] + markerOffset, 10, 10)) #Top left
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + self.__dimensions[1] - markerOffset - 10, self.__coordinates[1] + markerOffset, 10, 10)) #Top right
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + markerOffset, self.__coordinates[1] + self.__dimensions[0] - markerOffset - 10, 10, 10)) #Bottom left
        pygame.draw.rect(self.__screen, (255,0,0), (self.__coordinates[0] + self.__dimensions[1] - markerOffset - 10, self.__coordinates[1] + self.__dimensions[0] - markerOffset - 10, 10, 10)) #Bottom right


