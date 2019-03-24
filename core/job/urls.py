from django.conf.urls import url
from core.job.views import TweetFetchSaveJob, TweetPredictionJob

urlpatterns = [
    url(r'^save-tweets/', TweetFetchSaveJob.as_view(), name="job-save-tweets"),
    url(r'^tweet-prediction/', TweetPredictionJob.as_view(), name="job-predict-tweets"),
]
