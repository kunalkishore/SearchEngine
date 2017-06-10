from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import simplejson as json


def findArticle(url):
    driver = webdriver.Chrome()
    driver.get(url)
    try:
        element=WebDriverWait(driver,300).until(EC.presence_of_element_located((By.ID,"article-text")))
        elem=driver.find_element_by_id('article-text')
        print("collected on article")
        text=elem.text
    except TimeoutException:
        return ''
    driver.close()
    return text

def collectData():
    f=open('data.txt','w')
    driver = webdriver.Chrome()
    driver.get('http://www.reuters.com/resources/archive/us/20170609.html')
    element=WebDriverWait(driver,300).until(EC.presence_of_element_located((By.CLASS_NAME,"module")))
    elem=driver.find_elements_by_class_name('headlineMed')
    for e in elem:
        print("started")
        data={}
        article=e.find_element_by_xpath('a')
        url=article.get_attribute('href')
        title=article.get_attribute('text')
        data["newslink"]=url
        data["title"]=title
        data["date"]="10-07-2017"
        data["newsgenre"]="world news"
        article=findArticle(url)
        if len(article)>0:
            data["article"]=article
        else:
            continue
        json.dump(data,f)
        f.write('\n')
        f.flush()

collectData()
