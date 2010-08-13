
import sys
from Tkinter import *
import urllib2, urllib
import webbrowser
import os
import time
import string
from HTMLParser import HTMLParser


class SpiderParser(HTMLParser):

    def __init__(self, filename):
        HTMLParser.__init__(self)
        #f = open( filename ).read()
        self.readedInfo = ""
        self.feed(open( filename ).read())
         

    def handle_starttag(self, tag, attrs):
        if tag == 'h1' and attrs:
            for attribute in attrs:
                if (attribute[0] == 'title'): #&& (attribute[0] == 'title')
                    print "Parsed the song info => %s" % attribute[1]
                    self.readedInfo = attribute[1]
    def getParsedInfo(self):
        print "sending the info from the parser "+ self.readedInfo
        return self.readedInfo



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
        
        scrollbar2 = Scrollbar(master, orient=VERTICAL)
        self.list2 = Listbox(frame, yscrollcommand=scrollbar.set)
        self.configuration()
        scrollbar2.config(command=self.yview)
        scrollbar2.pack(side=RIGHT, fill=Y)
        self.list2.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.button_get_info = Button(frame, text="GET SONGS", fg="red", command=self.getSongsInfo)
        self.button_get_info.pack(side=RIGHT)
        
        self.configuration()
        
    
    def configuration(self):
        #Reader read configuration file
        self.archive = "spotify-urls.txt"
        #Parsing urls from archive
        f = open('spotify-urls.txt')
        self.urls = []
        for line in f.readlines():
            #line_readed = line.partition(':')
            self.urls += [ line ]
            self.list.insert(END, line)
            print line
        f.close()
    
    def getSongsInfo(self):
        #Reader read configuration file
        print "Trying to get the songs info"
        #Check internet connection
        if self.test_connection():
            self.songs = []
            #self.getSpotifyUrl('test') #BORRAME test
            i = 0
            for url in self.urls :
                # getting the urls
                filename = self.getSpotifyUrl(url, i)
                # parsing the html
                songInfo = self.parseHtmlArchive(filename)
                i = i + 1
                #songInfo = #TODO: parse the archive to get the info
                self.songs += [ songInfo ]
                self.list2.insert(END, songInfo)
                #print line
                
    def getSpotifyUrl(self, url, i):
        #webbrowser.open(picture_page)  # test
        # open the web page picture and read it into a variable
        url = url.partition('\n')[0] + '/index.html'
        print "Trying to open : "+ url
        opener1 = urllib2.build_opener()
        page1 = opener1.open(url)
        my_html = page1.read()

        # open file for binary write and save picture
        # picture_page[-4:] extracts extension eg. .gif
        # (most image file extensions have three letters, otherwise modify)
        filename = "eraseme-"+str(i)+".html"
        print filename  # test
        fout = open(filename, "wb")
        fout.write(my_html)
        fout.close()
        
        return filename

        # was it saved correctly?
        # test it out ...
        # webbrowser.open(filename)

    def parseHtmlArchive (self, filename):
        archiveparser = SpiderParser(filename)
        parsedInfo = archiveparser.getParsedInfo()
        print "gettin the info from the parser"+ parsedInfo
        return parsedInfo
    
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



