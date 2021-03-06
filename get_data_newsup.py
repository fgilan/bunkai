from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import re

url = "https://www3.nhk.or.jp/news/netnewsup/?utm_int=all_header_menu_netnewsup"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
#get the section with all the links
sec = driver.find_elements_by_class_name("module--content")
#get all article links
links = []
#header articles; avoid double link in the footer
header_articles = sec[0].find_elements_by_class_name('content--header')
for x in header_articles:
    links.append(x.find_element_by_tag_name('a').get_attribute('href'))
#get first half of articles
content_items_1 = sec[0].find_elements_by_class_name('content--items')
#get second half of articles
content_items_2 = sec[1].find_elements_by_class_name('content--items')
content_items = content_items_1 + content_items_2
for content_item in content_items:
    for item in content_item.find_elements_by_tag_name('a'):
        links.append(item.get_attribute('href'))
#get the most recent date already in the database
with open('nhk_articles_newsup.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    recent_date = list(reader)[-1][1]

#retrive info and write to file
with open('nhk_articles_newsup.csv', 'a', encoding='UTF-8') as file:
    #list of info to add
    articles = []
    writer = csv.writer(file, delimiter=',', lineterminator='\n')
    for link in links:
        info = []
        driver.get(link)
        time.sleep(2)
        #get title
        title = driver.find_element_by_class_name('content--title')
        title = title.find_elements_by_tag_name('span')[1].text
        info.append(title)
        #get date
        date = driver.find_elements_by_tag_name('time')
        date = date[2].text.split()[0]
        #if we have already gathered data for this date, end collection
        if date == recent_date:
            break
        info.append(date)
        #get summary
        body_text = []
        summary = driver.find_element_by_class_name('content--summary').text
        body_text.append(re.sub('\n','', summary))
        #get body paragraphs
        pars = driver.find_elements_by_class_name('body-text')
        for p in pars:
            body_text.append(re.sub('\n', '', p.text))
        info.append(''.join(body_text))
        articles.append(info)
    for article in articles[::-1]:
        writer.writerow(article)

driver.close()
driver.quit()
