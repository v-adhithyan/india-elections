import os

from dotenv import load_dotenv

load_dotenv()

SENTIMENTS = (
    ('p', 'positive'),
    ('n', 'negative'),
    ('e', 'neutral'),
)

PARTIES = (
    ('u', 'upa'),
    ('n', 'nda'),
    ('a', 'admk'),
    ('d', 'dmk')
)

TW_CONSUMER_KEY = os.environ["TW_CONSUMER_KEY"]
TW_CONSUMER_SECRET = os.environ["TW_CONSUMER_SECRET"]
TW_ACCESS_TOKEN = os.environ["TW_ACCESS_TOKEN"]
TW_ACCESS_TOKEN_SECRET = os.environ["TW_ACCESS_TOKEN_SECRET"]
