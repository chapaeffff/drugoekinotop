from django.conf.urls import include, url

from . import views

urlpatterns = [
    # url(r'^$', views.vkgrab, name='vkgrab'),
    url(r'^top/$', views.vktop, name='vktop'),
    # url(r'^$', views.vktop, name='vktop'),


    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'lists/$', views.lists, name='lists'),
    # url(r'lists/(?P<slug>[\w-]+)/$', views.list, name='list'),
    # url('',  views.lists, name='lists' ),

    # (?P<slug>[\w-]+)/$
# url(r'lists/<slug:slug>/', views.list, name='list'),

#    path('lists/(?P<slug>[-\w]+)/$', views.list, name='list'),

]
