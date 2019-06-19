from django.conf.urls import include, url
from django.contrib import admin

from . import views

# addfilm_url = reverse('admin:filmbase_film_add')
app_name = 'filmscrap'

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^searching/$', views.searching, name='searching'),
    # url(r'^addfilm/$', addfilm_url, name = 'addfilm'),
    url(r'film/new/$', views.film_new, name='film_new'),
    url(r'^video/dechaos/$', views.video_dechaos, name='video_dechaos'),
    url(r'^video/addbylink/$', views.video_addbylink, name='video_addbylink'),
    url(r'^video/link2form/$', views.video_link2form, name='video_link2form'),

    url('', views.filmscrap, name='filmscrap'),
    # url('^post/new/', admin.
    #     views.post_new, name='post_new'),


    # url(r'^get_suggs/$', views.get_suggested, name='get_suggested'),
    # url(r'^get_videos/$', views.get_videos, name='get_videos'),
    # url(r'^get_hidden/$', views.get_hidden, name='get_hidden'),

    # url(r'^$', views.suggested, name='suggested'),

    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'lists/$', views.lists, name='lists'),
    # url(r'lists/(?P<slug>[\w-]+)/$', views.list, name='list'),
    # url('',  views.lists, name='lists' ),

    # (?P<slug>[\w-]+)/$
# url(r'lists/<slug:slug>/', views.list, name='list'),

#    path('lists/(?P<slug>[-\w]+)/$', views.list, name='list'),

]
