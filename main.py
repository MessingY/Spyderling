from datetime import datetime
import csv
import JDSeleniumSpyderling
import SpyderlingFactory


# Starts run-time calculation
start = datetime.now()

controller = SpyderlingFactory.new_spyderling('JD', "all", {
    "seller": True,
    "curr_price": True,
    'o_price': True,
    'import': True,
    'ad_text': True,
    'comment_num': True,
    'satisfaction': True,
    'url': True,
    'ad': True,
    'title': True
})
controller.front_page_search('壮阳')
controller.searched_page_search('壮阳免疫力')
controller.extract_info()

JDSeleniumSpyderling.end(controller.get_driver())

print('Time: ', datetime.now()-start)




import requests
import csv
import re
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime

"""Basic setup to begin the website testers using Selenium on Chrome"""
path = "C:/Program Files/chromedriver.exe"
option = Options()
# option.headless = True
option.add_argument("window-size=1400,600")
driver = webdriver.Chrome(path, options=option)

location_setting = False    # Sets a one-time-use variable, to set the location for the first time
keyword = '壮阳'      # The keyword that is to be researched
page_num = 0                # The current page number
index = 0                   # The current product number
day, month, year = datetime.now().day, datetime.now().month, datetime.now().year
file_title = keyword + str(month) + '-' + str(day) + '-' + str(year)
fieldnames = [
    'Index', 'ID', 'Title', 'Seller', 'Category 1', 'Category 2', 'URL', 'Price', 'Imports/Exports', 'Origin', 'Weight',
    'Gender', 'Packaging', 'Form'
]

"""Opening and getting ready the csv file"""
f = open("C:/Users/Meison Yuan/Desktop/{title}.csv".format(title=file_title), 'w', encoding='UTF-8', newline='')
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()


"""The Crawling Process"""
while page_num < 51:

    url = 'https://search.jd.com/Search?keyword={key}&page={page_num}&psort=3&enc=utf-8'.format(
        key=keyword,
        page_num=1+page_num*2       # JD formats its page number to be every odd numbers
    )
    page_num = page_num + 1         # Updates the page number
    driver.get(url)
    sleep(3)

    """"Checks whether it has been redirected elsewhere"""
    while 'passport' in driver.current_url or 'keyword' not in driver.current_url:
        sleep(5)
        driver.get(url)

    """Sets up the location to be 天津 by hovering over the location menu and pressing it, done once at the beginning"""
    if location_setting is False:
        hover_element = driver.find_element(By.CSS_SELECTOR, "li[id='ttbar-mycity']")
        hover = ActionChains(driver).move_to_element(hover_element)
        hover.perform()
        TJ = driver.find_element(By.CSS_SELECTOR, "a[data-id='3']")
        TJ.click()
        location_setting = True
    sleep(3)

    """Checks again for misdirection"""
    while 'passport' in driver.current_url or 'keyword' not in driver.current_url:
        sleep(5)
        driver.get(url)
    sleep(3)

    """Gradually scrolls down and loads up the entire page"""
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight*1/4)')
    sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight*2/4)')
    sleep(5)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight*3/4)')
    sleep(5)

    """Data extraction"""
    soup = BeautifulSoup(driver.page_source, 'lxml')
    items = soup.find_all(class_='gl-i-wrap')       # Locates the element containing all the items
    for item in items:
        item = item.parent
        prod_id = item['data-sku']                  # Obtain the product ids of the individual items
        url = 'https://item.jd.com/{id}.html'.format(id=prod_id)    # Construct url of the item page
        print(url)
        areaId = randint(0, 10000)                  # Randomizes an areaId, this prevents the server from tracking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '__jdu = 16576482429101826605902; ip_cityCode = {areaId}'.format(areaId=areaId)
        }                             # Sets up the headers using the random areaId
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'

        """Requesting page info"""
        loop_num = 0
        while 'passport' in res.text:
            sleep(4)
            areaId = randint(0, 10000)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cookie': '__jdu = 16576482429101826605902; ip_cityCode = {areaId}'.format(areaId=areaId)
            }
            res = requests.get(url, headers=headers)
            res.encoding = 'utf-8'
            loop_num = loop_num + 1
            print('inaloop' + str(loop_num))
        sleep(4)
        index = index + 1

        soup = BeautifulSoup(res.text, 'lxml')
        try:
            cat = soup.find("a", {'clstag': 'shangpin|keycount|product|mbNav-3'}).text
        except AttributeError:
            cat = None
        try:
            cat2 = soup.find('a', {'clstag': 'shangpin|keycount|product|mbNav-2'}).text
        except AttributeError:
            cat2 = None
        try:
            seller = soup.find('a', {'clstag': 'shangpin|keycount|product|mbNav-5'}).text
        except AttributeError:
            seller = None
        try:
            impex = soup.find('li', string=re.compile(r'国产/进口.*')).attrs['title']
        except AttributeError:
            impex = None
        try:
            origin = soup.find('li', string=re.compile(r'商品产地.*')).attrs['title']
        except AttributeError:
            origin = None
        try:
            weight = soup.find('li', string=re.compile(r'商品毛重.*')).attrs['title']
        except AttributeError:
            weight = None
        try:
            gender = soup.find('li', string=re.compile(r'适用性别.*')).attrs['title']
        except AttributeError:
            gender = None
        try:
            packaging = soup.find('li', string=re.compile(r'包装形式.*')).attrs['title']
        except AttributeError:
            packaging = None
        try:
            form = soup.find('li', string=re.compile(r'剂型.*')).attrs['title']
        except AttributeError:
            form = None
        title = soup.find('div', {'class': 'sku-name'}).text.replace('\n', '').lstrip(' ').rstrip(' ')
        price = driver.find_element(By.CSS_SELECTOR, "i[data-price='{id}']".format(id=prod_id)).text
        price = soup.find

        row = {
            'Index': index,
            'ID': prod_id,
            'Title': title,
            'Seller': seller,
            'Category 1': cat,
            'Category 2': cat2,
            'Imports/Exports': impex,
            'Origin': origin,
            'URL': res.url,
            'Weight': weight,
            'Gender': gender,
            'Packaging': packaging,
            'Form': form
        }
        writer.writerow(row)

        print(row)
        print('This is the areaId ' + str(areaId))

    print("current page is " + str(page_num))


