# -*- coding: utf-8 -*-

import sys
import subprocess
import os.path
import sqlite3
from audio_wav import *

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
    print("with this version ... I guess it will work ! ")
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox 

from Utils.listes import *

class Menubar(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self, borderwidth=2)
        if parent :
            menu = tk.Menu(parent)
            parent.config(menu=menu)
            fileMenu = tk.Menu(menu)
            fileMenu.add_command(label="Save",command=self.save)
            menu.add_cascade(label="File", menu=fileMenu)

    def save(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)


class MakeNote():
    def __init__(self, parent):
        self.graph=None
        frame1 = tk.Frame(parent)
        frame1.grid(row = 0, column = 0)

        frame2 = tk.Frame(parent)
        frame2.grid(row = 0, column = 1)

        frame3 = tk.Frame(parent)
        frame3.grid(row = 0, column = 2)

        
        self.selectionNote = Selection(frame2)
        self.selectionAccord = Selection(frame3)

        notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.menuNotes = ListMenu(frame1,"note",notes)

        self.octaves=["2","3","4","5"]
        self.menuOctaves = ListMenu(frame1,"octave",self.octaves)

        self.createButtonNotes = tk.Button(frame1,text="Create note",fg="red")
        self.createButtonNotes.bind("<Button-1>",lambda event : self.createNote(event, self.selectionNote))

        self.createButtonAccord = tk.Button(frame1,text="Create accord",fg="red")
        self.createButtonAccord.bind("<Button-1>",lambda event : self.createAccord(event, self.selectionNote, self.selectionAccord ))

    
        self.createPlayNotes = tk.Button(frame2,text="PlayNote",fg="red")
        self.createPlayNotes.bind("<Button-1>",lambda event : self.playNote(event, self.selectionNote))
        
        self.createPlayAccord = tk.Button(frame3,text="PlayAccord",fg="red")
        self.createPlayAccord.bind("<Button-1>",lambda event : self.playAccord(event, self.selectionAccord))

        self.createButtonDeleteNote = tk.Button(frame2,text="deleteNote",fg="red")
        self.createButtonDeleteNote.bind("<Button-1>",lambda event : self.removeNote(event, self.selectionNote))

        self.createButtonDeleteAccord = tk.Button(frame3,text="deleteAccord",fg="red")
        self.createButtonDeleteAccord.bind("<Button-1>",lambda event : self.removeAccord(event, self.selectionAccord))


    """
    def callback(self, event):
        mw.destroy()
    """
    def createNote(self, event, selection):
        data = []
        note = str(self.menuNotes.get_note() + self.menuOctaves.get_note())
    
        print(note)
        selection.insert(note)
        notes = selection.getData()
        if not os.path.isfile("Sounds/"+ note +".wav"):
                connect = sqlite3.connect("Audio/frequencies.db")
                cursor = connect.cursor()
                for note in notes : 
                    key = note[:-1]
                    octave = note[-1:]
                    
                    
                    if '#' in key:
                        key_search = key[0] + "Sharp"
                    else:
                        key_search = key

                    result=cursor.execute("SELECT " + key_search +  " FROM frequencies WHERE octave=" + str(octave) + ";")
                    freq=result.fetchone()[0]
                    self.graph.set_frequence(freq)  

                    data = sinus_wav(filename='sinus.wav',f=freq,framerate=8000,duration=2)   
                                        
                save_wav("Sounds/"+note+".wav",data,8000)
        
    
    def playNote(self, event, selectionNote):
        notes = selectionNote.getData()
        connect = sqlite3.connect("Audio/frequencies.db")
        cursor = connect.cursor()
        for note in notes:
            key = note[:-1]
            octave = note[-1:]
                    
                    
            if '#' in key:
                key_search = key[0] + "Sharp"
            else:
                key_search = key

            result=cursor.execute("SELECT " + key_search +  " FROM frequencies WHERE octave=" + str(octave) + ";")
            freq=result.fetchone()[0]
            if self.graph:
                self.graph.set_frequence([freq])
            subprocess.call(["aplay","Sounds/"+note+".wav"])
    
    def playAccord(self, event, selection):
        accords = selection.getData()
        for accord in accords:
            subprocess.call(["aplay","Sounds/"+accord+".wav"])
        if self.graph:
            freqs = []
            notes = []
            note=""
            connect = sqlite3.connect("Audio/frequencies.db")
            cursor = connect.cursor()
            accord = accord[:-4]
            while True:
                print(accord)
                note += accord[0]
                if accord[0] in self.octaves:
                    notes.append(note)
                    note=""
                if len(accord) <=1: 
                    break
                accord=accord[1:]
            print(notes)
            for note in notes:
                key = note[:-1]
                if "#" in key:
                    key = key[0]+"Sharp"
                octave = note[-1:]
                print(key, octave)

                result=cursor.execute("SELECT "+key+" FROM frequencies WHERE octave="+note[-1:]+";")
                freqs.append(result.fetchone()[0])
            print(freqs)
            
            self.graph.set_frequence(freqs)
            connect.commit()
            
    
    def createAccord(self, event, selection, selectionAccord):        
        if len(selection.getData()) >= 3 :
            accord = ""
            data = []
            
            notes = selection.getData()
            for note in notes:
                accord+=note 
            selectionAccord.insert(accord)
            if not os.path.isfile("Sounds/"+ accord +".wav"):
                connect = sqlite3.connect("Audio/frequencies.db")
                cursor = connect.cursor()
                for note in notes : 
                    key = note[:-1]
                    octave = note[-1:]
                    if '#' in key:
                        key_search = key[0] + "Sharp"
                    else:
                        key_search = key

                    result=cursor.execute("SELECT " + key_search +  " FROM frequencies WHERE octave=" + str(octave) + ";")
                    print(result)
                    freq=result.fetchone()[0]

                    nextData = sinus_wav(filename='sinus.wav',f=freq,framerate=8000,duration=2)

                    if len(data)==0:
                        data = nextData   
                        
                    for i in range(0, len(nextData)):
                        data[i] += nextData[i]                     
                            
                  
                    
                save_wav("Sounds/"+accord+".wav",data,8000)
        else:
            messagebox.showinfo('Warning','Il faut minimum trois notes')
                    
                
                    
        
    def removeNote(self, event, selection):
        selection.deleteNote()
    
    def removeAccord(self, event, selection):
        selection.deleteAccord()
        print(selection.getData())

    def attach_graphnote(self, graph):
        self.graph = graph




    def packing(self):
        self.selectionNote.packing()
        self.selectionAccord.packing()
        self.menuNotes.packing()
        self.menuOctaves.packing()
        self.createButtonNotes.pack()
        self.createPlayNotes.pack()
        self.createButtonAccord.pack()
        self.createPlayAccord.pack()
        self.createButtonDeleteNote.pack()
        self.createButtonDeleteAccord.pack()





if __name__ == "__main__" :

    mw=tk.Tk()
    
    mw.geometry("360x300")
    mw.title("Generateur de fichier au format WAV")
    #menubar=Menubar(mw)
    #frame=tk.LabelFrame(mw, text="Generator ",borderwidth=5,width=600,height=300,bg="pink")
    #notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    #selection= Selection(frame)
    #menu=ListMenu(frame,"notes",notes,selection)
    #menu.packing()
    #selection.packing()
    
    #frame.pack()
    
    note = MakeNote(mw)
    note.packing()
    mw.mainloop()


    """
    mw=tk.Tk()
    #mw.option_readfile("hello.opt")
    label_hello=tk.Label(mw,text="Hello World !")
    label_bonjour=tk.Label(mw,name="labelBonjour")
    button_quit=tk.Button(mw,text="Goodbye World !")
    label_hello.pack()
    label_bonjour.pack()
    button_quit.pack()
    mw.mainloop() """
    