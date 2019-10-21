from django.contrib import admin
from .models import *
from video.models import Video

from django.forms import TextInput, Textarea
from django.db import models


# Register your models here.

class ListAdmin(admin.ModelAdmin):
    pass
    ordering = ('id',)

admin.site.register(List, ListAdmin)
admin.site.register(Author)
admin.site.register(Section)
admin.site.register(Review)




class Film_List_Elem_Admin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':22, 'cols':100})},
    }


admin.site.register(Film_List_Elem, Film_List_Elem_Admin)
# admin.site.register(YourModel, YourModelAdmin)






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