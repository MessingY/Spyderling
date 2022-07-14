import requests
import csv
import re
import json
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
page_setting = False        # Sets a one-time-use variable, to set the total page number
keyword = '注意力保健品'            # The keyword that is to be researched
page_num = 0                # The current page number
total_page = 100            # Place-holder for the total number of pages
index = 0                   # The current product number
day, month, year = datetime.now().day, datetime.now().month, datetime.now().year
file_title = keyword + str(month) + '-' + str(day) + '-' + str(year)
fieldnames = [
    'Index', 'ID', 'Title', 'Seller', 'Category 1', 'Category 2', 'URL', 'Original Price', 'Current Price',
    'Imports/Exports', 'Origin', 'Weight', 'Gender', 'Packaging', 'Form'
]

"""Opening and getting ready the csv file"""
f = open("C:/Users/Meison Yuan/Desktop/{title}.csv".format(title=file_title), 'w', encoding='UTF-8', newline='')
writer = csv.DictWriter(f, fieldnames=fieldnames)
writer.writeheader()


"""The Crawling Process"""
while page_num < total_page:

    url = 'https://search.jd.com/Search?keyword={key}&page={page_num}&psort=3&enc=utf-8'.format(
        key=keyword,
        page_num=1+page_num*2       # JD formats its page number to be every odd numbers
    )
    page_num = page_num + 1         # Updates the page number
    driver.get(url)
    sleep(3)

    """"Checks whether it has been redirected elsewhere, and if too many times, restart"""
    loop_ceiling = 10
    looper = 0
    while 'passport' in driver.current_url or 'keyword' not in driver.current_url:
        sleep(5)
        if looper < loop_ceiling:
            driver.get(url)
            looper = looper + 1
        else:
            driver.quit()
            sleep(5)
            driver = webdriver.Chrome(path, options=option)
            driver.get(url)
            looper = 0

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

    """Finds the total number of pages, then set it for the rest of the duration of the crawling"""
    if page_setting is False:
        skip = driver.find_element(By.CLASS_NAME, 'p-skip')
        total_page = int(skip.find_element(By.TAG_NAME, 'b').text)
        print(total_page)
        page_setting = True

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
            'Authority': 'item.jd.com',
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
            jdu = randint(0, 999999999)
            headers = {
                'Authority': 'item.jd.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cookie': '__jdu = 16576482429101{jdu}; ip_cityCode = {areaId}'.format(areaId=areaId, jdu=jdu)
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

        """Requesting webpage loading info --- getWareBusiness"""
        areaId = randint(0, 10000)
        headers = {
            'Authority': 'item.soa.jd.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '__jdu = 16576482429101826605902; areaId={areaId}; ip_cityCode = {areaId}'.format(areaId=areaId)
        }
        res = requests.get('https://item-soa.jd.com/getWareBusiness?callback=jQuery8400498&'
                           'skuId={prod_id}&area={areaId}_51035_55897_0&'
                           'paramJson=%7B%22platform2%22%3A%221%22%2C%22colType'
                           '%22%3A0%2C%22specialAttrStr%22%3A%22p0ppppppppp3ppppppppppppp%22%2C%22skuMarkStr%22%3A%2200'
                           '%22%7D&num=1'.format(prod_id=prod_id, areaId=areaId), headers=headers)
        res.encoding = 'utf-8'
        while res.text == "{'code':200,'limit:1}":
            areaId = randint(0, 10000)
            jdu = randint(0, 999999999)
            headers = {
                'Authority': 'item.soa.jd.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                'Accept-Encoding': 'gzip, deflate, br',
                'Cookie': '__jdu = 16576482429101{jdu}; areaId={areaId}; ip_cityCode = {areaId}'.format(
                    areaId=areaId,
                    jdu=jdu
                    )
            }
            res = requests.get('https://item-soa.jd.com/getWareBusiness?callback=jQuery8400498&'
                               'skuId={prod_id}&area={areaId}_51035_55897_0&'
                               'paramJson=%7B%22platform2%22%3A%221%22%2C%22colType'
                               '%22%3A0%2C%22specialAttrStr%22%3A%22p0ppppppppp3ppppppppppppp%22%2C%22skuMarkStr%22%3A%2200'
                               '%22%7D&num=1'.format(prod_id=prod_id, areaId=areaId), headers=headers)
            res.encoding = 'utf-8'
        ware_dic = json.loads('{' + res.text.partition('{')[2].strip(')'))
        op = ware_dic['price']['op']
        curr_price = ware_dic['price']['p']

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
            'Form': form,
            'Original Price': op,
            'Current Price': curr_price
        }
        writer.writerow(row)

        print(row)
        print('This is the areaId ' + str(areaId))

    print("current page is " + str(page_num))
