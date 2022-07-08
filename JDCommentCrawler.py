# coding:utf-8
import requests
import json


# Obtains the 10 comments information on given page number under the product ID
def jd_comment_crawler(prod_id, pg_num, headers):
    """Configures the url given product ID and the page number"""
    url = 'https://club.jd.com/comment/productPageComments.action?' \
          'callback=fetchJSON_comment98vv12621&' \
          'productId={prod_id}&' \
          'score=0&' \
          'sortType=5&' \
          'page={page}&' \
          'pageSize=10&' \
          'isShadowSku=0&' \
          'fold=1'.format(prod_id=prod_id, page=pg_num)
    result = requests.get(url, headers=headers).text
    """Converts the requested page into into JSON"""
    result = result.replace('fetchJSON_comment98vv12621(', '')
    result = result.replace(');', '')
    """Converts JSON into python dictionary"""
    result = json.loads(result)
    """Using keys in dictionary to find commenter information"""
    for comment in result['comments']:
        print(comment['content'])
        print('---------------------------------------------------------------------')
