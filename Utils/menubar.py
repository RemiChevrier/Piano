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
    print("with this version ... I guess it will work ! ")
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
class Menubar():
    def __init__(self, parent):
        self.menu = tk.Menu(parent)

        self.fileMenu = tk.Menu(self.menu)
        #self.fileMenu.add_command(label="Item")
        self.fileMenu.add_command(label="Exit", command=self.exitProgram)
        #fileMenu.add_command(label="Exit", command=self.create(self.master))
        self.menu.add_cascade(label="File", menu=self.fileMenu)

        self.helpMenu = tk.Menu(self.menu)
        self.helpMenu.add_command(label="Creator", command=self.creator)
        self.helpMenu.add_command(label="Thanks", command = self.thanks)
        self.menu.add_cascade(label="Help", menu=self.helpMenu)

    def exitProgram(self):
        MsgBox = messagebox.askquestion ('Exit App','Really Quit?',icon = 'error')
        if MsgBox == 'yes':
            exit()
        else:
            messagebox.showinfo('Welcome Back','Welcome back to the App')
    
    def creator(self):
        messagebox.showinfo('Creator','Rémi Chevrier')
    
    def thanks(self):
        messagebox.showinfo(' Thanks','Thanks tkInter for your support')    
   


if __name__ == "__main__" :
    mw = tk.Tk()
    mw.wm_title("Tkinter window")
    """
    btn = tk.Button(mw, text="Créer une nouvelle fenêtre", command = self.create)
    btn.pack(pady = 10) """
    menubar = Menubar(mw)
    mw.config(menu = menubar.menu)
    mw.mainloop()