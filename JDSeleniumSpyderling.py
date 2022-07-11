import json
import re
import requests
import Spyderling
import csv
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from bs4 import BeautifulSoup
from datetime import datetime


class JDSpyderlingController(Spyderling.SpyderlingController):

    def __init__(self):
        super().__init__()
        self.driver = None

    def get_curr_page_info(self):
        """Obtains the info of all the items on the current page, ordered by current filter"""
        driver = self.driver
        custom = self.custom
        curr_page = []          # One page of info in the form of a dictionary, with index as key and list
        soup = BeautifulSoup(driver.page_source, 'lxml')
        items = soup.select('#J_goodsList ul li')
        titles = soup.select('#J_goodsList ul li div .p-name a em')

        page_count = 0
        for item in items:
            id_ = item.attrs['data-sku']
            ware_url = 'https://item-soa.jd.com/getWareBusiness?callback=jQuery3859988&skuId=100029727640&cat=1316%2C1387%2C1420&area=3_51035_55897_0&shopId=1000398209&venderId=1000398209&paramJson=%7B%22platform2%22%3A%221%22%2C%22specialAttrStr%22%3A%22p0pppp1ppppp2ppppppppppppp%22%2C%22skuMarkStr%22%3A%2200%22%7D&num=1'.format(id_=id_)

            headers = {'authority': 'item-soa.jd.com',
                       'method': 'POST',
                       'path': '/attrlog.php',
                       'scheme': 'https',
                       'accept': '*/*',
                       'accept-encoding': 'gzip, deflate, br',
                       'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                       'content-type': 'application/x-www-form-urlencoded',
                       'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
                       'x-requested-with': 'XMLHttpRequest',
                       }

            new_info = requests.get(ware_url, headers=headers).text
            new_info = new_info[new_info.find('{'):] # .replace("\'", "\"")
            while new_info[-1] != ")":
                new_info = requests.get(ware_url, headers=headers).text
                print("Info Blocked")
            new_info = new_info[new_info.find('{'):]
            new_info = new_info[:-1]
            new_info = json.loads(new_info)

            curr_item = {'title': titles[page_count]}
            page_count = page_count + 1

            service = new_info['stockInfo']['serviceInfo']
            service = service.replace('</a>发货, 并提供售后服务. ', '')
            service = re.sub(r'^.*?>', '', service)
            if custom['seller'] is True:
                curr_item['seller'] = service

            if custom['o_price'] is True:
                o_price = new_info['price']['op']
                curr_item['o_price'] = o_price

            if custom['curr_price'] is True:
                curr_price = new_info['price']['p']
                curr_item['curr_price'] = curr_price

            if custom['import'] is True:
                try:
                    ad = new_info['ad']
                    if '进口' in service or '海外' in service:
                        curr_item['import'] = "Imported"
                    elif '进口' in ad or '海外' in ad:
                        curr_item['import'] = "Imported"
                except KeyError:
                    curr_item['import'] = "Domestic"

            if custom['ad_text'] is True:
                try:
                    curr_item['ad'] = new_info['ad']
                except KeyError:
                    curr_item['ad'] = "None"

            comment_url = None
            comment_stat_url = 'https://club.jd.com/comment/' \
                               'skuProductPageComments.action?' \
                               'callback=fetchJSON_comment98&' \
                               'productId={id}&' \
                               'score=0&' \
                               'sortType=5&' \
                               'page=0&' \
                               'pageSize=10&' \
                               'isShadowSku=0&' \
                               'fold=1'.format(id=id_)
            headers['authority'] = 'club.jd.com'
            new_info = requests.get(comment_stat_url, headers=headers).text
            new_info = new_info.replace('fetchJSON_comment98(', '')
            new_info = new_info.replace(");", '').replace("\'", "\"")
            duder = json.loads(new_info)
            while 'productCommentSummary' not in duder:
                new_info = requests.get(comment_stat_url, headers=headers).text
                new_info = new_info.replace('fetchJSON_comment98(', '')
                new_info = new_info.replace(");", '').replace("\'", "\"")
                duder = json.loads(new_info)

            if custom['comment_num'] is True:
                curr_item['comment_num'] = duder['productCommentSummary']['commentCountStr']

            if custom['satisfaction'] is True:
                curr_item['satisfaction'] = duder['productCommentSummary']['goodRateShow']

            if custom['url'] is True:
                curr_item['url'] = 'https://item.jd.com/{id}.html'.format(id=id_)

            curr_page.append(curr_item)
            print(curr_item)
        return curr_page

    def get_page_titles(self):
        pass    # TODO

    def get_page_ids(self):
        pass    # TODO

    def extract_info(self):
        """Extracts info on every page"""
        fieldnames = list(self.custom.keys())
        f = open("C:/Desktop/star.csv", 'w', encoding='UTF-8', newline='')  # TODO Modify csv
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        pages = self.get_extent()
        page_num = 1
        if pages == "all":
            while not self.is_last_page():
                page_info = self.get_curr_page_info()
                next_page(self, page_num)
                page_num = page_num + 1
                for item in page_info:
                    writer.writerow(item)
        else:
            while page_num != pages+1:
                page_info = self.get_curr_page_info()
                self.get_curr_page_info()
                next_page(self, page_num)
                page_num = page_num + 1
                for item in page_info:
                    writer.writerow(item)
        f.close()

    def get_chosen_info(self):
        pass    # TODO

    def front_page_search(self, keyword):
        """Searches a keyword on the front page of JD Global then checks for last page"""
        driver = self.get_driver()
        search_bar = driver.find_element(By.ID, "key")  # Finds the search bar
        search_bar.send_keys(keyword)
        click = driver.find_element(By.ID, "search-btn")  # Finds the search button
        click.click()
        next_page_loader(driver)
        scroll_down(self)
        check_last_page(self)
        gl_item = driver.find_elements(By.CLASS_NAME, "gl-i-wrap")

        if not self.is_last_page():
            """Checks whether the length of the item list is fully loaded"""
            while len(gl_item) != 60:
                print("..........IN A LOOP, CURRENT gl_item LENGTH = {len}".format(len=len(gl_item)))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/4)")
                sleep(1)
                gl_item = driver.find_elements(By.CLASS_NAME, "gl-item")
        else:
            print("LAST PAGE ALERT")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/4)")
            sleep(1)
            gl_item = driver.find_elements(By.CLASS_NAME, "gl-item")

    def searched_page_search(self, keyword):
        """Searches a keyword on an already searched page then checks for last page"""
        driver = self.get_driver()
        driver.execute_script("window.scrollTo(80,36)")
        driver.find_element(By.ID, "key-re-search").clear()
        search_bar = driver.find_element(By.ID, "key-re-search")
        search_bar.send_keys(keyword)
        click = driver.find_element(By.CSS_SELECTOR, "a[class='btn btn-primary btn-XL']")
        click.click()
        next_page_loader(driver)
        scroll_down(self)
        check_last_page(self)
        gl_item = driver.find_elements(By.CLASS_NAME, "gl-i-wrap")

        if not self.is_last_page():
            """Checks whether the length of the item list is fully loaded"""
            while len(gl_item) != 60:
                print("..........IN A LOOP, CURRENT gl_item LENGTH = {len}".format(len=len(gl_item)))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/4)")
                sleep(1)
                gl_item = driver.find_elements(By.CLASS_NAME, "gl-item")
        else:
            print("LAST PAGE ALERT")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/4)")
            sleep(1)
            gl_item = driver.find_elements(By.CLASS_NAME, "gl-item")

    def set_driver(self, driver):
        self.driver = driver

    def get_driver(self):
        return self.driver


