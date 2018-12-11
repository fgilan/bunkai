from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import re

url = "https://www3.nhk.or.jp/news/catnew.html?utm_int=all_header_menu_news-new#!/12/"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)
#get the section with all the links
sec = driver.find_element_by_class_name("module--content")
#get all article links
links = sec.find_elements_by_tag_name('a')
links = [link.get_attribute('href') for link in links]

#get most recent title
with open('nhk_articles_new.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    recent_title = list(reader)[-1][0]

with open('nhk_articles_new.csv', 'a', encoding='utf-8') as file:
    articles = []
    writer = csv.writer(file, delimiter=',', lineterminator='\n')
    for link in links:
        info = []
        driver.get(link)
        time.sleep(2)
        #check if it is a News Up
        genre = driver.find_elements_by_class_name('i-genre')
        if genre:
            continue
        #get title
        title = driver.find_element_by_class_name('content--title').text
        #check if already in database
        if title == recent_title:
            break
        info.append(title)
        #get date
        date = driver.find_elements_by_tag_name('time')
        if date[1].text == '':
            date = date[2].text.split()[0]
        else:
            date = date[1].text.split()[0]
        info.append(date)
        #get summary
        body_text = []
        summary = re.sub('\n','',driver.find_element_by_class_name('content--summary').text)
        body_text.append(summary)
        #get summary more, if it exists
        if driver.find_elements_by_class_name('content--summary-more'):
            body_text.append(re.sub('\n','',driver.find_element_by_class_name('content--summary-more').text))
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
