from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Alliance, Wordcloud
from core.permissions import LocalAccess
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


class AllianceCrud(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data = utils.get_candidate_and_party_dict()
        return Response(status=200, data=data, content_type='application/json')

    def post(self, request):
        q = request.data.get('q')
        party = request.data.get('party')

        if q and party and len(party) >= 1:
            Alliance.add(q, party[0])
            return HttpResponse("success", status=200)
        else:
            return HttpResponse("q and party should be present", status=422)

    def delete(self, request):
        q = request.data.get('q')
        _ = request.data.get('party')

        try:
            a = Alliance.objects.get(q=q)
            a.delete()
        except Alliance.DoesNotExist:
            return HttpResponse("does not exist.", status=422)
        return HttpResponse("success", status=200)

    def patch(self, request):
        q = request.data.get('q')
        party = request.data.get('party')
        try:
            a = Alliance.objects.get(q=q)
            a.q = q
            a.party = party[0]
            a.save()
        except Alliance.DoesNotExist:
            return HttpResponse("does not exist.", status=422)
        return HttpResponse("success", status=200)


class TweetJob(APIView):
    permission_classes = (IsAuthenticated, LocalAccess)

    def get(self, request):
        try:
            q = request.GET['q']
            api = TwitterApi()
            api.get_and_save_tweets(query=q)
            return HttpResponse("success", status=200)
        except KeyError:
            return HttpResponse("param q is required", status=422)
