from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^opinion-poll/', views.opinion_poll, name='opinion-poll'),

    url(r'^ajax/load-places/', views.load_constituencies, name="opinion-poll-load-places"),
]
