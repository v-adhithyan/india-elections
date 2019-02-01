from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import Wordcloud
from core.twitter import utils
from core.twitter.twitter_api import TwitterApi


def hello_world(request):
    return HttpResponse("India 2k19 - Visualizations")


class poc(TemplateView):
    template_name = "poc.html"


def index(request):
    data = utils.generate_view_dict()
    return render(request=request, template_name="index.html", context=data)


def get_word_cloud(request):
    if request.GET.get('q'):
        q = request.GET['q'].replace(" ", '+')
        try:
            with open(utils.get_word_cloud(q=q), "rb") as f:
                return HttpResponse(f.read(), content_type='image/png')
        except ValueError:
            return HttpResponse("Unknown error occured. Please try later", status=500)
        except Wordcloud.DoesNotExist:
            return HttpResponse("Unknown query word.", status=422)

    return HttpResponse("A query parameter q is required to generate word cloud")


class TweetJob(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        try:
            q = request.GET['q']
            api = TwitterApi()
            api.get_and_save_tweets(query=q)
            return HttpResponse("success", status=200)
        except KeyError:
            raise
            return HttpResponse("param q is required", status=422)
