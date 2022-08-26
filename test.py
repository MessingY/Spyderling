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

f = open("C:/Users/Innov/OneDrive/Desktop/NMN_ID.txt", 'r', encoding='UTF-8', newline='')

g = open('C:/Users/Innov/OneDrive/Desktop/NMN_ID.csv', 'w', encoding='UTF-8', newline='')
writer = csv.DictWriter(g, fieldnames=['ID', 'Comment Count', 'True Comment Count', 'Keywords'])
writer.writeheader()

for line in f:

    row = {}

    comment = 0
    randomizer = randint(0, 9999)
    rand2 = randint(0, 9999)
    header = {
        'Host': 'club.jd.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'ip_cityCode={rand}'.format(rand=str(randomizer)),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    res = requests.get(
        'https://club.jd.com/comment/skuProductPageComments.action?callback=fetchJSON_comment{rand2}&productId={id}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(
            id=line.strip('\r\n'), rand2=rand2), headers=header)
    print(res.text)
    res_dic = json.loads('{' + res.text.partition('{')[2].strip(');'))

    for i in range(1, 6):
        comment += res_dic['productCommentSummary']['score{i}Count'.format(i=i)]

    row['ID'] = line.strip('\r\n')
    row['Comment Count'] = res_dic['productCommentSummary']['commentCountStr']
    row['True Comment Count'] = comment

    dex = 0
    hot_stat = {}
    for hot in res_dic['hotCommentTagStatistics']:
        hot_stat[res_dic['hotCommentTagStatistics'][dex]['name']] = res_dic['hotCommentTagStatistics'][dex]['count']
        dex += 1
    print(comment)

    row['Keywords'] = hot_stat
    writer.writerow(row)

    sleep(3)

f.close()
