from django.db import models
from video.models import Video

# Create your models here.

class VKPost(models.Model):
    post_id = models.PositiveIntegerField()
    owner_id = models.SmallIntegerField()
    date = models.PositiveIntegerField()
    text = models.TextField()
    reposts = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)
    show_in_raw_rating = models.BooleanField(default=True)
    widget = models.TextField(blank=True)
    blocked = models.BooleanField(default=False)
    side_video = models.BooleanField(blank = True, default = False)

    def __str__(self):
        return self.text[:100]

class VKAtt(models.Model):
    type = models.CharField(max_length=30)
    order = models.PositiveSmallIntegerField()
    post_owner =  models.ForeignKey('VKPost', on_delete=models.CASCADE)

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



