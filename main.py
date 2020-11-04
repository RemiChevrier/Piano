# -*- coding: utf-8 -*-

import sys

print("Your platform is : " ,sys.platform)
major=sys.version_info.major
minor=sys.version_info.minor
print("Your python version is : ",major,minor)
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox

elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox

else :
    print("with your python version : ",major,minor)
    print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 
    from tkinter import messagebox


from math import pi,sin
import collections
import subprocess
from observer import *
from piano import *
from wave_visualizer import *
from wave_generator import *
from keyboard import *
from Utils.menubar import *

mw = tk.Tk()
mw.geometry("1600x700")
mw.title("Leçon de Piano")

label_hello=tk.Label(mw, text="Hello Mozart !",fg="blue")
#button_quit=tk.Button(mw, text="Goodbye Mozart", fg="red", command=mw.destroy)
label_hello.pack()
#button_quit.pack(side="bottom")

model = Model()
model.generate_signal()

viewFrame=tk.Frame(mw,borderwidth=5,width=360,height=300)

view=View(viewFrame)
view.grid(5)
view.packing()
view.update(model)


model.attach(view)


octaves=4
framePiano=tk.Frame(mw,borderwidth=5,width=360,height=300)
piano=Piano(framePiano,octaves)
piano.attach_graph(model)


framePiano.place(relx=0.35, rely=0.24, height=59, width=106)
framePiano.pack()
viewFrame.pack()  
"""
menubar=Menubar(mw)
frameGen=tk.LabelFrame(mw, text="Generator ",borderwidth=5,width=400,height=300,bg="pink")
notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
selection= Selection(frameGen)
menu=ListMenu(frameGen,"notes",notes,selection)
menu.packing()
selection.packing()
"""

frameGen = tk.Frame(mw)
frameGen.pack(side="left", fill='y')
makenote = MakeNote(frameGen)
makenote.attach_graphnote(model)
makenote.packing()

menubar = Menubar(mw)
mw.config(menu = menubar.menu)

mw.mainloop()
