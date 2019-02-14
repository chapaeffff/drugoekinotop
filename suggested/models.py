from django.db import models
from vkposts.models import VKPostBase
from video.models import VideoBase

# Create your models here.

#
class Suggested(VKPostBase):
    from_id = models.PositiveIntegerField(blank=True)
    rating = models.PositiveSmallIntegerField(default=1)


# # class Suggested(models.Model):
# #     post_id = models.PositiveIntegerField()
# #     owner_id = models.SmallIntegerField()
# #     date = models.PositiveIntegerField()
# #     text = models.TextField()
#


class VideoSugg (VideoBase):
    sugg_post = models.ForeignKey('Suggested', on_delete=models.CASCADE)




# class VKAtt(models.Model):
#     type = models.CharField(max_length=30)
#     order = models.PositiveSmallIntegerField()
#     post_owner = models.ForeignKey('VKPost', on_delete=models.CASCADE)
#
# class VideoAtt(VKAtt):
#     # host_att = models.ForeignKey('VKAtt', on_delete=models.CASCADE)
#     video = models.ForeignKey("video.Video", on_delete=models.SET_NULL, null=True)
#
#


#
# class VideoSugg(models.Model):
#
#       name='VideoSugg',
#         fields=[
#             ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
#             ('vid', models.CharField(max_length=10)),
#             ('owner_id', models.CharField(max_length=10)),
#             ('title', models.CharField(max_length=150)),
#             ('sugg', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.Suggested')),
#         ],
#     ),
# ]
