from django.contrib import admin
from .models import *
from video.models import Video

# Register your models here.

admin.site.register(List)
admin.site.register(Film_List_Elem)
admin.site.register(Video)



# from django.contrib import admin
# from .models import * #Post, Director, List_Elem, Film, Film_List_Elem
#
# admin.site.register(Post)
# admin.site.register(Director)
# #admin.site.register(List_Elem)
# admin.site.register(Film)
# admin.site.register(Film_List_Elem)
# admin.site.register(List)
# admin.site.register(Inbox)
# admin.site.register(Video)