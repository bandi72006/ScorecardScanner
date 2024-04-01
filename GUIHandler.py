import pygame
from button import *
from image import *
from text import *
from cameraFeed import *
import time

class GUI:
    def __init__(self, dimensions):
        pygame.init()
        self.__screen = pygame.display.set_mode(dimensions)
        pygame.display.set_caption("WCA Scorecard Scanner")

        #0 = Main menu
        #1 = Data entry menu
        #2 = statistics menu
        #3 = export data menu
        #4 = configuration menu
        #5 = Scanner menu


        self.__currentScreen = 0
        self.__mainMenu = [Button(self.__screen, (315,300), (300,100), "Data entry", "M1"), 
                           Button(self.__screen, (665,300), (300,100), "Statistics", "M2"),
                           Button(self.__screen, (315,425), (300,100), "Export data", "M3"),
                           Button(self.__screen, (665,425), (300,100), "Configuration", "M4"),
                           Button(self.__screen, (490,550), (300,100), "Exit", "E", (255,94,94), (255,33,33)),
                           Image(self.__screen, "WCALogo.png", (350,30), (200,200)),
                           Text(self.__screen, "Data Enterer", (580, 110), 60)
                           ]
        
        self.__dataEntryMenu = [Button(self.__screen, (440,200), (400,125), "Scan new card", "M5"),
                                Button(self.__screen, (440,400), (400,125), "Edit competition results", "O"),
                                Button(self.__screen, (530,600), (200,75), "Back", "M0", (255,94,94), (255,33,33)),
                                Image(self.__screen, "WCALogo.png", (1170,610), (100,100)),
                                Text(self.__screen, "Data Entry", (50, 30), 80)
                                ]

        self.__scannerMenu = [Button(self.__screen, (1060, 260), (150,150), "", ""),
                              Image(self.__screen, "cameraIcon.png", (1070, 285), (130,100)),
                              Text(self.__screen, "or press Space", (1060,420), 20),
                              Image(self.__screen, "WCALogo.png", (1170,610), (100,100)),
                              Text(self.__screen, "Take photo", (50, 30), 50),
                              Camera(self.__screen, (460,100), (480,360)),
                              Button(self.__screen, (540,600), (200,75), "Back", "M0", (255,94,94), (255,33,33))
                              ]

        self.__statsMenu = [Button(self.__screen, (1170,610), (100,100), "Back", "M0", (255,94,94), (255,33,33))]

        self.__exportDataMenu = [Button(self.__screen, (1170,610), (100,100), "Back", "M0", (255,94,94), (255,33,33))]

        self.__configMenu = [Button(self.__screen, (1170,610), (100,100), "Back", "M0", (255,94,94), (255,33,33))]

        self.__menuDict = {0: self.__mainMenu, 1: self.__dataEntryMenu, 2: self.__statsMenu,
                           3: self.__exportDataMenu, 4: self.__configMenu, 5: self.__scannerMenu}


    def getCurrentScreen(self):
        return self.__currentScreen
        
    def setCurrentScreen(self, menuNum):
        self.__currentScreen = menuNum

    def draw(self):
        clickTime = 0 #Not set as attribute as only used within this function
        while True:
            #Drawing
            registeredClicks = pygame.mouse.get_pressed() #0th element = left click

            
            #Held down left click also clicks buttons on next menu
            if time.time() - clickTime > 0.5 and registeredClicks[0]: #Must include delay to allow mouse to be unclicked
                isClick = True
                clickTime = time.time()
            else:
                isClick = False
            mousePos = pygame.mouse.get_pos()


            self.__screen.fill((255,255,255))
            for element in self.__menuDict[self.getCurrentScreen()]:
                element.draw(mousePos, isClick, self.setCurrentScreen)

            pygame.display.flip()


            #Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break

        