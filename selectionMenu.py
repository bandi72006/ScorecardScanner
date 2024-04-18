from easygui import *

class selectionMenu:
    def __init__(self):
        #Talk about like static class or sumn (look at todo list)
        pass

    def draw(self, function, **kwargs):
        #USE SELENIUM TO SCRAPE INFORMATION

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