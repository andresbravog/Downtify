
import sys
from Tkinter import *
import urllib
import os
import time
import string

class App:
    
    def __init__(self, master):
        
        frame = Frame(master)
        frame.pack()
        
        
        
        self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
        self.button.pack(side=LEFT)
        
        scrollbar = Scrollbar(master, orient=VERTICAL)
        self.list = Listbox(frame, yscrollcommand=scrollbar.set)
        self.configuration()
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.pack(side=LEFT, fill=BOTH, expand=1)

        self.hi_there = Button(frame, text="Check", command=self.checkin(1))
        self.hi_there.pack(side=LEFT)
        
        self.configuration()
        
    
    def configuration(self):
        #Reader read configuration file
		#self.archive = "spotify-urls.txt"
        #Parsing urls from archive
        f = open('spotify-urls.txt')
        self.urls = []
        for line in f.readlines():
            #line_readed = line.partition(':')
            self.urls += line
            print line
        f.close()
    
    def yview(self, *args):
        apply(self.list.yview, args)
    
    def test_connection(self):
        if os.system("ping -c 2 www.google.com"):
            return False
        else:
            return True


root = Tk()

app = App(root)

root.mainloop()



