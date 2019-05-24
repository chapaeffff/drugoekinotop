# -*- coding: utf-8 -*-


from django.db import models
from filmbase.models import Film

# Create your models here.

class Image (models.Model):
    image = models.ImageField(upload_to='uploads/shots/')
    description = models.CharField(max_length=200, blank = True)
    def __str__(self):
        return self.description

class Shot(models.Model):
    image = models.ImageField(upload_to='uploads/shots/')
    movie = models.ForeignKey('filmbase.Film', on_delete=models.PROTECT, null=True, blank=True, )
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.movie.title + ' / ' + self.movie.director.name + ' (' + self.description + ')'

# class Shot (models.Model):
#     image = models.ImageField(upload_to='uploads/shots/')
#     movie = models.ForeignKey('filmbase.Film', on_delete=models.PROTECT, null = True, blank = True, )
#     description = models.CharField(max_length=200, blank = True)
#     def __str__(self):
#         return self.movie.title + ' / ' + self.movie.director.name + ' (' + self.description + ')'