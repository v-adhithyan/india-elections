from django.http.response import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
from core.twitter.utils import generate_word_cloud


def hello_world(request):
    return HttpResponse("India 2k19 - Visualizations")


class poc(TemplateView):
    template_name = "poc.html"


def get_word_cloud(request):
    if request.GET.get('q'):
        q = request.GET['q']
        with open(generate_word_cloud(q=q), "rb") as f:
            return HttpResponse(f.read(), content_type='image/png')

    return HttpResponse("A query parameter q is required to generate word cloud")
