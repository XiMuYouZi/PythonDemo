import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from JDSpider.Config import *
import pymongo


class JDSpider:

        def __init__(self):
            client = pymongo.MongoClient(MONGO_URL)
            self.db = client[MONGO_DB]
            self.browser = webdriver.PhantomJS(service_args=SERVICE_ARGS,
                                          executable_path='/Users/Chan/phantomjs-2.1.1-macosx/bin/phantomjs')
            # self.browser = webdriver.Chrome()
            self.wait = WebDriverWait(self.browser, 10)
            self.browser.set_window_size(1400, 900)

        def search(self):
            print('正在搜索')
            try:
                self.browser.get('https://www.taobao.com')
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
                )
                submit = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
                input.send_keys(KEYWORD)
                submit.click()
                total = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
                self.get_products()
                print(type(total),total.text)
                return total.text
            except TimeoutException:
                print('serch出错啦')
                return self.search()


        def next_page(self,page_number):
            print('正在翻页', page_number)
            try:
                input = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
                )
                submit = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
                input.clear()
                input.send_keys(page_number)
                submit.click()
                self.wait.until(EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
                self.get_products()
            except TimeoutException:
                self.next_page(page_number)


        def get_products(self):
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
            html = self.browser.page_source
            doc = pq(html)
            items = doc('#mainsrp-itemlist .items .item').items()
            for item in items:
                product = {
                    'image': item.find('.pic .img').attr('src'),
                    'price': item.find('.price').text(),
                    'deal': item.find('.deal-cnt').text()[:-3],
                    'title': item.find('.title').text(),
                    'shop': item.find('.shop').text(),
                    'location': item.find('.location').text()
                }
                print(product)
                self.save_to_mongo(product)


        def save_to_mongo(self,result):
            try:
                if self.db[MONGO_TABLE].insert(result):
                    print('存储到MONGODB成功', result)
            except Exception:
                print('存储到MONGODB失败', result)


        def getComputerInfo(self):
            try:
                total = self.search()
                total = int(re.compile('(\d+)').search(total).group(1))
                for i in range(2, total + 1):
                    self.next_page(i)
            except Exception:
                print('出错啦')
            finally:
                self.browser.close()





