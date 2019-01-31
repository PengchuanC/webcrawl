import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd

from scrapy.config import CHROME_DRIVER, FILES

name_ex = ''
default_dir = ''


class Chrome(object):
    def __init__(self):
        self.driver = Chrome.create()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def create():
        chrome_options = Options()
        chrome_options.add_argument('log-level=4')
        chrome_options.add_argument('--disable-gpu')
        option = chrome_options
        driver = webdriver.Chrome(executable_path=CHROME_DRIVER, chrome_options=option)
        driver.get('http://data.stats.gov.cn/easyquery.htm?cn=C01')
        driver.find_element_by_xpath('//*[@id="mySelect_sj"]/div[2]/div[1]').click()
        driver.find_element_by_xpath('//*[@id="mySelect_sj"]/div[2]/div[2]/div[2]/ul/li[3]').click()
        return driver


def make_dir(dir):
    dir_path = os.path.join(FILES, dir)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    global default_dir
    default_dir = dir_path


def save_to_excel(html, name):
    excel = pd.read_html(html)[0]
    path = os.path.join(default_dir, name)
    excel.to_excel(f'{path}.xlsx', index=False)


def digui(driver, id):
    start = 1
    while True:
        try:
            tag_id = driver.find_element_by_xpath(f'//*[@id="{id}"]/*[{start}]').get_attribute('id')
            name = driver.find_element_by_xpath(f'//*[@id="{id}"]/*[{start}]').tag_name
            start += 1
            if name == 'a':
                global name_ex
                driver.find_element_by_xpath(f'//*[@id="{tag_id}"]').click()
                try:
                    tag_class = driver.find_element_by_xpath(f'//*[@id="{tag_id}"]/*').get_attribute('class')
                    if 'docu' in tag_class:
                        _tag_id = driver.find_element_by_xpath(f'//*[@id="{tag_id}"]/*[2]').get_attribute('id')
                        tag_name = driver.find_element_by_xpath(f'//*[@id="{tag_id}"]/*[2]').tag_name
                        tag_text = driver.find_element_by_xpath(f'//*[@id="{tag_id}"]/*[2]').text
                        print(_tag_id, tag_name, tag_class, name_ex + '_' + tag_text)
                        html = driver.page_source
                        save_to_excel(html, name_ex + '_' + tag_text)
                        driver.execute_script("window.scrollTo(0, 1600)")
                    elif 'ico_open' in tag_class:
                        name_ex = driver.find_element_by_xpath(f'//*[@id="{tag_id}"]/*[2]').text
                except NoSuchElementException:
                    pass
            digui(driver, tag_id)
        except NoSuchElementException:
            break


def get_main_class(id):
    with Chrome() as c:
        driver = c.driver
        start = 1
        while True:
            try:
                tag_id = driver.find_element_by_xpath(f'//*[@id="{id}"]/*[{start}]').get_attribute('id')
                text = driver.find_element_by_xpath(f'//*[@id="{id}"]/*[{start}]').text
                start += 1
                yield (tag_id, text)
            except NoSuchElementException:
                break


if __name__ == '__main__':
    main_class = list(get_main_class('treeZhiBiao_1_ul'))
    for _class in main_class:
        _id, name = _class
        print(_id, name)
        # make_dir(name)
        # with Chrome() as c:
        #     driver = c.driver
        #     digui(driver, _id)
