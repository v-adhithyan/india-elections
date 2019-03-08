from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.urls import reverse

from core.models import Wordcloud
from core.twitter import utils
from core.twitter.twitter_api import TwitterApi


def hello_world(request):
    return HttpResponse("India 2k19 - Visualizations")


class POC(TemplateView):
    template_name = "poc.html"


def index(request):
    data = utils.generate_view_data("upa", "nda", remove=True)
    return render(request=request, template_name="new.html", context=data)


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
        except FileNotFoundError:
            return HttpResponse("Please try again later.", status=422)

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
            return HttpResponse("param q is required", status=422)


def tn(request):
    data = utils.generate_view_data("admk", "dmk")
    return render(request=request, template_name="new.html", context=data)


def terms_and_conditions(request):
    return render(request=request, template_name='terms.html')


def new_ui_proto(request):
    data = utils.generate_view_data("admk", "dmk")
    return render(request=request, template_name="new.html", context=data)


def whatsup_with_tweets(request):
    q = request.GET.get('q')
    wordcloud_url = reverse("get-word-cloud") + "?q={}".format(q)
    data = {"title": q, "img_href": wordcloud_url}
    return render(request=request, template_name='wc.html', context=data)
