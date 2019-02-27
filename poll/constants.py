import os

from dotenv import load_dotenv

load_dotenv()

OPINION_POLL_OPTIONS = (
    ('c', 'UPA - Congress - DMK'),
    ('b', 'NDA - BJP - ADMK - PMK'),
    ('o', 'Others'),
    ('n', 'Nota'),
)

GENDER = (
    ('m', 'Male'),
    ('f', 'Female')
)

GOOGLE_RECAPTCHA_SITE_KEY = os.environ.get("RECAPTCHA_SITE_KEY", "")
GOOGLE_RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
