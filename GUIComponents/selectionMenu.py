import tkinter as tk
from config import *

class selectionMenu:
    def __init__(self):
        self.__window = tk.Tk() 
        self.__window.title('WCA Scorecard scanner') 
        self.__window.geometry('500x100') 

    def draw(self, function, *argv): #1st argv: getText, 2nd argv: setText
        #E - Event selection
        #C - Competitor selection
        #T - Edit time
        #CL - Edit competition link
        #CN - Edit competition name
        #CE - Edit events in comp (for config)

        if function == "E": #Event selection
            self.__window.geometry('100x400')

            self.__selectedEvent = ""
            events = config.getEvents()

            self.__list = tk.Listbox(self.__window, selectmode = "single", height=20) 
            self.__list.pack()
            for i in range(len(events)): 
                self.__list.insert(tk.END, events[i])  

            self.__okButton = tk.Button(self.__window, text = "Select event", command=self.__selectEvent)
            self.__okButton.pack()
        
            self.__window.mainloop() 
            
            argv[1](self.__selectedEvent) #Sets button label
            return self.__selectedEvent
        

        if function == "C": #Competitor selection
            self.__window.geometry('100x400')

            self.__selectedCompetitor = ""
            competitors = config.getCompetitors()

            self.__list = tk.Listbox(self.__window, selectmode = "single", height=20) 
            self.__list.pack()
            for i in range(len(competitors)): 
                self.__list.insert(tk.END, competitors[i])  

            self.__okButton = tk.Button(self.__window, text = "Select competitor", command=self.__selectCompetitor)
            self.__okButton.pack()
        
            self.__window.mainloop() 
            
            argv[1](self.__selectedCompetitor) #Sets button label
            return self.__selectedCompetitor
        
        if function == "T": #Time edit
            #Grabs current time
            self.__newTime = argv[0]()
            self.__textBox = tk.Text(self.__window, height = 2, width = 52, bg = "light yellow")
            self.__textBox.insert(tk.END, str(self.__newTime))
            self.__okButton = tk.Button(self.__window, text = "Confirm time", command=self.__confirmTime)

            self.__textBox.pack()
            self.__okButton.pack()

            self.__window.mainloop()
            argv[1](self.__newTime)   #Sets button label 


        if function == "CN": #Edit competition name
            #Private attributes vs variables so can be accessed by other methods within class
            self.__textBox = tk.Text(self.__window, height = 2, width = 52, bg = "light yellow")
            self.__okButton = tk.Button(self.__window, text = "Submit name", command=self.__configName)
            self.__textBox.pack()
            self.__okButton.pack()
            self.__window.mainloop()


        if function == "CL": #Edit competition link
            #Private attributes vs variables so can be accessed by other methods within class
            self.__textBox = tk.Text(self.__window, height = 2, width = 52, bg = "light yellow")
            self.__okButton = tk.Button(self.__window, text = "Submit link", command=self.__configLink)
            self.__textBox.pack()
            self.__okButton.pack()
            self.__window.mainloop()

        if function == "CE": #Edit events in comp (for config)
            self.__window.geometry('300x400') 

            #Labels
            #Used to iterate over and create labels for each
            self.__events = ["3x3", "2x2", "4x4", "5x5", "6x6", "7x7", "3BLD", "FMC", "OH", "Clock", "Mega", "Pyra", "Skewb", "SQ1", "4BLD", "5BLD", "MBLD"]
            self.__eventLabels = [tk.Label(self.__window, text=event) for event in self.__events]
            for i in range(len(self.__eventLabels)):
                self.__eventLabels[i].grid(row = i, column = 0)

            #Spinboxes
            self.__spinBoxes = [tk.Spinbox(self.__window, from_ = 0, to = 4) for _ in self.__events]
            for i in range(len(self.__eventLabels)):
                self.__spinBoxes[i].grid(row = i, column = 1)

            self.__okButton = tk.Button(self.__window, text = "Confirm events", command=self.__configEvents)
            self.__okButton.grid(row = len(self.__events), column = 0)

            self.__window.mainloop()

    
    def __configName(self):
        name = self.__textBox.get("1.0",'end-1c') #Get value from textbox
    
        config.editCompName(name)
        self.__window.destroy()

    def __configEvents(self):
        eventsDict = {}
        for i in range(len(self.__events)):
            if int(self.__spinBoxes[i].get()) != 0: #Only add events that are in comp
                eventsDict[self.__events[i]] = int(self.__spinBoxes[i].get())
            
        config.editCompEvents(eventsDict)
        self.__window.destroy()

    def __configLink(self):
        link = self.__textBox.get("1.0",'end-1c') #Get value from textbox
        
        config.editCompLink(link)
        self.__window.destroy()

    def __selectCompetitor(self):
        self.__selectedCompetitor = self.__list.get(tk.ANCHOR) 

        self.__window.destroy()

    def __selectEvent(self):
        self.__selectedEvent = self.__list.get(tk.ANCHOR) 

        self.__window.destroy()

    def __confirmTime(self):
        self.__newTime = self.__textBox.get("1.0",'end-1c') 

        self.__window.destroy()
