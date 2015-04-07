import sys
from collections import deque
import Queue
import httplib2
import urllib2 as urllib
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup, SoupStrainer
from database import Database
from threading import Thread
from threading import Lock as ThreadLock, Event
import time
from models import Page


http = httplib2.Http()





class Crawler(Thread):
    """docstring for Crawler"""

    urlDb = Database('url')
    crawledUrls = {'size': 0, 'error': 0}
    queue = Queue.Queue()
    database = Database()
    database.openDb()
    database.clearDb()
    urlDb.openDb()
    urlDb.clearDb()
    threads = []
    lock = ThreadLock()
    def __init__(self):
        super(Crawler, self).__init__()
        self.stopSignal = False
        self._stop = Event()

    def stop(self):
        self.stopSignal = True
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    # function to fetch a web page
    def fetch_page(self, url):
        conn = urllib.urlopen(url)
        time.sleep(0.010)
        return conn.read()
        
    # function to get the date of a web page of the given URL
    # function returns href links and information in the page
    def get_data(self, url):
        links = []
        page = self.fetch_page(url)
        soup = BeautifulSoup(page)
        try:
            title = soup.find('title').get_text().lower()
        except AttributeError, e:
            title = ""
        
        meta = []
        for line in soup.find_all('a'):
            links.append(line.get('href'))
        for line in soup.find_all('meta'):
            meta.append(str(line.attrs).lower())
        return {'links': links, 'info': {'title': title, 'meta': meta}}
        
    # function to get the base address of a web page
    def get_base(self, url):
        if url[7:].find('/') == -1:
            url = url + '/'
        return url[0:url.rfind('/')+1]
        
    # function to get the base domain of a web page
    def get_base_domain(self, url):
        last = url[7:].find('/') + 7;
        if last == -1:
            return url
        else:
            return url[0:last]
        
    
    # function to store data in a database
    def store_data(self, url):
        Crawler.lock.acquire()
        Crawler.queue.put(url)
        Crawler.lock.release()

        while Crawler.queue.empty() == False:
            if self.stopSignal:
                break

            Crawler.lock.acquire()
            url = Crawler.queue.get()
            Crawler.lock.release()

            print url + '\n'
            # a = {}
            try:
                a = self.get_data(url)
            except urllib.HTTPError, e:
                print "Error at url: '" + url + "'"
                Crawler.lock.acquire()
                Crawler.crawledUrls['error'] += 1
                Crawler.lock.release()
                continue
            except urllib.URLError, e:
                print 'URL error for link "' + url + '"'
                Crawler.lock.acquire()
                Crawler.crawledUrls['error'] += 1
                Crawler.lock.release()
                continue
            
            base = self.get_base(url)
            base_domain = self.get_base_domain(url)
            
            for link in a['links']:
                # we continue for the next link if type of link is not string
                                             # if the link starts with #
                                             # if the link is https
                                             # if the link is already visited
                                             # if the link is having javascript:void(0)
                if type(link)!=str or link[0:1] == '#' or link[0:8] == 'https://' or Crawler.crawledUrls.has_key(url.lower()) or link.rfind('javascript:void(0)')!=-1:
                    continue
                link = link.strip()
                
                if len(link)!=0:
                    if(link[0]=='/'):
                        link = base_domain + link
                    elif (link[0:7] != 'http://'):
                        link = base + link
                Crawler.lock.acquire()
                Crawler.queue.put(link)
                Crawler.lock.release()
            try:
                Page(url=url, title=a['info']['title'], content=str(a['info']['meta']), name=a['info']['title']).save()
                
                # Crawler.database.store({'url': url, 'data': a['info']})
            except urllib.HTTPError, e:
                    print 'HTTP Error at link: ' + link
                    # continue
            except urllib.URLError, e:
                    print 'URL error for link "' + link + '"'
                    # continue

            Crawler.lock.acquire()
            Crawler.crawledUrls[url.lower()] = True
            Crawler.crawledUrls['size'] += 1
            Crawler.urlDb.store(url.lower() + "\n")
            Crawler.lock.release()
    
            
    # function to show data of the database
    def show_data(self):
        Crawler.lock.acquire()
        Crawler.database.openDb()
        data = Crawler.database.show()
        Crawler.database.closeDb()
        Crawler.lock.acquire()
        print data
        
    # function to make search in a database
    def search_data(self, url):
        Crawler.lock.acquire()
        Crawler.database.openDb()
        data = Crawler.database.find('url',url)
        Crawler.database.closeDb()
        Crawler.lock.release()

        print data
    
    def clear(self):
        Crawler.lock.acquire()
        Crawler.database.clearDb()
        Crawler.urlDb.clearDb()
        Crawler.lock.release()
        
    def openDatabase(self):
        Crawler.lock.acquire()
        Crawler.database.openDb()
        Crawler.urlDb.openDb()
        Crawler.lock.release()
    
    def closeDatabase(self):
        Crawler.lock.acquire()
        Crawler.database.closeDb()
        Crawler.urlDb.closeDb()
        Crawler.lock.release()
    
    def setUrl(self, url):
        self.url = url
    
    def run(self):
        
        self.store_data(self.url)
        
        # self.show_data()
        #print links
    
    
    def status(self):
        return {'num_links': Crawler.crawledUrls['size']}
    

    # def temp(self):
    #     data = Page("http://google.com","Google","this is a google website home page0","Description");
    #     data.save()
        
       
# links = ['http://google.com', 'http://wikipedia.org', 'http://facebook.com', 'http://python.org', 'http://tutorialspoint.com']

# crawlers = {}
# for link in links:
#     crawlers[link] = Crawler()
    
#     crawlers[link].setUrl(link)
#     crawlers[link].start()
