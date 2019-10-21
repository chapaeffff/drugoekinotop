# from django.conf.urls import url
# from . import views
#
# urlpatterns = [
#     url(r'^$', views.post_list, name='post_list'),
#     url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
#     url(r'^post/new/$', views.post_new, name='post_new'),
# 	url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
#
#     url(r'^directors/', views.directors_list, name = 'directors'),
# 	url(r'^director/(?P<pk>\d+)/$', views.director_detail, name='director_detail'),
# 	url(r'^film/(?P<pk>\d+)/$', views.film_detail, name='film_detail'),
#
#
#     url(r'^items/', views.items_list, name = 'items'),
#     url(r'^film_items/', views.film_items_list, name = 'film_items'),
#
#     url(r'^list/(?P<pk>\d+)/$', views.list, name='list'),
#
#
#
# ]

#from django.urls import include, path

from django.conf.urls import include, url
from django.urls import path


from . import views

urlpatterns = [

    url(r'adm/(?P<slug>[\w-]+)$', views.list_adm, name='list_adm'),
    url(r'(?P<slug>[\w-]+)$', views.list, name='list'),
    # url(r'$', views.lists, name='lists'),
    path('', views.lists, name='lists'),
    path('adm/', views.lists_adm, name='lists_adm'),

    # url('',  views.index, name='index' ),


    # (?P<slug>[\w-]+)/$
# url(r'lists/<slug:slug>/', views.list, name='list'),

#    path('lists/(?P<slug>[-\w]+)/$', views.list, name='list'),

]
