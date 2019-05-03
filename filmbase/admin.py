from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Director)


class FilmAdmin(admin.ModelAdmin):
    pass
    ordering = ('-id',)

admin.site.register(Film, FilmAdmin)

