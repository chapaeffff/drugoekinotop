from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Concept)
admin.site.register(Connection)
admin.site.register(ConnectionFilm)
admin.site.register(ConnectionTag)
admin.site.register(Tag)
admin.site.register(ConnectionVKPost)


#
# class Concept(models.Model):
#     # class Meta:
#     #     abstract = True
#     comment = models.CharField(max_length=200)
#     def __str__(self):
#         return self.comment[:100]
# #
# class Connection(models.Model):
#     concept = models.ForeignKey('Concept', on_delete=models.CASCADE)
#     class Meta:
#         abstract = True
#     comment = models.CharField(max_length=200)
#     def __str__(self):
#         return self.comment[:100]
#
# class  ConnectionFilm(Connection):
#     film = models.ForeignKey("filmbase.Film", on_delete=models.CASCADE)
#
# class Tag (models.Model):
#     tag=  models.CharField(max_length=50)
#
#
# class  ConnectionTag(Connection):
#     tag = models.ForeignKey("Tag", on_delete=models.CASCADE) #например тег - советские / мультфильмы, пересекаем получаем советские муль
#
# class  ConnectionVKPost(Connection):
#     # post_fid  = models.CharField(max_length=100)
#     post = models.ForeignKey('vkposts.VKPost', on_delete=models.CASCADE)