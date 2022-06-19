'''
Webscraper Application (currently limited to target search engine),
queries for products based on a search key, adds the most relevant results to
a returned database containing name, price, and nutrition (to be plugged into underlying math model)

Author: Zayn Khan
Email: zaynalikhan@gmail.com
Version Date: 6.18.2022

'''
import time
import requests
from bs4 import BeautifulSoup
import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager



set_urls=set()
def generate_search(query):
    search_engine="https://www.target.com/s?searchTerm=" + query
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(search_engine)
    time.sleep(10)
    elements = driver.find_elements(By.TAG_NAME, 'a')

    list_links=[]
    for e in elements:
        link=e.get_attribute(name='href')
        exp=re.search("/p/.*/", link)
        regex=exp.group() if exp is not None else None
        if (link.startswith("https://www.target.com/p/") and regex is not None and regex not in set_urls):
           list_links.append(link)
           set_urls.add(regex)
    driver.close()
    return(list_links)





def generate_item(url):
    request= requests.get(url)
    print(url)
    parsed=BeautifulSoup(request.text,"html.parser")
    content=re.findall("JSON.parse\(.*\);",parsed.prettify())[2]
    item_info=str()
    to_parse=re.sub("\\\\", "",content[12:-3])

    file=json.loads(to_parse)
    nutrients=dict()

    find_name=file['__PRELOADED_QUERIES__']['queries'][1][1]['product']['item']['product_description']['title']
    find_price = file['__PRELOADED_QUERIES__']['queries'][1][1]['product']['price']['current_retail']
    nutrition_label = file['__PRELOADED_QUERIES__']['queries'][1][1]['product']['item']['enrichment']['nutrition_facts']['value_prepared_list'][0]['nutrients']
    serving_size=file['__PRELOADED_QUERIES__']['queries'][1][1]['product']['item']['enrichment']['nutrition_facts']['value_prepared_list'][0]['servings_per_container']


    nutrients['name']=find_name
    nutrients['price']=find_price
    nutrients['link']=url
    nutrients['Servings Per Container']=serving_size #rename later

    for item in nutrition_label:
        try:
            nutrients[item['name']]=item['quantity']
        except KeyError:
            pass

    return nutrients

def generate_products(list_urls):
    products=[]
    for link in list_urls:
        try:
            products.append(generate_item(link))
        except Exception:
            pass
    return products


#fed to backend algorithm and supplies background information to the frontend
def create_model(query, price=20.0):
    contents=generate_search(query)
    output=generate_products(contents)

    for filtered in output:
        if float(filtered['price'])>float(price):
            output.remove(filtered)

    return output

print(create_model("egg",10.0))






