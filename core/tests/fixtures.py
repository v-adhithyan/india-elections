import json
import pathlib

import pytest


@pytest.fixture
@pytest.mark.django_db
def tweets():
    tweet_file = pathlib.Path(__file__).resolve().parent / 'tweets.json'
    with open(tweet_file, 'r') as f:
        return json.loads(f.read())
