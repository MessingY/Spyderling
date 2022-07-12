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
from lxml import etree
import json
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup

path = "C:/Program Files/chromedriver.exe"
option = Options()
# option.headless = True
option.add_argument("window-size=1400,600")
driver = webdriver.Chrome(path, options=option)

keyword = '壮阳'
page_num = 0
while page_num < 101:
    url = 'https://search.jd.com/Search?keyword={key}&page={page_num}&enc=utf-8'.format(
        key=keyword,
        page_num=1+page_num*2
    )
    driver.get(url)
    page_num = page_num
    sleep(3)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight*3/4)')
    sleep(5)

# res = requests.get(url, headers=headers)
# res.encoding = 'utf-8'
# soup = BeautifulSoup(res.text, 'lxml')
# selector = soup.select("[class~=gl-i-wrap]")
# for item in selector:
#     print(item.find("i").text)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    items = soup.find_all(class_='gl-i-wrap')
    ids = []
    for item in items:
        item = item.parent
        ids.append(item['data-sku'])
    for prod_id in ids:
        url = 'https://item.jd.com/{id}.html'.format(id=prod_id)
        print(url)
        areaId = randint(0, 10000)
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        #     'Accept-Encoding': 'gzip, deflate, br',
        #     'Host': "h5speed.m.jd.com",
        #     'Cookie': '__jda=122270672.1657519470004205725549.1657519470.1657604957.1657609987.7; '
        #               '__jdv=122270672|direct|-|none|-|1657519470004; '
        #               '__jdu=1657519470004205725549; '
        #               'areaId={number}; '
        #               'ipLoc-djd={number}-51035-55897-0; '
        #               'shshshfp=99eff37f51cb9af5a9d6753e1d437d26; '
        #               'shshshfpa=bf745fc1-3644-3bd2-e51e-ad13f3c23b29-1657519515; '
        #               'shshshfpb=fZez1FG8sYAmy307en9kKVQ; __jdc=122270672; '
        #               'wlfstk_smdl=34gf0e53wfkcbngep6vqvklavpeysduw; '
        #               'joyya=1657605998.1657606007.16.0cjo965; '
        #               '__jdb=122270672.15.1657519470004205725549|7.1657609987; '
        #               'shshshsID=6a1cb4b576c8aa9a8e1af9575b83c991_3_1657613230201; '
        #               '3AB9D23F7A4B3C9B=NHZFOSOVJICYRYGAHEV2DPWTU4UDVKOJITKPCKK4P4C2NWRHH64QVPGLXUBUZSUHIQYONNV7XDILWJYSDJ3EBRV7CU; '
        #               'token=823eb7297438518d894dfac75e242e72,2,920896; '
        #               '__tk=a2e3752dda414b9b9e12646ec6a9bbf1,2,920896'.format(number=areaId),
        #     'Referer': 'https://item.jd.com/'
        # }
        res = requests.get(url)
        res.encoding = 'utf-8'
        sleep(4)
        print(res.text)

    print("next page")

