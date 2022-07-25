import tkinter as tk
from tkinter import filedialog
from tkinter import *
import os
import shutil
import sqlite3
import time as t

src = ""
dst = ""
file_names = ""


class Setup(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args,**kwargs)

        self.title("File Replacer")
        self.resizable(width=False, height=False)
        self.frames = {}

        #frame that will hold all the frames
        container = tk.Frame(self)
        container.grid(row=0,column=0, sticky="nsew")
        container.columnconfigure(0,weight=1)
        container.rowconfigure(0,weight=1)


        #listing frames (pages) to be controlled and stacking them ontop of each other
        #for F in (Main):
        frame = Main(parent=container, controller=self)
        self.frames[Main] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Main)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


class Main(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self,parent,*args, **kwargs)

        self.conn = sqlite3.connect("dirs.db")
        self.c = self.conn.cursor()

        label1 = tk.Label(self, text = "Mods Folder:")
        label2 = tk.Label(self, text = "Extracted Game:")

        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0)

        self.e1 = tk.Entry(self, width = 80)
        self.e1.grid(row=0, column = 1)

        self.e2 = tk.Entry(self, width = 80)
        self.e2.grid(row =1, column=1)

        getDir = tk.Button(self, text = "Get Mods Folder", width = 18, command = self.getModsDir)
        getDir.grid(row=0, column=2)

        getEx = tk.Button(self, text = "Get Extracted Game", width = 18, command = self.getMkDir)
        getEx.grid(row=1, column=2)

        apply = tk.Button(self, text = "Apply Mods", width = 12, command = self.merge)
        apply.grid(row=2, column=1, sticky = "w")

        runGame = tk.Button(self, text = "Run Game", width = 12, command = self.run)
        runGame.grid(row=2, column=1, sticky = "e")

        setDefault1 = tk.Button(self, text = "Set as Default Path",command = self.setMods)
        setDefault1.grid(row=0, column=3)

        setDefault2 = tk.Button(self, text = "Set as Default Path", comman = self.setSrc)
        setDefault2.grid(row=1, column=3)

        self.insertData()
    
    def insertData(self):
        try:
            self.c.execute("""
            SELECT dir
            FROM main
            WHERE id = ?1
            """, (2,))

            dir = self.c.fetchall()[0][0]

            if dir == "None":
                pass
            else:
                self.e1.insert(0, dir)
        except:
            pass
        
        try:
            self.c.execute("""
            SELECT dir
            FROM main
            WHERE id = ?1
            """, (1,))

            dir = self.c.fetchall()[0][0]
            
            if dir == "None":
                pass
            else:
                self.e2.insert(0, dir)
        except:
            pass
    
    def setSrc(self):
        src = self.e2.get()

        self.c.execute("""
        UPDATE main
        SET dir = ?1
        WHERE id = ?2
        """, (src, 1,))
        
        self.conn.commit()
    
    def setMods(self):
        mods = self.e1.get()

        self.c.execute("""
        UPDATE main
        SET dir = ?1
        WHERE id = ?2
        """, (mods, 2,))

        self.conn.commit()


    def getMkDir(self):
        self.e2.delete(0, END)
        dir = filedialog.askdirectory()
        self.e2.insert(0, dir)
        pass

    def getModsDir(self):
        self.e1.delete(0, END)
        dir = filedialog.askdirectory()
        self.e1.insert(0, dir)
        pass
    
    def merge(self):
        mods = self.e1.get()
        src = self.e2.get()
        file_names = os.listdir(mods)

        print(file_names)

        for root_dirs, dirs, files in os.walk(src):
            for files in files:
                if files in file_names:
                    shutil.copy(os.path.join(mods,files), os.path.join(root_dirs,files))
                
        status = "Applied Changes"
        self.statusWin(status)
    
    def statusWin(self, status):
        window = tk.Toplevel(self)
        window.geometry("100x100")

        window.resizable(width=False, height=False)
        for i in range(5):
            window.columnconfigure(i, weight = 1)
            window.rowconfigure(i, weight=1)
        
        statusLabel = tk.Label(window, text = status)
        statusLabel.grid(row=2, column=2)

        window.grab_set()
    
    def run(self):
        try:
            os.startfile(self.e2.get() + "//sys//main.dol")
        except:
            status = "Make sure main.dol files\nare set to run with Dolphin"
            self.statusWin(status)


program = Setup()
program.mainloop()