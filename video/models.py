# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.

from filmbase.models import *


class VideoBase(models.Model):
    video_id = models.PositiveIntegerField(null=True, blank=True)
    owner_id = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('video_id', 'owner_id',)
        abstract = True

    title = models.CharField(max_length=150, null=True, blank=True)
    film = models.ForeignKey('filmbase.Film', on_delete=models.PROTECT, null=True, blank=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    date = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveSmallIntegerField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return 'Untitled'


class Video(VideoBase):
    # video_id = models.PositiveIntegerField(null = True, blank = True)
    # owner_id = models.IntegerField(null=True, blank=True)
    #
    # class Meta:
    #     unique_together = ('video_id', 'owner_id',)
    #
    # title = models.CharField(max_length=150, null = True, blank = True)
    # #film = models.ForeignKey('filmbase.Film', on_delete=models.PROTECT, null = True, blank = True)
    # duration = models.PositiveIntegerField(null = True, blank = True)
    # date = models.PositiveIntegerField(null=True, blank=True)
    # width = models.PositiveSmallIntegerField(null = True, blank = True)
    # height = models.PositiveSmallIntegerField(null=True, blank=True)

    views = models.PositiveIntegerField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    photo = models.CharField(max_length=150, null=True, blank=True)
    first_frame = models.CharField(max_length=150, null=True, blank=True)
    player = models.CharField(max_length=250, null=True, blank=True)
    hd = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    kp_id = models.PositiveIntegerField(null=True, blank=True)
    prop_title = models.BooleanField(blank=True, default=False)
    deleted = models.BooleanField(blank=True, default=False)
    # timeout = models.PositiveSmallIntegerField (null = True, blank = True)