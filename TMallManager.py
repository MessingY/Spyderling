from abc import ABC
from time import sleep
import Spyderling
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from datetime import datetime


class TMallController(Spyderling.SpyderlingController, ABC):

    def __init__(self):
        super().__init__()
