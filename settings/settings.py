import os.path


""" LinkedIn Email and Password """
username = 'test@test.com'
password = 'password'

""" Message to send HR """
message = 'Здравствуйте, я Junior Python разработчик с опытом программирования более 7 месяцев. ' \
          'Я ищу работу и буду рад, если вы добавите меня в друзья.'

""" Search filters """
geo = '%5B"ru%3A0"%5D'      # Геолокация - Россия
job_position = 'hr'         # Профессия - HR
industry = '%5B"96"%5D'     # Сфера деят-ти  - IT
search_filters = [geo, job_position, industry]

""" Import email and password during development """
if os.path.isfile('local_settings.py'):
    from local_settings import *
