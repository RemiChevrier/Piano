# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
print("Your platform is : " ,sys.platform)
major=sys.version_info.major
minor=sys.version_info.minor
print("Your python version is : ",major,minor)
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    print("with your python version : ",major,minor)
    print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin,cos
from observer import *

class Model(Subject) :
    def __init__(self):
        Subject.__init__(self)
        self.a,self.f,self.p=1.0,[2.0],0.0
        self.signal=[]

    def vibration(self,t,impair=True):
        a,freqs,p=self.a,self.f,self.p
        somme=0
        print(freqs)
        for f in freqs:
            print(f)
            somme=somme + a*sin(2*pi*int(f)*t-p)
        return somme
        
    def generate_signal(self,period=2,samples=100.0):
        del self.signal[0:]
        echantillons=range(int(samples)+1)
        Tech = period/samples
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        self.notify()
        return self.signal
    def set_magnitude(self,newa):
        self.a=newa
    def set_frequence(self,newb):
        self.f = newb
        print("setfrequence")
        self.generate_signal()
    def set_pulsation(self,newp):
        self.p = newp
        

class View(Observer) :
    def __init__(self,parent,bg="white", width=600,height=300):
        self.canvas=tk.Canvas(parent,bg=bg,width=width,height=height)
        self.a,self.f,self.p=10.0,2.0,0.0
        self.width,self.height=width,height
        self.units=1
        self.canvas.bind("<Configure>",self.resize)
   
    def update(self, model):
        print("View : update()")
        self.signal = model.signal
        if self.signal :
            self.canvas.delete("sound")
            self.plot_signal(self.signal)

    def plot_signal(self,signal,color="red"):
        w,h=self.width,self.height
        signal_id=None
        if signal and len(signal) > 1:
            print(self.units)
            plot = [(x*w,h/2.0*(1-y*1.0/(self.units/2.0))) for (x, y) in signal]
            signal_id=self.canvas.create_line(plot, fill=color, smooth=1, width=3,tags="sound")
        return signal_id

    def grid(self,steps=2):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")

    def resize(self,event):
        if event:
            self.width,self.height=event.width,event.height
            self.canvas.delete("grid")
            # self.canvas.delete("sound")
            # self.plot_signal(self.signal)
            self.grid(self.units)

    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)

class Controller(object) :
    def __init__(self, parent, model, view):
        self.model, self.view = model, view
        self.create_controls(parent)
        
    def create_controls(self, parent):
        self.frame=tk.LabelFrame(parent,text='Signal')
        self.amp=tk.IntVar()
        self.amp.set(1)
        self.scaleA=tk.Scale(self.frame,variable=self.amp, label="Amplitude", orient="horizontal",length=250, from_=0,to=5,tickinterval=1)
        self.scaleA.bind("<Button-1>",self.update_magnitude)
        self.freq=tk.IntVar()
        self.freq.set(10)
        self.scaleB=tk.Scale(self.frame,variable=self.freq, label="Fréquence", orient="horizontal",length=250, from_=0,to=10,tickinterval=1)
        self.scaleB.bind("<Button-1>",self.update_frequence)
        self.puls=tk.IntVar()
        self.puls.set(10)
        self.scaleC=tk.Scale(self.frame,variable=self.puls, label="Fréquence", orient="horizontal",length=250, from_=-10,to=10,tickinterval=1)
        self.scaleC.bind("<Button-1>",self.update_pulsation)
    
    def update_magnitude(self,event):
        self.model.set_magnitude(self.amp.get())
        self.model.generate_signal()
    def update_frequence(self,event):
        self.model.set_frequence(self.freq.get())
        self.model.generate_signal()
    def update_pulsation(self,event):
        self.model.set_pulsation(self.puls.get())
        self.model.generate_signal()
    def packing(self):
        self.frame.pack()
        self.scaleA.pack()
        self.scaleB.pack()
        self.scaleC.pack()

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    mw.title("Visualisation de signal sonore")
    frame=tk.LabelFrame(mw, text="Signal Visualizer",borderwidth=5,width=400,height=300,bg="yellow")
    # frame=tk.Frame(mw,borderwidth=5,width=360,height=300,bg="green")
    frame.pack()

    view=View(frame)
    view.grid(4)
    view.packing()
    model = Model()
    model.attach(view)
    model.generate_signal()
    ctrl=Controller(mw,model,view)
    view.packing()
    ctrl.packing()
    mw.mainloop()
