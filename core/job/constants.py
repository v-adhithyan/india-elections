from core.twitter.bot import (tweet_all,
                              tweet_prediction_for_india,
                              tweet_prediction_for_tamilnadu)

PLACE_PREDICTION_DICT = {
    "tn": tweet_prediction_for_tamilnadu,
    "india": tweet_prediction_for_india,
    "all": tweet_all
}
