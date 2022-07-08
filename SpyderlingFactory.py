from selenium import webdriver
import JDSeleniumSpyderling
from selenium.webdriver.chrome.options import Options


def new_spyderling(name, extent, pref):
    """Sets up preferences and returns one of the children class"""
    if name == "JD":
        driver = selenium_launch("https://global.jd.com")
        controller = JDSeleniumSpyderling.JDSpyderlingController()
        controller.set_driver(driver)
        controller.set_extent(extent)
        controller.set_custom(pref)
        return controller
    # elif name == "TMall":
    #     manager = TMallManager.TMallManager()
    #     manager.set_custom(pref)
    #     return manager


def selenium_launch(url):
    """Launches the Selenium tester with initial urls and returns a SeleniumLauncher object"""

    """Sets up the Selenium path"""
    path = "C:/Program Files/chromedriver.exe"
    option = Options()
    option.headless = True
    option.add_argument("window-size=1400,600")
    driver = webdriver.Chrome(path, options=option)
    driver.get(url)
    return driver
