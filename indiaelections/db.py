import os

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# use this flag to enable mysql
# only in production we use mysql
# for dev and testing we will use sqlite
MYSQL = bool(os.getenv("MYSQL", False))

MYSQL_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USERNAME"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': os.environ['DB_HOST'],
        'PORT': '',
    }
}

SQLITE_DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


def get_db_config():
    if MYSQL:
        return MYSQL_DATABASE

    return SQLITE_DATABASE
