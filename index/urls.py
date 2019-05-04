from django.conf.urls import  url

from . import views

urlpatterns = [

    url(r'$',  views.index, name='index'),

    # (?P<slug>[\w-]+)/$
# url(r'lists/<slug:slug>/', views.list, name='list'),

#    path('lists/(?P<slug>[-\w]+)/$', views.list, name='list'),

]