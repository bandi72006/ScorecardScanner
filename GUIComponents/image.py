import pygame 

class Images:
    def __init__(self, screen, filePath, XY, finalDims = (0,0)):
        self.__screen = screen
        try:
            self.__image = pygame.image.load(filePath) #saves rendering/processing time by storing surface as attribute
        except: #Except for different paths on machines (Mac/linux file directories)
            filePath = filePath.replace("\\", "/")
            filePath = "ScorecardScanner/" + filePath
            self.__image = pygame.image.load(filePath) 
        if finalDims != (0,0): # (0,0) = has not given size as parameter = keep original size
             self.__image = pygame.transform.scale(self.__image, finalDims)
        
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner

    def draw(self, mousePos, isClick, setScreen, appendScreen, getElements, setScreenElements): #Unused parameter to match draw calling in GUIHandler.py
        self.__screen.blit(self.__image, self.__coordinates)