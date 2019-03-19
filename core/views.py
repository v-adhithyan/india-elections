from django.http.response import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.models import Wordcloud
from core.twitter import utils
from core.twitter.twitter_api import TwitterApi
from core.constants import ALL_TIME, TIMERANGE_DICT, TIMERANGE_DISPLAY


def hello_world(request):
    return HttpResponse("India 2k19 - Visualizations")


class POC(TemplateView):
    template_name = "poc.html"


@csrf_exempt
def index(request):
    # default range to all time if range is invalid or not in query params
    range = request.GET.get('range', ALL_TIME)

    if range not in TIMERANGE_DICT.keys():
        range = ALL_TIME

    data = utils.generate_view_data("upa", "nda", remove=True, timerange=range)
    data.update({"range": TIMERANGE_DISPLAY.get(range, ALL_TIME)})
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


@csrf_exempt
def tn(request):
    range = request.GET.get('range', ALL_TIME)

    if range not in TIMERANGE_DICT.keys():
        range = ALL_TIME

    data = utils.generate_view_data("admk", "dmk", timerange=range)
    data = utils.generate_view_data("admk", "dmk", timerange=range)
    data.update({"range": TIMERANGE_DISPLAY.get(range, ALL_TIME)})
    return render(request=request, template_name="new.html", context=data)

@csrf_exempt
def terms_and_conditions(request):
    return render(request=request, template_name='terms.html')


def new_ui_proto(request):
    data = utils.generate_view_data("admk", "dmk")
    return render(request=request, template_name="new.html", context=data)


@csrf_exempt
def whatsup_with_tweets(request):
    q = request.GET.get('q')
    wordcloud_url = reverse("get-word-cloud") + "?q={}".format(q)
    data = {"title": q, "img_href": wordcloud_url}
    return render(request=request, template_name='wc.html', context=data)


@csrf_exempt
def handler404(request, *args, **kwargs):
    response = render_to_response("404.html", {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


@csrf_exempt
def handler500(request, *args, **kwargs):
    response = render_to_response("500.html", {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response


@csrf_exempt
def handler422(request, *args, **kwargs):
    response = render_to_response("422.html", {}, context_instance=RequestContext(request))
    response.status_code = 422
    return response
