"""indiaelections URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt import views as jwt_views

from core import views

urlpatterns = [
    url(r'^$', cache_page(600)(views.index), name="home"),
    url(r'^terms-and-conditions', cache_page(24 * 60 * 60)(views.terms_and_conditions), name="tandc"),
    url(r'^admin/', admin.site.urls),
    # url(r'', views.hello_world),
    # url(r'^poc/', cache_page(600)(views.POC.as_view()), name='poc'),
    url(r'^india/', views.index, name='index'),
    url(r'^tn/', views.tn, name='tn'),
    url(r'^wordcloud/', cache_page(600)(views.get_word_cloud), name="get-word-cloud"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^job/', views.TweetJob().as_view(), name="tweet-fetcher-job"),
    url('alliance/', views.AllianceCrud.as_view(), name='crud-alliance'),
    url(r'^poll/', include('poll.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
