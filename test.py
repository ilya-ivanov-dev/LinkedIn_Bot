import time, datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from db_use import db_save
from settings.settings import message, search_filters, username, password


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
        if search_f['geo']:
            geo = f"?facetGeoRegion={search_f['geo']}"
        if search_f['job']:
            job = f"&title={search_f['job']}"
        if search_f['ind']:
            ind = f"&facetIndustry={search_f['ind']}"
        self.search_filters_url = f'{self.search_url}{geo}{job}{ind}'

    def _nav(self, url):
        """ Go to page """
        self.browser.get(url)

    def login(self, username, password):
        """ Login to LinkedIn account """
        self._nav(self.login_url)
        self.browser.find_element_by_id('username').send_keys(username)
        self.browser.find_element_by_id('password').send_keys(password)
        self.browser.find_element_by_class_name('btn__primary--large').click()

    def search(self):
        """ Go to the search results page """
        self._nav(self.search_filters_url)
        self.scroll_end_page()

    def scroll_end_page(self):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.END)  # прокрутка до конца страницы
        time.sleep(2)

    def page_search_result(self):
        return self.browser.find_elements_by_class_name("search-result__wrapper")       # список контактов HR

    def page_href_list(self):
        return self.browser.find_elements_by_class_name("search-result__result-link")   # список ссылок на страницы HR

    def page_connect_buttons(self):
        return self.browser.find_elements_by_class_name("search-result__action-button") # список кнопок Connect

    def send_message(self, name, message):
        self.browser.find_element_by_xpath("//button[@data-control-name='srp_profile_actions']")
        pass

    def connect_and_save_contacts(self):
        """ Отправка сообщения (через Connect) и запись контакта в БД """
        i = 0
        href_list = self.page_href_list()
        search_res = self.page_search_result()
        for result in search_res:
            res = result.text
            N = res.count('\n')
            #   0            2    -4    -3             -1
            # name | 2nd  | 2nd | job | geo | sh_c | connect    N == 6  2nd degree connection
            #   0            2          -3     -2      -1
            # name | name | 3rd | 3rd | job | geo  | connect    N == 6  3rd degree connection
            #   0                 -3    -2      -1
            # name | 3rd  | 3rd | job | geo | connect           N == 5
            # LinkedIn Member (without button Connect)          N == 3
            res_elem = res.split('\n')  # информация о HR

            # Проверка контакта на доступность, отправка сообщения через Connect и запись в БД
            if (N == 5 or N == 6) and res_elem[-1] == 'Connect':
                # Определяем текущие дату и время
                tz = pytz.timezone('Europe/Moscow')
                now = datetime.datetime.now(tz)
                date_now = now.strftime("%d-%m-%Y")
                time_now = now.strftime("%H-%M-%S")

                href = href_list[i].get_attribute("href")
                contact = {
                    'date': date_now,
                    'time': time_now,
                    'name': res_elem[0],
                    'status': res_elem[-1],
                    'href': href,
                }
                if res_elem[2] == '2nd':
                    contact['job'] = res_elem[-4]
                    contact['geo'] = res_elem[-3]
                else:
                    contact['job'] = res_elem[-3]
                    contact['geo'] = res_elem[-2]
                db_save(contact)
            i += 2  # При парсинге получаем по 2 ссылки на контакт, поэтому берем каждую 2-ю

    def next_page(self):
        """ Go to the next search page """
        self.browser.find_element_by_xpath("//button[@aria-label='Next']").click()
        time.sleep(1)
        self.scroll_end_page()

    def start_bot(self):
        """ Parsing search results pages """
        # self.login(username, password)
        self.search()
        while True:
            self.connect_and_save_contacts()
            self.next_page()


if __name__ == '__main__':
    """ Run LinkedinBot """
    bot = LinkedinBot(search_filters)
    bot.start_bot()
