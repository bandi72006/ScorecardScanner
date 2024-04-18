import pygame 

class Text:
    def __init__(self, screen, text, XY, fontSize):
        self.__screen = screen
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__font = pygame.font.Font('freesansbold.ttf', fontSize)
        self.__text = self.__font.render(text, False, (0,0,0))
    
    def draw(self, mousePos, isClick, setScreen, appendScreen, getElements): #Unused parameter to match draw calling in GUIHandler.py
        self.__screen.blit(self.__text, self.__coordinates)