# The helper functions needed to traverse the page
def next_page(controller, page_num):
    """Goes to the next page from said page number"""

    """If last page, then ends"""
    if controller.is_last_page():
        pass
    else:
        driver = controller.get_driver()
        next_btn = driver.find_element(By.CLASS_NAME, 'pn-next')  # locates the next-page button
        now = datetime.now()
        next_btn.click()  # clicks the button
        print("IT TOOK {time} TO CLICK THE NEXT BUTTON".format(time=datetime.now()-now))
        next_page_loader(driver)  # wait for the next page to load
        now = datetime.now()
        scroll_down(controller)  # scroll down to load all items
        print("IT TOOK {time} TO SCROLL DOWN TO THE BOTTOM OF PAGE {page_num}".format(
            time=datetime.now()-now,
            page_num=page_num
        ))


def next_page_loader(driver):
    """ Waits for the next page to finish loading"""
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "J_filter"))
    )


def scroll_down(controller):
    """Begins to scroll to the bottom to load all products on the page"""
    driver = controller.get_driver()
    xp = "//div[@id='J_bottomPage'][@class='p-wrap']"  # Path to the bottom page selector index
    loading = driver.find_element(By.XPATH, xp)  # finds Bottom page element
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", loading)  # Scrolls to the index
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    except StaleElementReferenceException:
        driver.execute_script("arguments[0].scrollIntoView(true);", loading)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    try:
        """Waits until the page has been loaded and the lazyload attribute has been changed to 'done' """
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xp))
        )
    finally:
        sleep(2)  # 2-second delay to allow the page to load up
        check_last_page(controller)  # checks for last page


def check_last_page(controller):
    """Checks if the next page button is disabled, then sets the attribute accordingly"""
    driver = controller.get_driver()
    try:
        driver.find_element(By.XPATH, "//a[@class='pn-next disabled']")
        controller.set_last_page(True)
    except NoSuchElementException:
        controller.set_last_page(False)


def end(driver):
    driver.quit()
