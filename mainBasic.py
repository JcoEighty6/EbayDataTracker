import requests
import sqlite3
from bs4 import BeautifulSoup #this one is for webcrawling

#Variables
maxPages = 5                  #This determines how many pages per letter.

#SQLite Variables
ebay_data = '/Users/J/Desktop/my_db.sqlite' #database location

#Connect to DB
conn = sqlite3.connect(ebay_data)
c = conn.cursor() #the DB cursor.

#Create table
c.execute("CREATE TABLE if not exists ebay (id INT PRIMARY KEY NOT NULL)") #create a table with a single column called id which is an int and the primary key

#fw = open('info.txt','w')
def Ebay_Analyzer(maxPages):

    pageNumber = 1 #The current page to crawl

    while (pageNumber <= maxPages):

        url = 'http://www.ebay.com/sch/i.html?_from=R40|R40&_sacat=0&LH_Complete=1&_udlo=&_udhi=&_ftrt=901&_ftrv=1&_sabdlo=&_sabdhi=&_samilow=&_samihi=&_sadis=15&_stpos=&_sop=13&_dmd=1&_nkw=a&_pgn=' + str(pageNumber) + '&_skc='+ str(((pageNumber-1)*50)) +'&rt=nc'

        sourceCode = requests.get(url)
        plainText = sourceCode.text
        soup = BeautifulSoup(plainText)

        for link in soup.findAll('a', {'class': 'vip'}):
            href = link.get('href')
            newSource = requests.get(href)
            newPlainText = newSource.text
            newSoup = BeautifulSoup(newPlainText)

            for title in newSoup.findAll('h1', {'class': 'it-ttl'}):
                itemTitle = title.get_text()
                #print(itemTitle[16:])
                #insertTitle = itemTitle[16:]



            for itemID in newSoup.findAll('div', {'class': 'u-flL iti-act-num'}):
                itemNumber = itemID.string
                print(itemNumber)
                ID = (itemNumber)
                #fill a row with data
                c.execute("INSERT INTO ebay (id) VALUES (?)", (itemNumber,))

            for category in newSoup.findAll('li', {'class': 'bc-w'}):
                for info in category.findAll('a', {'class': 'thrd'}):
                    text = info.string
                    #print(text)
        print(pageNumber)
        pageNumber += 1
        print(pageNumber)
Ebay_Analyzer(1)

conn.commit()
conn.close()