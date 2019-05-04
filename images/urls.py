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

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


from . import views



urlpatterns = [
url(r'^new/$', views.image_new, name='image_new'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
