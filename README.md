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
  - Migrate the app ```python manage.py migrate```
  - Start server ```python manage.py runserver```
  - Open browser and go to localhost:8000/ - You will see India elections 2k19 - visulizations

## POC
  - <https://indiaelections.pythonanywhere.com/poc>

## Contributors
  - [Ayyappan Thirunavukarasu](https://github.com/ayps)
  - [Adhithyan Vijayakumar](https://github.com/v-adhithyan)

## License
 - MIT

