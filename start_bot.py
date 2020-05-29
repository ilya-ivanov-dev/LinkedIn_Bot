import json
import time
import datetime
import pytz
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from db_use import db_save
from settings.settings import hi, text, search_filters, username, password


with open('settings/names.json', encoding="utf-8") as f:
    file_content = f.read()
    data_names = json.loads(file_content)

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

        # Filter search url
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
        time.sleep(2)

    def scroll_end_page(self):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.END)
        time.sleep(1)

    def scroll_top_page(self):
        self.browser.find_element_by_tag_name("body").send_keys(Keys.HOME)
        time.sleep(1)

    def send_message(self, name_surname, button):
        """ Click Connect and sending message """
        button_connect_id = button.get_attribute('id')
        self.browser.find_element_by_id(f"{button_connect_id}").click()
        self.browser.find_element_by_xpath("//button[@aria-label='Add a note']").click()
        contact_name = name_surname.split(' ')[0]
        if contact_name in data_names.keys():
            name = data_names.get(contact_name)
            message = f'{hi}, {name}.\n{text}'
        else:
            message = f'{hi}!\n{text}'
        self.browser.find_element_by_tag_name("textarea").send_keys(message)
        button_done_aria = self.browser.find_element_by_xpath("//div[@role='dialog']").text.split('\n')[-2]
        self.browser.find_element_by_xpath(f"//button[@aria-label='{button_done_aria}']").click()

    def connect_and_save_contacts(self):
        """ Finding contacts, sending messages (Connect button) and writing contacts to the database """
        self.scroll_end_page()
        i_href = 0
        i_button = 0
        search_res = self.browser.find_elements_by_class_name("search-result__wrapper")  # contact list
        href_list = self.browser.find_elements_by_class_name("search-result__result-link")
        button_list = self.browser.find_elements_by_xpath("//div[@class='search-result__actions']/div")
        for result in search_res:
            res = result.text
            count_enter = res.count('\n')

            #       count_enter as N
            # name | name | 2nd  | 2nd | job | geo | sh_c | Invite sent    N == 7
            #   0            2    -4    -3             -1
            # name | 2nd  | 2nd | job | geo | sh_c | connect    N == 6  2nd degree connection
            #   0            2          -3     -2      -1
            # name | name | 3rd | 3rd | job | geo  | connect    N == 6  3rd degree connection
            #   0                 -3    -2      -1
            # name | 3rd  | 3rd | job | geo | connect           N == 5
            # LinkedIn Member (without button Connect)          N == 3

            res_elem = res.split('\n')  # employee information

            if (count_enter == 5 or count_enter == 6) and res_elem[-1] == 'Connect':
                # Определяем текущие дату и время
                tz = pytz.timezone('Europe/Moscow')
                now = datetime.datetime.now(tz)
                date_now = now.strftime("%d-%m-%Y")
                time_now = now.strftime("%H-%M-%S")

                href = href_list[i_href].get_attribute("href")
                contact = {
                    'date': date_now,
                    'time': time_now,
                    'name': res_elem[0],
                    'status': 'Invite Sent',
                    'href': href,
                }

                if res_elem[2] == '2nd':
                    contact['job'] = res_elem[-4]
                    contact['geo'] = res_elem[-3]
                else:
                    contact['job'] = res_elem[-3]
                    contact['geo'] = res_elem[-2]

                self.scroll_top_page()
                time.sleep(1)
                ActionChains(self.browser).move_to_element(result).perform()
                time.sleep(1)

                button = button_list[i_button]
                self.send_message(contact['name'], button)
                self.scroll_end_page()
                time.sleep(1)

                db_save(contact)

            i_href += 2     # When parsing, we get 2 links to a contact, so we take every 2nd

            # LinkedIn Member contact without a button, skip when passing through the list
            if 5 <= count_enter <= 7:
                i_button += 1

    def next_page(self):
        self.scroll_end_page()
        self.browser.find_element_by_xpath("//button[@aria-label='Next']").click()
        time.sleep(1)

    def start_bot(self):
        """ Parsing contacts on the issuing pages and sending messages """
        # self.login(username, password)
        self.search()
        while True:
            self.connect_and_save_contacts()
            self.next_page()


if __name__ == '__main__':
    """ Run LinkedinBot """
    bot = LinkedinBot(search_filters)
    bot.start_bot()
