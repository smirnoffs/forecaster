import os

SECRET_KEY = os.environ['SECRET_KEY']
LANG = os.getenv('LANG', 'en')
PUSHOVER_TOKEN = os.environ['PUSHOVER_TOKEN']
PUSHOVER_KEY = os.environ['PUSHOVER_KEY']
