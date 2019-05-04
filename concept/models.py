# -*- coding: utf-8 -*-

from django.db import models
from video.models import Video
from filmbase.models import Film

# Create your models here.

#
class Concept(models.Model):
    # class Meta:
    #     abstract = True
    comment = models.TextField()
    k10 = models.PositiveSmallIntegerField(default=10, blank = True)
    def __str__(self):
        try:
            film = ConnectionFilm.objects.get(concept = self)
            if film:
                strname = self.comment[:100] + 'фильм: ' + film.film.title
        except:
            strname = self.comment[:100]


        return strname
#
class Connection(models.Model):
    concept = models.ForeignKey('Concept', on_delete=models.CASCADE)
    # class Meta:
    #     abstract = True
    comment = models.CharField(max_length=200, blank = True)


class  ConnectionFilm(Connection):
    film = models.ForeignKey("filmbase.Film", on_delete=models.CASCADE)

    def __str__(self):
        try:
            strname = 'фильм: ' + self.film.title
        except:
            strname = self.comment[:100]
        return strname



class Tag (models.Model):
    tag=  models.CharField(max_length=50)


class  ConnectionTag(Connection):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE) #например тег - советские / мультфильмы, пересекаем получаем советские муль

class  ConnectionVKPost(Connection):
    # post_fid  = models.CharField(max_length=100)
    post = models.ForeignKey('vkposts.VKPost', on_delete=models.CASCADE)
    # def __init__(self,strname):
    #     try:
    #         self.strname = 'пост: ' + self.post.text[:30]
    #     except:
    #         self.strname = self.comment[:100]
    #
    def __str__(self):
        try:
            strname = 'пост: ' + str(self.post.id) + ' ' \
                      + str(self.post.date) + ' ' + self.post.text[:50]
        except:
            strname = self.comment[:100]
        return strname

#


# class VKPostBase(models.Model):
#     class Meta:
#         abstract = True
#     post_id = models.PositiveIntegerField()
#     owner_id = models.SmallIntegerField()
#     date = models.PositiveIntegerField()
#     text = models.TextField()
#     def __str__(self):
#         return self.text[:100]
#
#
# class VKPost(VKPostBase):
#     # post_id = models.PositiveIntegerField()
#     # owner_id = models.SmallIntegerField()
#     # date = models.PositiveIntegerField()
#     # text = models.TextField()
#     reposts = models.PositiveIntegerField(blank=True, null = True)
#     updated = models.DateTimeField(auto_now=True)
#     show_in_raw_rating = models.BooleanField(default=True)
#     widget = models.TextField(blank=True)
#     blocked = models.BooleanField(default=False)
#     side_video = models.BooleanField(blank = True, default = False)
#     copy = models.BooleanField(blank = True, default = False)
#
#
#
# class VKAtt(models.Model):
#     type = models.CharField(max_length=30)
#     order = models.PositiveSmallIntegerField()
#     post_owner = models.ForeignKey('VKPost', on_delete=models.CASCADE)
#
# class VideoAtt(VKAtt):
#     # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
#     video = models.ForeignKey("video.Video", on_delete=models.SET_NULL, null=True)
#
# class Photo(models.Model):
#     photo_id  = models.PositiveIntegerField()
#     owner_id = models.SmallIntegerField()
#     full_att = models.TextField()
#
#
# class PhotoAtt(VKAtt):
#     # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
#     photo = models.ForeignKey("Photo", on_delete = models.SET_NULL, null = True)
#
# class ElseAtt(VKAtt):
#     # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
#     att_text = models.TextField()
#
#
#
