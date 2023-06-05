from tkinter import ttk
import tkinter as tk
from ServiceStatePageClass import ServiceStatePage
from RunTimePageClass import RunTimePage
from InstancePlanningPageClass import InstancePlanningPage
from StochasticPolicyPage import StochasticPolicyPage
from StochasticConstraintsBasedPolicy import StochasticConstraintsBasedPolicy
from tkinter import filedialog
from tkinter import Text
from tkinter import END
import tkinter.messagebox as msgbox
import os
import tkinter.font as font
import json
import tkinter as tk
from constants import *


class tkinterApp(tk.Tk):
    
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
       
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        self.geometry("1920x1080")
        container = tk.Frame(self)
        self.title("Adaptive Software")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #container.grid(side = "top", fill = "both", expand = True)
        container.grid(row=0, column=0, sticky= "nsew")
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
        # iterating through a tuple consisting of the different page layouts
        for F in (StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, ServiceStatePage):
            frame = F(container, self)
            
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky ="nsew")
        
        self.show_frame(StartPage) #THIS CALL WILL LOAD THE FIRST PAGE, IT ACCEPTS THIS CLASSES : StartPage, InstancePlanningPage, StochasticPolicyPage, StochasticConstraintsBasedPolicy, RunTimePage, ServiceStatePage)
        
 
    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


    def show_ServiceStatePage(self):
        self.show_frame(ServiceStatePage)
    

    def getFrame(self, cont):
        return self.frames[cont]
    

    def get_ServiceStatePage(self):
        return self.frames[ServiceStatePage]
    

    def get_RunTimePage(self):
        return self.frames[RunTimePage]
    

    def show_mainPage(self):
        self.show_frame(StartPage)


    #This method check the selected radio button and call showframe function
    def checkRadio(self, temp, radioStatus):
        if radioStatus.get() == 2: #if RunTime RadioButton has been selected 
            self.show_frame(RunTimePage) #tell show_frame to load runTimePage
            config_file = filedialog.askopenfilename(
                title="Select the config file",
                initialdir="./config_files"
            )
            while not config_file:
                msgbox.showerror("Error", "Please select a file")
                config_file = filedialog.askopenfilename(
                    title="Select the config file",
                    initialdir="./config_files"
                )
            config_json = json.load(open(config_file))
            folder = config_json['folder']
            if not os.path.isdir(folder):
                msgbox.showerror("Error", "The folder specified in the config file does not exist")
                self.show_mainPage()
                return
            
            temp : RunTimePage = self.getFrame(RunTimePage)
            temp.config_file = str(config_file)
            #temp.check_files_config()
            temp.set_files()

            temp = self.getFrame(ServiceStatePage)
            temp.config_file = str(config_file)
            temp.set_image_services()
            temp.refreshComboBox()
        else:                      #DesignTime RadioButton has been selected
            self.show_frame(temp)
            folder = filedialog.askdirectory(
                title='Select the folder', #name of the tab
                initialdir="./", #initial shown directory
            )
            while not folder:
                msgbox.showerror("Error", "Please select a folder")
                folder = filedialog.askdirectory(
                    title='Select the folder', #name of the tab
                    initialdir="./", #initial shown directory
                )
            try:
                os.mkdir(folder)
            except:
                print()
            temp = self.getFrame(temp) #retrive the frame instance, otherwise it uses the generic class 
            temp.path = str(folder)
            temp.refreshListBox()          


# first window frame startpage  --START PAGE--
class StartPage(tk.Frame):
    def __init__(self, parent, controller : tkinterApp):
        
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=1)
        self.option_add("*Font","aerial") #change font size 
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=MEDIUMFONT) 
    
        # label of frame
        label = ttk.Label(self, text ="Adaptive 0.2", font = LARGEFONT)
        label.grid(row = 0, column =0, padx = 10, pady = 10)
  
        # button planning
        button1 = ttk.Button(self, text ="Instance planning",
            command = lambda : controller.checkRadio(InstancePlanningPage, selected_value),
            style='CustomButton.TButton',
            width= 30
        )
        button1.grid(row = 1, column = 0, padx = 10, pady = 10)
  
        # button stochastic policy
        button2 = ttk.Button(self, text ="Stochastic policy",
            command = lambda : controller.checkRadio(StochasticPolicyPage, selected_value),
            style='CustomButton.TButton',
            width= 30
        )
        button2.grid(row = 2, column = 0, padx = 10, pady = 10)
  
        # button stochastic constraint-based policy
        button3 = ttk.Button(self, text ="Stochastic constraint-based policy",
            command = lambda : controller.checkRadio(StochasticConstraintsBasedPolicy, selected_value),
            style='CustomButton.TButton',
            width= 30
        )
        button3.grid(row = 3, column = 0, padx = 10, pady = 10)

        selected_value = tk.IntVar()
        style.configure('TRadiobutton', font=MEDIUMFONT)
        designTime = ttk.Radiobutton(
            self,
            text='Design Time',
            value=1,
            variable=selected_value,
            style= 'TRadiobutton'
        )  
        designTime.grid(row = 4, column = 0, padx = 5)
        designTime.invoke() # highlights the first radio button, without it there would be the two buttons blank

        runTime = ttk.Radiobutton(
            self,
            text='Run Time',
            value=2, #Value 2 is related to runtime
            variable=selected_value,
            style= 'TRadiobutton'
        )
        runTime.grid(row = 5, column = 0, padx = 5)


# Driver Code
app = tkinterApp() ##app corresponds to the object app, its attributes are: 
app.mainloop()