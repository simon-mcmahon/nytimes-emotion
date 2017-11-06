import time
import datetime
from requests import get
import sqlite3

import logging
logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('Record of success or failure of calls')

from bs4 import BeautifulSoup

from apscheduler.schedulers.background import BackgroundScheduler


sched = BackgroundScheduler()

sched.start()

def scrape():
    query_time = round(time.time())
    url = 'http://www.nytimes.com/most-popular.html'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    #Find the div tag which contains the lists
    list_containers = html_soup.find_all('div', class_='mostPopularModule')

    count = 0
    article_key = ['email','viewed','fb','twitter']
    article_links = {'fb': [], 'twitter': [], 'email': [], 'viewed': []}
    for list in list_containers:
        count = count + 1

        #only choose most emailed, viewed, FB and twitter
        if count in [1,2,3,6]:
            #get the dictionary key for the current count
            key = article_key[[1,2,3,6].index(count)]
            link_list = list.find_all('li')
            for link in link_list:
                headline = link.text.strip()
                link_txt = link.a['href']
                article_links[key] += [(link_txt,headline)]
                #trim the new line and whitespace from link

    # print(article_links)

    print('---------Scraping most popular finished-----------')

    # Creates or opens a file called mydb with a SQLite3 DB
    db = sqlite3.connect('data/nytimes.sqlite')

    # Get a cursor object and make the tables if they do not already exist
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS link(link_id INTEGER PRIMARY KEY, url TEXT, headline TEXT, article TEXT) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS query(query_id INTEGER PRIMARY KEY, unixtime DATETIME) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fb(query_id INTEGER NOT NULL, link1 TEXT, link2 TEXT, link3 TEXT, link4 TEXT, 
        link5 TEXT, link6 TEXT, link7 TEXT, link8 TEXT, link9 TEXT, link10 TEXT, 
        FOREIGN KEY (query_id) REFERENCES query(query_id)) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS twitter(query_id INTEGER NOT NULL, link1 TEXT, link2 TEXT, link3 TEXT, link4 TEXT, 
        link5 TEXT, link6 TEXT, link7 TEXT, link8 TEXT, link9 TEXT, link10 TEXT, 
        FOREIGN KEY (query_id) REFERENCES query(query_id)) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email(query_id INTEGER NOT NULL, link1 TEXT, link2 TEXT, link3 TEXT, link4 TEXT, 
        link5 TEXT, link6 TEXT, link7 TEXT, link8 TEXT, link9 TEXT, link10 TEXT, 
        FOREIGN KEY (query_id) REFERENCES query(query_id)) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS viewed(query_id INTEGER NOT NULL, link1 TEXT, link2 TEXT, link3 TEXT, link4 TEXT, 
        link5 TEXT, link6 TEXT, link7 TEXT, link8 TEXT, link9 TEXT, link10 TEXT, 
        FOREIGN KEY (query_id) REFERENCES query(query_id)) ''')
    db.commit()

    #Begin adding the collected links into the database

    #Get the last row id numbers for link_id and query_id

    max_link_id = db.execute('SELECT max(link_id) FROM link;').fetchall()[0][0]
    if max_link_id==None:
        max_link_id = 0
    else:
        max_link_id = int(max_link_id)

    max_query_id = db.execute('SELECT max(query_id) FROM query;').fetchall()[0][0]
    if max_query_id==None:
        max_query_id = 0
    else:
        max_query_id = int(max_query_id)

    try:
        with db:
            db.execute('''INSERT INTO query(query_id, unixtime)
                      VALUES(?,?)''', (max_query_id+1, query_time))
            #assemlbe the links for each social media
            link_count = 0
            for social_media in article_key:
                num_links = len(article_links[social_media])
                link_tuple = tuple([max_query_id+1] + [article_links[social_media][x][0] for x in range(0,num_links)] )
                headline_tuple = tuple([max_query_id+1] + [article_links[social_media][x][1] for x in range(0,num_links)] )

                db.execute('''INSERT INTO {0}(query_id, link1,link2,link3,link4,link5,link6,link7,link8,link9,link10)
                          VALUES(?,?,?,?,?,?,?,?,?,?,?)'''.format(social_media), link_tuple)
                #Get the article text and insert into DB

                # TODO: Check if the article exists and do not add if so

                for article_url in link_tuple[1:]:
                    link_count = link_count + 1
                    headline_add = headline_tuple[link_tuple.index(article_url)]
                    # print(article_url)
                    # print(str(link_count + max_link_id))
                    # #Get the article text for each article
                    article = article_text(article_url)
                    # print(article)
                    db.execute('''INSERT INTO link(link_id,url,headline,article)
                              VALUES(?,?,?,?)''', (max_link_id + link_count, article_url, headline_add,article))

    except sqlite3.IntegrityError:
        logging.warning('Record already exists - Integrity error sqlite3')
    finally:
        print('Completed grab at '+str(query_time))
        logging.warning('Completed grab at '+str(query_time))
        db.commit()
        db.close()

def article_text(article_url):
    response = get(article_url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    #Find the div tag which contains the lists
    article_response = html_soup.find_all('p', class_='story-body-text story-content')
    text = ''
    for story_section in article_response:
        text += story_section.text.strip() + '\n'

    return text


sched.add_job(scrape, 'interval', minutes=15, id='ny_popular')
#scheduler.remove_job('my_job_id')
#sched.add_interval_job(some_job, seconds = 900)
while True:
    time.sleep(120)
    print('----------Still alive-----')
#sched.shutdown()