import os.path


""" LinkedIn Email and Password. Write down your details """
username = 'test@test.com'
password = 'password'

""" Message to send HR """
mes1 = 'Здравствуйте!'
mes2 = ' Я Junior Python разработчик с опытом программирования более полугода. ' \
          'Я в поисках работы и буду рад, если вы добавите меня в друзья.'

""" Search filters """
search_filters = {
    'geo': '%5B"ru%3A0"%5D',        # Геолокация - Россия
    'job': 'hr',                    # Профессия - HR
    'ind': '%5B"96"%5D'             # Сфера деят-ти  - Иформационные технологии и услуги
}

""" Import email and password during development """
if os.path.isfile('local_settings.py'):
    from local_settings import *
