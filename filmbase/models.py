# -*- coding: utf-8 -*-

from django.utils import timezone

from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible

from transliterate import translit

import uuid

from video.models import Video


# from images.models import *



@python_2_unicode_compatible
class Director(models.Model):
    name = models.CharField(max_length=120)
    image = models.CharField(max_length=400, default = '', blank = True)
    kp_id = models.PositiveIntegerField(unique=True)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Film(models.Model):
    title = models.CharField(max_length=150, blank = True)
    title_en = models.CharField(max_length=150, blank=True)
    title_alter = models.CharField(max_length=150, blank=True)
    image = models.CharField(max_length=400, default = '', blank = True)
    first_image = models.ForeignKey('images.Shot',on_delete=models.CASCADE, null = True, blank = True)

    director = models.ForeignKey('Director',on_delete=models.PROTECT, null = True, blank = True, )
    year = models.PositiveIntegerField(null = True, blank = True)
    runtime = rating = models.PositiveSmallIntegerField(null = True, blank = True)
    videovk = models.CharField(max_length=400, null = True, blank = True)
    material = models.TextField(blank=True)
    kp_id = models.PositiveIntegerField(unique = True, null = True, blank = True)
    budget = models.PositiveIntegerField(null=True, blank=True)
    rating = models.FloatField(null = True, blank = True)
    votes = models.PositiveIntegerField(null = True, blank = True)
    imdb_rating = models.FloatField(null = True, blank = True)
    imdb_votes = models.PositiveIntegerField(null=True, blank=True)
    # stars = models.ManyToManyField('Actor',  null = True, blank = True,)
    kp_plot = models.TextField(blank = True)
    moratory10 = models.PositiveSmallIntegerField(blank = True, null = True) #1 - wait a bit, #10 - wait a lot

    release = models.DateTimeField(blank = True, null = True)
    profit_usa = models.PositiveIntegerField(null=True, blank=True)
    profit_russia = models.PositiveIntegerField(null=True, blank=True)

    last_search = models.DateTimeField(blank = True, null = True)

    slug = models.SlugField(max_length=200, default=uuid.uuid4, unique=True)

    modified = models.DateTimeField(blank=True, null = True)

    def videos(self, long = False):
        vs = Video.objects.filter(film = self)
        return vs


    def __str__(self):
        try: fulltitle= self.title + ' / ' + self.director.name + ' ' + self.year
        except: fulltitle = self.title #+ 'no dir'
        return fulltitle.encode('utf8')


    def save(self, *args, **kwargs):
        # if not self.id:
        # Only set the slug when the object is created.
        self.slug = '{0}-{1}'.format(self.pk,
                                     slugify(translit(self.title +'-'+str(self.year),
                                                      'ru', reversed=True)))
        self.modified = timezone.now()
        super(Film, self).save(*args, **kwargs)


    # def moonwalked(self):
    #     if self.player:
    #         if 'moonwalk' in self.player:
    #             return True
    #     else:
    #         return False

# default to 1 day from now
# def get__film_slug(self):
#     try:
#         fulltitle = self.title + ' / ' + self.director.name + ' ' + self.year
#     except:
#         fulltitle = self.title  # + 'no dir'
#     return fulltitle
#
#
#
# class MyModel(models.Model):
#   my_date = models.DateTimeField(default=get_default_my_date)