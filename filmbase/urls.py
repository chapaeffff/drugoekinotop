#from django.urls import include, path
from django.conf.urls import include, url


from . import views

app_name = 'filmbase'

urlpatterns = [
    url('(?P<pk>\d+)/$', views.film_detail, name='film_detail'),

]
