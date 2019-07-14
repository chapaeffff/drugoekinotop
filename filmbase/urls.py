#from django.urls import include, path
from django.conf.urls import include, url

from . import views

app_name = 'filmbase'

urlpatterns = [
    # url(r'^/$', views.searchkp, name='searchkp'),

    # url(r'^post/(?P<slug>.+)/$', views.post_detail, name='post_detail'),
    url(r'(?P<slug>[\w\-]+)$', views.film_detail, name='film_detail'),
    url(r'(?P<pk>\d+)', views.film_detail, name='film_detail'),

    # url(r'(?P<slug>[\w-]+)$', views.list, name='list'),

    url(r'^search/$', views.search, name='search'),
    url(r'^searching/$', views.searching, name='searching'),

]
