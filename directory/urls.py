from django.conf.urls import url
from directory import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^ajax/search', views.search),
]
