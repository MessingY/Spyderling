from abc import ABC, abstractmethod


class SpyderlingTraverser:
    """Abstract class to manage traversing the websites"""

    @abstractmethod
    def front_page_search(self, driver, keyword):
        pass

    @abstractmethod
    def searched_page_search(self, driver, keyword):
        pass

    @abstractmethod
    def next_page(self, driver, page_num):
        pass

    @abstractmethod
    def next_page_loader(self, driver):
        pass

    @abstractmethod
    def end(self, driver):
        pass


class SpyderlingController(ABC):
    """Abstract class that contains all methods of extracting information using selected Spyderling"""

    def __init__(self):
        self.last_page = None   # Boolean: True if the driver is currently on the last page of a product
        self.extent = None      # Str or int: The extent of the search, either "all" or number of pages

        """Example of custom attribute
            {
                title: True,
                Seller: True,
                comment: [True, 'C:/Program Files/chromedriver.exe']
            }"""
        self.custom = None      # Dict: A dictionary of customization preferences for tailoring the csv files

    @abstractmethod
    def get_curr_page_info(self):
        pass

    @abstractmethod
    def extract_info(self):
        pass

    @abstractmethod
    def get_chosen_info(self):
        pass

    def set_last_page(self, last_page):
        self.last_page = last_page

    def set_extent(self, extent):
        self.extent = extent

    def set_custom(self, custom):
        self.custom = custom

    def is_last_page(self):
        return self.last_page

    def get_extent(self):
        return self.extent

    def get_custom(self):
        return self.custom
