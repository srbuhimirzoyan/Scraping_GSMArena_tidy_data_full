import requests
from lxml import html
from lxml.etree import tostring
import pandas as pd
from bs4 import BeautifulSoup
import time

def phones_url_list(url):
    '''function scraping phone urls from a given sitemap.xml url'''
  response=requests.get(url, headers={"user-agent":"edu_research_bot"}) 
  #making HTML a bytes object
  page=response.content  
  #getting string of source code from response
  tree=html.document_fromstring(page)
  phonelist=[i.text_content() for i in tree.xpath("//url/loc")]
  stop_words=['related','pictures']
  phonelist=[url for url in phonelist if not any(stop_word in url for stop_word in stop_words)]
  return phonelist

  #defining a function getting all the necessary data 
def phone_info_scraper(url):
    '''function getting all the features of the phone with respective titles'''
    request= requests.get(url)
    time.sleep(2)
    page = BeautifulSoup(request.content,"html.parser")
    model_name=page.find('h1', attrs={"data-spec":"modelname"}).get_text()
    table=page.find_all("table")
    ttl=[i.find_all("td", class_="ttl") for i in table]
    nfo=[i.find_all("td", class_="nfo") for i in table]
    titles=[]
    for rowlist in ttl:
        for row in rowlist:
            titles.append(row.get_text())
        rowinfo=[]
    for rowlist in nfo:
        for row in rowlist:
            rowinfo.append(row.get_text())
    all_info_dict=dict(zip(titles,rowinfo))
    all_info_dict["model_name"]=model_name
    all_info_dict["url"]=url
    return all_info_dict