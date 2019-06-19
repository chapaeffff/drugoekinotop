from django.conf.urls import include, url

from . import views

urlpatterns = [

    url(r'^get_posts/$', views.get_posts, name='get_posts'),
    url(r'^get_videos/$', views.get_videos, name='get_videos'),
    url(r'^get_hidden/$', views.get_hidden, name='get_hidden'),
    url(r'^next_post/$', views.next_post, name='next_post'),
    url(r'^test_func/$', views.test_func, name='test_func'),
    url(r'^test_func2/$', views.test_func2, name='test_func2'),

    url(r'^$', views.vkgrab, name='vkgrab'),

    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'lists/$', views.lists, name='lists'),
    # url(r'lists/(?P<slug>[\w-]+)/$', views.list, name='list'),
    # url('',  views.lists, name='lists' ),

    # (?P<slug>[\w-]+)/$
# url(r'lists/<slug:slug>/', views.list, name='list'),

#    path('lists/(?P<slug>[-\w]+)/$', views.list, name='list'),

]
