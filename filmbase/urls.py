#from django.urls import include, path
from django.conf.urls import include, url

from . import views

app_name = 'filmbase'

urlpatterns = [
    # url(r'^/$', views.searchkp, name='searchkp'),
    url('(?P<pk>\d+)/$', views.film_detail, name='film_detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^searching/$', views.searching, name='searching'),

]
