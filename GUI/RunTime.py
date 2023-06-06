import tkinter as tk
from tkinter import ttk
import os
from tkinter import END
from tkinter import messagebox as msgbox
from PIL import ImageTk, Image #EXTRA LIBRARY --> pip install pillow
import json
from local.aida_utils import AIDAUtils
import time
import subprocess
import asyncio
from constants import *
import signal
import numpy as np
import threading
import queue


class RunTimePage(tk.Frame):
    def __init__(self, parent, controller):
        self.config_file = ''
        self.service_map = {}
        self.service_map_rectangle = {}
        self.background_canvas = None
        self.controller = controller
        self.initialRun = True
        self.n_runs = 1

        self.aida = None
        self.queueInfo = None

        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, weight=0)
        style = ttk.Style()
        style.configure('CustomButton.TButton', font=MEDIUMFONT)

        self.rightFrame = tk.Frame(self, width= 400, height= 100)
        
        buttonsFrame = tk.Frame(self.rightFrame)
        buttonsFrame.grid(column=0, row = 5, pady=40)

        self.rightFrame.pack(side = "right", padx= 50)

        self.topFrame = tk.Frame(self, width=1400)
        
        servicesLabel = ttk.Label(self.topFrame , text= "Services" , font= LARGEFONT)
        servicesLabel.pack(side= "top")
        
        self.topFrame.pack()

        self.backgroundFrame = tk.Frame(self, width= 1400)
        
        self.whiteImage = np.zeros((1200, 900))
        self.background_image = ImageTk.PhotoImage(Image.fromarray(self.whiteImage))
        
        self.background_canvas = tk.Canvas(self.backgroundFrame, width=1200, height=900)
        self.image_on_canvas = self.background_canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        self.background_canvas.pack()

        self.backgroundFrame.pack(side= "left", padx= 50)

        self.servicesLabel = ttk.Label(self.rightFrame, text= "Execution plan", font= LARGEFONT)
        self.servicesLabel.grid(row= 0, column= 0)

        self.serviceslistBox = tk.Listbox(self.rightFrame, width= 60, height= 20, font= XSMALLFONT)
        self.serviceslistBox.grid(column= 0, row= 1, pady=20)

        self.comboBox = ttk.Combobox(self.rightFrame,width= 25, height= 15, font= SMALLFONT, state= "readonly") #readonly avoid the user from entering values arbitarily
        self.comboBox.grid(column= 0, row= 2, pady=5)

        disruptionButton = ttk.Button(self.rightFrame, text="Break", command=self.breakHandler, style= 'CustomButton.TButton')
        disruptionButton.grid(row=3, column=0)

        homeButton = ttk.Button(buttonsFrame, text="Home", command=lambda: self.goHome(), style= 'CustomButton.TButton')
        homeButton.grid(row=1, column=0, padx=10, pady=10)

        self.startButton = ttk.Button(buttonsFrame, text="Start", command= self.start, style= 'CustomButton.TButton') #no action
        self.startButton.grid(row=1, column=1, padx=10, pady=10)

        self.nextButton = ttk.Button(buttonsFrame, text="Next", command=self.next , style= 'CustomButton.TButton', state="disabled") #debug button to reset background to green
        self.nextButton.grid(row=2, column=0, padx=10, pady=10)

        self.killButton = ttk.Button(buttonsFrame, text="Kill", command=self.kill, style= 'CustomButton.TButton', state="disabled") #debug button to reset background to green
        self.killButton.grid(row=2, column=1, padx=10, pady=10)

        self.immediateRunButton = ttk.Button(buttonsFrame, text="Immediate Run", command=self.immediateRun, style= 'CustomButton.TButton')
        self.immediateRunButton.grid(row=3, column=0)

        self.runButton = ttk.Button(buttonsFrame, text="Run", command=self.run, style='CustomButton.TButton')
        self.runButton.grid(row=3, column=1)


    def start(self):
        self.reset_on_start()

        config_json = json.load(open(self.config_file))
        folder = config_json['folder']
        mode = config_json['mode']
        target_file = config_json['target_file']

        app_path = "../local/IndustrialAPI/app.py"
        self.p1 = subprocess.Popen([f"xterm -e python {app_path}"], shell=True, preexec_fn=os.setsid)

        time.sleep(3)

        launch_devices_path = "../local/IndustrialAPI/launch_devices.py"
        self.p2 = subprocess.Popen([f"xterm -e python {launch_devices_path} {folder} {mode}"], shell=True)

        time.sleep(3)

        self.queue = queue.Queue()
        target = os.path.abspath(f"{folder}/{target_file}")
        self.aida = AIDAUtils(target, self.queue)

        asyncio.get_event_loop().run_until_complete(self.aida.compute_policy())

        self.startButton.config(state= "disabled")
        self.nextButton.config(state= "normal")
        self.killButton.config(state= "normal")


    async def _next(self):
        if self.initialRun:
            self.serviceslistBox.insert(END, f"RUN {self.n_runs}")
            self.initialRun = False
        service, previous_state, new_state, executed_action, finished = await self.aida.next_step()
        self.change_rect_color(service, new_state)
        self.serviceslistBox.insert(END, f"{service} : {executed_action} - {previous_state} -> {new_state}")
        if finished:
            self.initialRun = True
            self.n_runs+=1
        #    msgbox.showinfo("Execution completed!", "Execution completed!")
        #    self.startButton.config(state= "normal")
        #    self.nextButton.config(state= "disabled")
        #    self.killButton.config(state= "disabled")
        #    self.kill()

    
    def next(self):
        asyncio.get_event_loop().run_until_complete(self._next())


    def update_gui(self):
        #while self.queue.not_empty:
        elem = self.queue.get()
        print(elem)
        service, previous_state, new_state, executed_action, _ = elem
        self.change_rect_color(service, new_state)
        self.serviceslistBox.insert(END, f"{service} : {executed_action} - {previous_state} -> {new_state}")
        
        self.controller.after(1000, self.update_gui)

    async def _next_finished(self):
        if self.initialRun:
            self.serviceslistBox.insert(END, f"RUN {self.n_runs}")
            self.initialRun = False
        service, previous_state, new_state, executed_action, finished = await self.aida.next_step()
        self.change_rect_color(service, new_state)
        self.serviceslistBox.insert(END, f"{service} : {executed_action} - {previous_state} -> {new_state}")
        if finished:
            self.initialRun = True
            self.n_runs+=1
        return service, previous_state, new_state, executed_action, finished
    

    def _immediateRun_while(self):
        finished = False
        while not finished:
            _,_,_,_,finished = asyncio.get_event_loop().run_until_complete(self._next_finished())
    def _immediateRun(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self._immediateRun_while())
        loop.run_forever()
    def immediateRun(self):
        thread = threading.Thread(target=self._immediateRun)
        thread.start()

    def _run_while(self):
        finished = False
        while not finished:
            _,_,_,_,finished = asyncio.get_event_loop().run_until_complete(self._next_finished())
            time.sleep(2)
    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(self._run_while())
        loop.run_forever()
    def run(self):
        thread = threading.Thread(target=self._run)
        thread.start()


    def kill(self):
        print("Stopping...")
        os.killpg(os.getpgid(self.p1.pid), signal.SIGTERM)
        self.startButton.config(state= "normal")
        self.nextButton.config(state= "disabled")
        self.killButton.config(state= "disabled")


    def refreshComboBox(self): #very ugly way to update items in the listbox
        data = list(self.service_map.keys())
        self.comboBox['values'] = data
        self.comboBox.current(0)
    
    def breakHandler(self):
        highlighted_value = self.comboBox.get() #return the selected value
        
        self.change_rect_red(highlighted_value)


    def set_image_services(self):
        with open(self.config_file) as json_file:
            data = json.load(json_file)
    
        services = data['services']
        self.image_path = f"utils/{data['image_path']}"
        self.folder = data['folder']
        
        self.matrix = [data['matrix'][key] for key in ['rows', 'columns']]

        service_map = {}
        
        for service in services:
            nome_file = service['name_file']
            x = service['x']
            y = service['y']
            label = service['label']

            service_map[label] = (x,y,nome_file)

        self.service_map = service_map
        
        data = list(self.service_map.keys())

        self.background_image = ImageTk.PhotoImage(Image.open(self.image_path).resize((1200,900)))
        self.background_canvas.itemconfig(self.image_on_canvas, image = self.background_image)
        
        step_x = 1200 / self.matrix[1]
        step_y = 900 / self.matrix[0]
        
        for service_label in self.service_map.keys():
            y = self.service_map[service_label][0]
            x = self.service_map[service_label][1]
            x1 = x * step_x
            if x1 == 0: x1 +=1
            y1 = y * step_y
            if y1 == 0: y1 +=1
            rectangle = self.background_canvas.create_rectangle(x1, y1, x1+step_x, y1+step_y, fill="green", stipple="gray50", outline="black")
            self.background_canvas.create_text(x1+step_x/2, y1+step_y/2, text=service_label, font=SERVICE_FONT)
            self.service_map_rectangle[service_label] = rectangle


    def reset_on_start(self):
        for service_label in self.service_map_rectangle.keys():
            self.background_canvas.itemconfig(self.service_map_rectangle[service_label], fill="green", stipple="gray50", outline="black")
        self.serviceslistBox.delete(0, END)


    def change_rect_color(self, service, state):
        match state:
            case "configured":
                self.background_canvas.itemconfig(self.service_map_rectangle[service], fill="gray", stipple="gray50", outline="black")
            case "broken":
                self.background_canvas.itemconfig(self.service_map_rectangle[service], fill="red", stipple="gray50", outline="black")
            case "executing":
                self.background_canvas.itemconfig(self.service_map_rectangle[service], fill="blue", stipple="gray50", outline="black")
            case "repairing":
                self.background_canvas.itemconfig(self.service_map_rectangle[service], fill="yellow", stipple="gray50", outline="black")
            case "ready":
                self.background_canvas.itemconfig(self.service_map_rectangle[service], fill="green", stipple="gray50", outline="black")
      

    def resetPage(self):
        self.config_file = ''
        self.service_map = {}
        self.service_map_rectangle = {}
        self.initialRun = True
        self.n_runs = 1
        
        try:
            self.kill()
        except:
            print("services not killed or already killed")

        self.serviceslistBox.delete(0, END)


    def goHome(self):
        self.controller.get_PreRunTimePage().resetPage()
        self.resetPage()
        self.controller.show_mainPage()