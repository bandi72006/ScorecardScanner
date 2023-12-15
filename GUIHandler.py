import pygame
from button import *

class GUI:
    def __init__(self, dimensions):
        pygame.init()
        self.__screen = pygame.display.set_mode(dimensions)
        pygame.display.set_caption("WCA Scorecard Scanner")

        #0 = Main menu
        self.currentScreen = 0
        self.__mainMenu = [Button(self.__screen, (315,300), (300,100), "Data entry"), 
                           Button(self.__screen, (665,300), (300,100), "Statistics"),
                           Button(self.__screen, (315,425), (300,100), "Export data"),
                           Button(self.__screen, (665,425), (300,100), "Configuration"),
                           Button(self.__screen, (490,550), (300,100), "Exit", (255,94,94), (255,33,33))]
        
        self.__WCALogo = pygame.transform.scale(pygame.image.load("WCALogo.png"), (250,250)) #Logo as attribute as used in every menu, saves rendering/processing time


    def draw(self):
        while True:
            #Drawing
            mousePos = pygame.mouse.get_pos()
            self.__screen.fill((255,255,255))
            for element in self.__mainMenu:
                element.draw(mousePos)
            
            self.__screen.blit(self.__WCALogo, (515,10))
            
            pygame.display.flip()


            #Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break