from django.http.response import HttpResponse
from rest_framework.views import APIView
import logging

from core.constants import TODAY
from core.job.constants import PLACE_PREDICTION_DICT
from core.job.permissions import JobAccess
from core.twitter.twitter_api import TwitterApi

logging.basicConfig(level=logging.INFO)


class TweetFetchSaveJob(APIView):
    authentication_classes = ()
    permission_classes = (JobAccess, )

    def get(self, request):
        try:
            queries = str(request.GET['q'])
            api = TwitterApi()
            for q in queries.split(","):
                try:
                    logging.info("Tweet fetch job started for {}".format(q))
                    q = q.strip()
                    api.get_and_save_tweets(query=q)
                    logging.info("Tweet fetch job completed for {}".format(q))
                except BaseException as e:
                    logging.info("Tweet fetch job failed for {} :: {}".format(q, repr(e)))
                    pass
                # pass
            return HttpResponse("success", status=200)
        except KeyError:
            return HttpResponse("param q is required", status=422)


class TweetPredictionJob(APIView):
    authentication_classes = ()
    permission_classes = (JobAccess,)

    def get(self, request):
        place = request.GET.get('place', 'all')
        timerange = request.GET.get('timerange', TODAY)
        tweet_prediction = PLACE_PREDICTION_DICT.get(place, None)

        if not tweet_prediction:
            return HttpResponse("Unable to tweet prediction.", status=422)

        tweet_prediction(timerange=timerange)
        return HttpResponse("OK", status=200)
