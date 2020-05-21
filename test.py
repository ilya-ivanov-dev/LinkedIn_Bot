import time, datetime

import pytz as pytz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from db_use import db_save
# from settings import username, password


class LinkedinBot:
    def __init__(self, search_f):
        """ Opening Operadriver with VPN and sets urls """
        browser_options = webdriver.ChromeOptions()
        opera_config = '/home/dan/.config/opera'
        browser_options.add_argument('user-data-dir=' + opera_config)
        self.browser = webdriver.Opera(options=browser_options)

        self.base_url = 'https://www.linkedin.com'
        self.login_url = f'{self.base_url}/login'
        self.search_url = f'{self.base_url}/search/results/people/'

        """ Filter search url """
        if search_f[0]:
            geo = f'?facetGeoRegion={search_f[0]}'
        if search_f[1]:
            pos = f'&title={search_f[1]}'
        if search_f[2]:
            ind = f'&facetIndustry={search_f[2]}'
        self.search_filters_url = f'{self.search_url}{geo}{pos}{ind}'

    def _nav(self, url):
        self.browser.get(url)

    def login(self, username, password):
        """ Login to LinkedIn account """
        self._nav(self.login_url)
        self.browser.find_element_by_id('username').send_keys(username)
        self.browser.find_element_by_id('password').send_keys(password)
        self.browser.find_element_by_class_name('btn__primary--large').click()

    def search(self):
        self._nav(self.search_filters_url)

    def parse(self):
        """ Parsing result data """
        search_results_list = []
        self.browser.find_element_by_tag_name('body').send_keys(Keys.END)   # прокрутка до конца страницы
        time.sleep(1)

        search_result = self.browser.find_elements_by_class_name("search-result__wrapper")
        href_list = self.browser.find_elements_by_class_name("search-result__result-link")

        i = 0
        for result in search_result:
            res = result.text
            href = href_list[i].get_attribute("href")
            i += 2
            N = res.count('\n')
            res_elem = res.split('\n')

            tz = pytz.timezone('Europe/Moscow')
            now = datetime.datetime.now(tz)
            date_now = now.strftime("%d-%m-%Y")
            time_now = now.strftime("%H-%M-%S")

            if N == 5 or N == 6:    # Доступные контакты
                row = {
                    'date': date_now,
                    'time': time_now,
                    'name': res_elem[0],
                    'job_position': res_elem[3],
                    'href': href,
                    'geo': res_elem[4],
                    'status': res_elem[-1]
                }
                search_results_list.append((row['date'], row['time'], row['name'], row['job_position'],
                                            row['href'], row['geo'], row['status']))
        return search_results_list



if __name__ == '__main__':

    """ Search filters """
    geo = '%5B"ru%3A0"%5D'      # Геолокация - Россия
    job_position = 'hr'         # Профессия - HR
    industry = '%5B"96"%5D'     # Сфера  - IT
    search_filters = [geo, job_position, industry]

    """ Run LinkedinBot """
    bot = LinkedinBot(search_filters)
    # bot.login(username, password)
    bot.search()
    contacts = bot.parse()
    db_save(contacts)

    print()


