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

SKY_BLUE = "#87ceeb"
SAFFRON = "#F97D09"
GREEN = "#006400"
RED = "#ff0000"

PARTIES_COLOR = {
    'upa': SKY_BLUE,
    'nda': SAFFRON,
    'admk': GREEN,
    'dmk': RED
}

TW_CONSUMER_KEY = os.environ["TW_CONSUMER_KEY"]
TW_CONSUMER_SECRET = os.environ["TW_CONSUMER_SECRET"]
TW_ACCESS_TOKEN = os.environ["TW_ACCESS_TOKEN"]
TW_ACCESS_TOKEN_SECRET = os.environ["TW_ACCESS_TOKEN_SECRET"]
