import pygame 

class Text:
    def __init__(self, screen, text, XY, fontSize):
        self.__screen = screen
        self.__text = text
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__font = pygame.font.Font('freesansbold.ttf', fontSize)
        self.__renderFont(text)
        
    
    def __renderFont(self, textToRender):
        self.__renderedText = self.__font.render(textToRender, False, (0,0,0))
        self.__textSize = (self.__renderedText.get_width(), self.__renderedText.get_height()) #Gets space taken by text
    
    def setCoordinates(self, coordinates):
        self.__coordinates = coordinates
        
    def getSize(self):
        return self.__textSize

    def getText(self):
        return self.__text
    
    def setText(self, text):
        self.__text = text
        self.__renderFont(self.__text)

    def draw(self, mousePos, isClick, setScreen, appendScreen, getElements): #Unused parameter to match draw calling in GUIHandler.py
        self.__screen.blit(self.__renderedText, self.__coordinates)