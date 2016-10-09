import os

SECRET_KEY = os.getenv('SECRET_KEY')
LANG = os.getenv('LANG', 'en')
PUSHOVER_TOKEN = os.getenv('PUSHOVER_TOKEN')
PUSHOVER_KEY = os.getenv('PUSHOVER_KEY')
