
import sys
sys.path.append('/Users/andresbravogorgonio/Documents/Proyectos/Downtify/SRC/downtify/')
from Tkinter import *
import urllib2, urllib
import webbrowser
import os
import time
import string
from HTMLParser import HTMLParser
import gdata.youtube.service
import macOSclipboard



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
                    self.readedInfo = attribute[1]
        if tag == 'a' and attrs:
            for attribute in attrs:
                if (attribute[0] == 'title'): #&& (attribute[0] == 'title')
                    self.readedInfo += " - " + attribute[1]
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
        
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.list.pack(side=LEFT, fill=BOTH, expand=1)
        
        scrollbar2 = Scrollbar(master, orient=VERTICAL)
        self.list2 = Listbox(frame, yscrollcommand=scrollbar.set)
        
        scrollbar2.config(command=self.yview)
        scrollbar2.pack(side=RIGHT, fill=Y)
        self.list2.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.button_get_info = Button(frame, text="GET SONGS", fg="red", command=self.getSongsInfo)
        self.button_get_info.pack(side=RIGHT)
        self.button_get_info = Button(frame, text="ISPECT THE CLIPBOARD", fg="red", command=self.getSpotifyLinks)
        self.button_get_info.pack(side=RIGHT)
        
        #self.configuration()
        
    
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
        
    def getSpotifyLinks(self):
        #Parsing urls from archive
        f = macOSclipboard.paste()
        if f.find('http://open.spotify.com') != -1 :
            self.urls = []
            for line in f.split('\n'):
                if line.find('http://open.spotify.com') == 0 :
                    self.urls += [ line ]
                    self.list.insert(END, line)
                    print line
        else :
            print "No spotify urls in clipboard"
    
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
                # youtube query json
                self.SearchAndPrint(songInfo)
                i = i + 1
                #songInfo = #TODO: parse the archive to get the info
                self.songs += [ songInfo ]
                self.list2.insert(END, songInfo)
                #wait 3 secconds
                print "Wait for 3 secconds..."
                time.sleep(3)
                
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
        
    def getYoutubeResults(self, query , i):
        #webbrowser.open(picture_page)  # test
        # open the web page picture and read it into a variable
        youtubeGdataurl = "http://gdata.youtube.com/feeds/api/videos?max-results=5&alt=json&q="
        youtubeQuery = self.parseYoutubeQuery(query)
        url = youtubeGdataurl + youtubeQuery
        print "Trying to open : "+ url
        opener1 = urllib2.build_opener()
        page1 = opener1.open(url)
        my_html = page1.read()

        # open file for binary write and save picture
        # picture_page[-4:] extracts extension eg. .gif
        # (most image file extensions have three letters, otherwise modify)
        filename = "eraseme-youtube-"+str(i)+".json"
        print filename  # test
        fout = open(filename, "wb")
        fout.write(my_html)
        fout.close()

        return filename

        # was it saved correctly?
        # test it out ...
        # webbrowser.open(filename)
        
    def parseYoutubeQuery(self, query):
        queryPartition = query.split(' ')
        youtubeQuery = ""
        for part in queryPartition :
            youtubeQuery += part
            youtubeQuery += "%20"
        return youtubeQuery
            

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
            
    #YOUTUBE DEFS
    
    def PrintEntryDetails(self, entry):
      #print 'Video title: %s' % entry.media.title.text
      #print 'Video published on: %s ' % entry.published.text
      #print 'Video description: %s' % entry.media.description.text
      #print 'Video category: %s' % entry.media.category[0].text
      #print 'Video tags: %s' % entry.media.keywords.text
      print "Coping to clipboard the video url :"+entry.media.player.url
      macOSclipboard.copy(entry.media.player.url); 
      #print 'Video flash player URL: %s' % entry.GetSwfUrl()
      #print 'Video duration: %s' % entry.media.duration.seconds

      # non entry.media attributes
      #print 'Video geo location: %s' % entry.geo.location()
      #print 'Video view count: %s' % entry.statistics.view_count
      #print 'Video rating: %s' % entry.rating.average

      # show alternate formats
      # for alternate_format in entry.media.content:
      #         if 'isDefault' not in alternate_format.extension_attributes:
      #           print 'Alternate format: %s | url: %s ' % (alternate_format.type,
      #                                                      alternate_format.url)

      # show thumbnails
      # for thumbnail in entry.media.thumbnail:
      #         print 'Thumbnail url: %s' % thumbnail.url
        
    def PrintVideoFeed(self, feed):
      for entry in feed.entry:
        self.PrintEntryDetails(entry)
        return 1
        
    def SearchAndPrint(self, search_terms):
      yt_service = gdata.youtube.service.YouTubeService()
      query = gdata.youtube.service.YouTubeVideoQuery()
      query.vq = search_terms
      query.orderby = 'viewCount'
      query.racy = 'include'
      feed = yt_service.YouTubeQuery(query)
      self.PrintVideoFeed(feed)


root = Tk()

app = App(root)

root.mainloop()


# http://gdata.youtube.com/feeds/api/videos?max-results=5&alt=json&q=search%20query%20here
