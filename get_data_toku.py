from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import re

url = "https://www3.nhk.or.jp/news/tokushu/?utm_int=all_header_menu_tokushu"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
#get the section with all the links
sec = driver.find_elements_by_class_name("module--content")[1]
#get all article links
links = []
#header articles; avoid double link in the footer
header_articles = sec.find_elements_by_class_name('content--header')
for x in header_articles:
    links.append(x.find_element_by_tag_name('a').get_attribute('href'))
#get rest of articles
content_items = sec.find_element_by_class_name('content--items')
for x in content_items.find_elements_by_tag_name('a'):
    links.append(x.get_attribute('href'))
#get most recent date of articles gathered
with open('nhk_articles_toku.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    recent_date = list(reader)[-1][1]
with open('nhk_articles_toku.csv', 'a', encoding='utf-8') as file:
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
        if date[1].text == '':
            date = date[2].text.split()[0]
        else:
            date = date[1].text.split()[0]
        if date == recent_date:
            break
        info.append(date)
        #get summary
        body_text = []
        summary = re.sub('\n','',driver.find_element_by_class_name('content--summary').text)
        body_text.append(summary)
        #get body paragraphs
        pars = driver.find_elements_by_class_name('body_text')
        for p in pars:
            body_text.append(re.sub('\n', '', p.text))
        info.append(''.join(body_text))
        articles.append(info)
    for article in articles[::-1]:
        writer.writerow(article)

driver.close()
driver.quit()
