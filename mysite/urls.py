# from django.conf.urls import include, url
# from django.contrib import admin
# from feed.models import LatestEntriesFeed
#
#
# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'', include('blog.urls')),
#     url(r'^latest/feed/', LatestEntriesFeed()),
#
# ]

from django.contrib import admin
from django.conf.urls import include, url




urlpatterns = [

    url(r'admin/', admin.site.urls),
    url(r'film/', include ('filmbase.urls')),


    url('', include('blog.urls')),

]
