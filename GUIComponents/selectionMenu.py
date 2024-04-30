from easygui import *
import tkinter as tk
from tkinter import ttk
from config import *

class selectionMenu:
    def __init__(self):
        self.__window = tk.Tk() 
        self.__window.title('Combobox') 
        self.__window.geometry('500x100') 

    def draw(self, function, *argv): #1st argv: getText, 2nd argv: setText
        #E - Event selection
        #C - Competitor selection
        #T - Edit time
        #CL - Edit competition link

        if function == "E": #Event selection

            events = ["2x2R1", "2x2R2", "3x3R1", "3x3R2", "3x3R3", "PyraminxR1", "PyraminxR2",
                      "4x4R1", "SkewbR1", "SkewbR1"]

            output = choicebox("", "Select event: ", events)
            return output

        if function == "C": #Competitor selection
            competitors = ["Bandar Alaish", "Max Park", "Cary Huang", "Dana Yi", "Aysha Jamsheer",
                           "Baha Alshwaiki"]
            
            output = choicebox("", "Select event: ", competitors)
            return output
        
        if function == "T": #Time edit
            #Grabs current time
            time = argv[0]()
            newTime = textbox("Edit time:", "Edit time:", time)
            argv[1](newTime)        


        if function == "CL": #Edit competition link
            #Private attributes vs variables so can be accessed by other methods within class
            self.__textBox = tk.Text(self.__window, height = 2, width = 52, bg = "light yellow")
            self.__okButton = tk.Button(self.__window, text = "submit link", command=self.__configOnClose)
            self.__textBox.pack()
            self.__okButton.pack()
            self.__window.mainloop()


    def __configOnClose(self):
        value = self.__textBox.get("1.0",'end-1c') #Get value from textbox
        
        editCompLink(value)
        self.__window.destroy()