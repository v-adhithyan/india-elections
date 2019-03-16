# india-elections [![Waffle.io - Columns and their card count](https://badge.waffle.io/v-adhithyan/india-elections.svg?columns=all)](https://waffle.io/v-adhithyan/india-elections)
[![Build Status](https://travis-ci.com/v-adhithyan/india-elections.svg?branch=master)](https://travis-ci.com/v-adhithyan/india-elections)
[![codecov](https://codecov.io/gh/v-adhithyan/india-elections/branch/master/graph/badge.svg)](https://codecov.io/gh/v-adhithyan/india-elections)

  Lets visualize India elections 2019 . (UPS vs NDA). [Work in progress.]
## Prerequisites
  - Make sure Python 3.6 is installed or a version of Python greater than 3.6
  - Developed in mac / ubuntu.
  - Install virtualenv.  (https://gist.github.com/frfahim/73c0fad6350332cef7a653bcd762f08d)

## Running in local
  - Clone this repostiory ```git clone https://github.com/v-adhithyan/india-elections```
  - cd to the repo ```cd india-elections```
  - Create virtualenv ```virtualenv elections```
  - Activate virtualenv ```source elections/bin/activate```
  - Install dependencies ```pip install -r requirements.txt```
  - create a .env file and add the following contents and replace secrets with your's
    ```
    DJANGO_SETTINGS_MODULE='indiaelections.settings'
    SENTRY_TOKEN='your sentry token'
    TW_CONSUMER_KEY='your twitter consumer key'
    TW_CONSUMER_SECRET='your twitter consumer secret'
    TW_ACCESS_TOKEN='twitter access token'
    TW_ACCESS_TOKEN_SECRET='twitter access token secret'
    DB_HOST = "localhost"
    DB_NAME='indiaelections'
    DB_USERNAME='indiaelections'
    DB_PASSWORD='some password'
    MYSQL='0'
    MEMCACHE_DISTRIBUTED='0'
    MEMCACHE_LOCATION='memcache host'
    MEMCACHE_USERNAME='memcache username'
    MEMCACHE_PASSWORD='memcache password'
    DEV_STATIC='1'
    ```
  - Migrate the app ```python manage.py migrate```
  - Start server ```python manage.py runserver```
  - Open browser and go to localhost:8000/ - You will see India elections 2k19 - visulizations

## Pre commit hooks

  At the root directory, run the following command to add pre commit hook.
  ```
  flake8 --install-hook git
  git config --bool flake8.strict true
  ```
## POC
  - <https://indiaelections.pythonanywhere.com/poc>

## Contributors
  - [Ayyappan Thirunavukarasu](https://github.com/ayps)
  - [Adhithyan Vijayakumar](https://github.com/v-adhithyan)


## Todo

- [ ] Use pre-commit library for pre-commit hooks
- [ ] Write more unit tests/ fix failing tests
- [ ] Add contributing and Pull request template
- [ ] Refactor code, use wily, rope, improve maintainabilty

## License
 - MIT
