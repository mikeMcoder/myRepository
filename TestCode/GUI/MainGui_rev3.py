# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:54:42 2019

@author: michael.mercado
"""
import Tkinter as Tk

#create class MainGui
#esablish the size of the rootwindow

class CheckButton():
    def __init__(self, main, text, row = None):
        self.var = Tk.IntVar()
        self.text=text
        c = Tk.Checkbutton(
            main, activebackground = "red",\
            activeforeground = "yellow",\
            bg = "blue",\
            bitmap = None,\
            text=text,\
            height = 3,\
            variable=self.var,\
            command=self.check)
        
        c.grid(row = row, column = 5)
        
    
    def check(self):
        try:
            self.var1 = self.var.get()
            print (self.text, "is", self.var1)
            return self.var1
        except:
            raise

class StartButton():
    def __init__(self):
        pass
    

class MainGui:
    def __init__(self):
        
        self.root = Tk.Tk()         #get the root window
        self.root.title("RT GUI")   # add a title to the root window
        self.root.geometry("800x500")# this is the size of the main window
        #layout containers
        self.root.grid_rowconfigure(1, weight = 1)
        self.root.grid_columnconfigure(0, weight = 1)
 
 
        #create the containers or frames color blue
        self.frame = Tk.Frame(main = self.root,bg = 'blue', width=500, height=500,\
                              pady = 1)
        self.label = Tk.Label(self.frame,text ="NANO RT")
        self.label.grid(row = 0, sticky = 'n')
       
        #assign a location for this frame
        self.frame.grid(row = 0, sticky = 'sw')
        
        
        #add the check buttons
        self.addCheckbutton()
        
        
        
   
    def addCheckbutton(self):
        self.check1 = CheckButton(self.frame,text="RandomFrequencyTest", row = 0)
        self.check2 = CheckButton(self.frame, text="RandomPowerTest",  row = 1)
        self.check3 = CheckButton(self.frame, text="RandomFtfTest", row = 2)
        
        #place the checkbuttons in the correct spot
        
        
    def sampleProgram(self):
        print ("Running a program...")
        
    def RunEngine(self):
        
        
        try:
            self.check1(command = self.sampleProgram)
            
        except:
            pass
            
        
        
#initialize parameters
#create root window
#create selection buttons
#attach start button
#attach stop button


if __name__=='__main__':
    gui = MainGui()
    gui.root.mainloop()
    
    