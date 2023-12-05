import pygame
class Button:
    def __init__(self, screen, XY, dims, text, colour = (255,242,204)):
        self.__screen = screen
        self.__coordinates = (XY[0], XY[1]) #Coordinates of top-left corner
        self.__dimensions = (dims[0], dims[1])
        self.__colour = colour
        self.__font = pygame.font.Font('freesansbold.ttf', 16)
        self.__text = self.__font.render(text, False, (0,0,0))


    def draw(self):
        pygame.draw.rect(self.__screen, self.__colour, (self.__coordinates[0], self.__coordinates[1], self.__dimensions[0], self.__dimensions[1])) #Main button
        pygame.draw.rect(self.__screen, (0,0,0), (self.__coordinates[0]-1, self.__coordinates[1]-1, self.__dimensions[0]+1, self.__dimensions[1]+1), 1) #Button border


        #FIX TEXT CENTERING
        self.__screen.blit(self.__text, (self.__coordinates[0] + (self.__dimensions[0])//2 - 8, self.__coordinates[1] + (self.__dimensions[1])//2 - 8))
