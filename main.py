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
