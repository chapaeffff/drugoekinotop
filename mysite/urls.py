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
from django.urls import path, include
from django.conf.urls import include, url

from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static



urlpatterns = [

    path('admin/', admin.site.urls),
    url(r'film/', include ('filmbase.urls', namespace='filmbase')),
    url(r'scrap/', include('filmscrap.urls')),
    url(r'vkgrab/', include('vkgrab.urls')),
    url(r'vk/', include('vkposts.urls')),
    # url(r'lists', include('blog.urls')),
    path('lists/', include('blog.urls')),

    url(r'sugg/', include('suggested.urls')),
    url(r'video/', include('video.urls')),
    url(r'images/', include('images.urls')),
    url(r'concepts/', include('concept.urls')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # url(r'^$', include('index.urls')),
    path('', include('index.urls')),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
