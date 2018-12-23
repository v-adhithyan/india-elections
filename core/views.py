from django.http.response import HttpResponse
from django.views.generic import TemplateView
# Create your views here.


def hello_world(request):
    return HttpResponse("India 2k19 - Visualizations")


class poc(TemplateView):
    template_name = "poc.html"
