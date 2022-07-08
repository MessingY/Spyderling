from datetime import datetime
import Spyderling
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import JDSeleniumSpyderling


def get_page_ids(self):
    pass  # TODO


def get_page_titles(self):
    pass  # TODO


def get_page_prices(self):
    """Obtains the prices of all the items on the current page, ordered by current filter"""
    driver = self.driver
    prices = []
    gl_item = driver.find_elements(By.CLASS_NAME, "gl-item")

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

    """returns the prices"""
    for item in gl_item:
        price = item.find_element(by=By.TAG_NAME, value='i')
        prices.append(price.text)
    return prices


def get_all_pages_info(self):
    """"Starting from the current page, obtain all the information as preferred"""
    while not self.is_last_page():
        pass