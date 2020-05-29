import os.path


""" LinkedIn Email and Password. Write down your details """
username = 'test@test.com'
password = 'password'

""" Message to send HR """
hi = 'Greeting'         # Greeting in front of the name (without signs!. And others).
                        # If possible, the name is substituted automatically

text = 'Message'        # The body of the message. Automatically spelled from a new line after greeting

""" Search filters """
search_filters = {
    'geo': '%5B"ru%3A0"%5D',        # Locations - Russia
    'job': 'hr',                    # profession (title) - HR
    'ind': '%5B"96"%5D'             # Industries - Information Technology & Services
}

""" Import email and password during development """
if os.path.isfile('settings/local_settings.py'):
    from settings.local_settings import *
