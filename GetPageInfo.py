
# Using url, writes down the product information onto an appropriately named .csv file on the desktop
import csv
import re

import requests
from bs4 import BeautifulSoup

from JDCommentCrawler import jd_comment_crawler


def get_page_info(html):

    # Creates the cookies and header for the request
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Host': 'club.jd.com',
        'Referer': 'https://item.jd.com/3867555.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/58.0.3029.110 Safari/537.36',
        'Cookie': '',
    }

    """Takes str argument to opening the html file"""
    # opened_html = open(html, "r", encoding='utf-8')
    contents = requests.get(html, headers=headers).text

    """Reading the file and storing in a variable"""
    # contents = opened_html.read()

    """Creating a BeautifulSoup object and specifies the parser"""
    bs_text = BeautifulSoup(contents, 'lxml')
    jd_titles = bs_text.select('#J_goodsList ul li div .p-name a em')  # Obtains product names
    jd_prices = bs_text.select('#J_goodsList ul li div .p-price strong i')  # Obtains product prices
    jd_hrefs = bs_text.select('#J_goodsList ul li div .p-name a')  # Obtains product urls

    fieldnames = ['placement', 'jdtitles', 'jdprices', 'jdhrefs']
    # f = open("C:/Users/Innov/OneDrive/Desktop/" + html[:-5] + '.csv', 'w',
    #          encoding='UTF-8',
    #          newline='')
    f = open("C:/Users/Innov/OneDrive/Desktop/star.csv", 'w', encoding='UTF-8', newline='')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    """Obtains product"""
    count = 0
    info = []
    for jd_title, jd_price, jd_href in zip(jd_titles, jd_prices, jd_hrefs):
        count = count + 1
        res = re.match("(http|https|ftp)://[^\s]+", jd_href["href"])
        if res is None:  # If it does not begin with http, then create hyperlink
            jd_href["href"] = ('https:' + jd_href["href"])
        writer.writerow(
            {
                'placement': format(count),
                'jdtitles': format(jd_title.get_text().replace('\n', '')),
                'jdprices': format(jd_price.get_text()),
                'jdhrefs': format(jd_href['href'])
            }
        )
        prod_id = format(jd_href['href']).replace('https://item.jd.com/', '').replace('.html', '')
        jd_comment_crawler(prod_id, 0, headers)
    f.close()
