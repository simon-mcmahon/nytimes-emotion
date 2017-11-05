import time
import os
from requests import get

from bs4 import BeautifulSoup

from apscheduler.schedulers.background import BackgroundScheduler


sched = BackgroundScheduler()

sched.start()

def scrape():
    url = 'http://www.nytimes.com/most-popular.html'
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
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
                article_links[key] += [(headline,link_txt)]
                #trim the new line and whitespace from link

            print(len(list.find_all('li')))
    print(article_links)

    print(type(list_containers))
    print(len(list_containers))

    print("Every 10 seconds")


sched.add_job(scrape, 'interval', seconds=10, id='ny_popular')
#scheduler.remove_job('my_job_id')
#sched.add_interval_job(some_job, seconds = 900)

time.sleep(30)
sched.shutdown()