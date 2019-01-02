from urllib.parse import parse_qs

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
from core.twitter.utils import generate_word_cloud, generate_view_dict


def hello_world(request):
    return HttpResponse("India 2k19 - Visualizations")


class poc(TemplateView):
    template_name = "poc.html"


def index(request):
    data = generate_view_dict()
    return render(request=request, template_name="index.html", context=data)


def get_word_cloud(request):
    if request.GET.get('q'):
        q = request.GET['q'].replace(" ", '+')
        try:
            with open(generate_word_cloud(q=q), "rb") as f:
                return HttpResponse(f.read(), content_type='image/png')
        except ValueError:
            return HttpResponse("Unknown error occured. Please try later", status=500)

    return HttpResponse("A query parameter q is required to generate word cloud")
