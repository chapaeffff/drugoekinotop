from django.conf.urls import include, url

from . import views

urlpatterns = [

    url(r'^get_posts/$', views.get_posts, name='get_posts'),
    url(r'^get_videos/$', views.get_videos, name='get_videos'),
    url(r'^get_hidden/$', views.get_hidden, name='get_hidden'),
    url(r'^new_fulls/$', views.new_fulls, name='new_fulls'),
    # url(r'^test_func/$', views.test_func, name='test_func'),
    url(r'^test_func2/$', views.test_func2, name='test_func2'),
    url(r'^update_kp/$', views.update_kp, name='update_kp'),
    url(r'^no_long_videos_feed2file/$', views.no_long_videos_feed2file, name='no_long_videos_feed2file'),
    url(r'^no_long_videos_get_from_file/$', views.no_long_videos_get_from_file, name='no_long_videos_get_from_file'),
    url(r'^list_concepts/$', views.list_concepts, name='list_concepts'),
    url(r'^posts2concept/$', views.posts2concept, name='posts2concept'),


    url(r'^check_videos/$', views.check_videos, name='check_videos'),
    url(r'^calc_rating/$', views.calc_rating, name='calc_rating'),
    url(r'^concept_rating/$', views.concept_rating, name='concept_rating'),



    url(r'^not_linked/$', views.not_linked, name='not_linked'),

    url(r'^find_new_long_2file/$', views.find_new_long_2file, name='find_new_long_2file'),

    url(r'^upload_2_private/$', views.upload_2_private, name='upload_2_private'),
    url(r'^delete_broken_video/$', views.delete_broken_video, name='delete_broken_video'),

    url(r'^$', views.vkgrab, name='vkgrab'),

    # url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    # url(r'lists/$', views.lists, name='lists'),
    # url(r'lists/(?P<slug>[\w-]+)/$', views.list, name='list'),
    # url('',  views.lists, name='lists' ),

    # (?P<slug>[\w-]+)/$
# url(r'lists/<slug:slug>/', views.list, name='list'),

#    path('lists/(?P<slug>[-\w]+)/$', views.list, name='list'),

]
