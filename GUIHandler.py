import pygame
from button import *

class GUI:
    def __init__(self, dimensions):
        pygame.init()
        self.__screen = pygame.display.set_mode(dimensions)
        pygame.display.set_caption("WCA Scorecard Scanner")

        self.currentScreen = "mainMenu"

        self.button = Button(self.__screen, (50,50), (100,50), "hello")

    def draw(self):
        while True:
            #Drawing
            self.__screen.fill((255,255,255))
            self.button.draw()
            pygame.display.flip()


            #Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break