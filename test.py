from selenium import webdriver
from settings import username, password


class LinkedinBot:
    def __init__(self):
        """ Opening Operadriver with VPN and sets urls """
        browser_options = webdriver.ChromeOptions()
        opera_config = '/home/dan/.config/opera'
        browser_options.add_argument('user-data-dir=' + opera_config)
        self.browser = webdriver.Opera(options=browser_options)

        self.base_url = 'https://www.linkedin.com'
        self.login_url = f'{self.base_url}/login'
        self.search_url = f'{self.base_url}/search/results/people/'

    def _nav(self, url):
        self.browser.get(url)

    def login(self, username, password):
        """ Login to LinkedIn account """
        self._nav(self.login_url)
        self.browser.find_element_by_id('username').send_keys(username)
        self.browser.find_element_by_id('password').send_keys(password)
        self.browser.find_element_by_class_name('btn__primary--large').click()

    def search(self, geo, pos, ind):
        if geo:
            geo = f'?facetGeoRegion={geo}'

        if pos:
            pos = f'&title={pos}'

        if ind:
            ind = f'&facetIndustry={ind}'

        self._nav(f'{self.search_url}{geo}{pos}{ind}')







if __name__ == '__main__':

    """ Search filters """
    geo = '%5B"ru%3A0"%5D'      # Геолокация - Россия
    job_position = 'hr'         # Профессия - HR
    industry = '%5B"96"%5D'     # Сфера  - IT


    bot = LinkedinBot()
    bot.login(username, password)
    bot.search(geo, job_position, industry)



