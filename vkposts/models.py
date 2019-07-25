# -*- coding: utf-8 -*-

from django.db import models
from video.models import Video


import re

# Create your models here.

class VKPostBase(models.Model):
    class Meta:
        abstract = True
    post_id = models.PositiveIntegerField()
    owner_id = models.SmallIntegerField()
    date = models.PositiveIntegerField()
    text = models.TextField()
    def __str__(self):
        return  self.text[:80] + str(self.post_id)


class VKPost(VKPostBase):
    # post_id = models.PositiveIntegerField()
    # owner_id = models.SmallIntegerField()
    # date = models.PositiveIntegerField()
    # text = models.TextField()
    reposts = models.PositiveIntegerField(blank=True, null = True)
    updated = models.DateTimeField(auto_now=True)
    show_in_raw_rating = models.BooleanField(default=True)
    widget = models.TextField(blank=True)
    blocked = models.BooleanField(default=False)
    side_video = models.BooleanField(blank = True, default = False)
    copy = models.BooleanField(blank = True, default = False)

    @property
    def first_line(self):
        return self.text.split(sep='\n')[0]

    @property
    def till_slash(self):
        till_slash = self.first_line.split(sep='/')[0].strip()
        till_slash = till_slash.split(sep='(')[0].strip()
        return till_slash

    @property
    def year_in_line(self):
        try:
            year = re.findall(r'\d+', self.first_line)[-1]
        except:
            year = None
        return year






class VKAtt(models.Model):
    type = models.CharField(max_length=30)
    order = models.PositiveSmallIntegerField()
    post_owner = models.ForeignKey('VKPost', on_delete=models.CASCADE)

class VideoAtt(VKAtt):
    # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
    video = models.ForeignKey("video.Video", on_delete=models.SET_NULL, null=True)

class Photo(models.Model):
    photo_id  = models.PositiveIntegerField()
    owner_id = models.SmallIntegerField()
    full_att = models.TextField()


class PhotoAtt(VKAtt):
    # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
    photo = models.ForeignKey("Photo", on_delete = models.SET_NULL, null = True)

class ElseAtt(VKAtt):
    # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
    att_text = models.TextField()



