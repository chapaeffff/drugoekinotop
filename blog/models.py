from django.db import models
from django.template.defaultfilters import slugify
from transliterate import translit
from django.utils.encoding import python_2_unicode_compatible

from filmbase.models import *

@python_2_unicode_compatible
class List(models.Model):
    title = models.CharField(max_length=400)
    intro = models.TextField()
    slug = models.SlugField(max_length=60, blank=True)
    fin_count = models.PositiveSmallIntegerField(blank = True, null = True)

    def save(self, *args, **kwargs):
        # if not self.id:
        # Only set the slug when the object is created.
        self.slug = slugify(translit(self.title, 'ru', reversed=True))  # Or whatever you want the slug to use
        super(List, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog.views.list_pk', args=[str(self.slug)])

    def __str__(self):
        return self.title


class Film_List_Elem(models.Model):
    film = models.ForeignKey('filmbase.Film', on_delete=models.PROTECT)
    text = models.TextField()
    order = models.IntegerField()
    owner_list = models.ForeignKey('List', on_delete=models.PROTECT, null=True, blank=True, default=1)

    def __str__(self):
        return self.film.title


# from django.db import models
# from django.utils import timezone
# from django.utils.encoding import python_2_unicode_compatible
#
#
#
# class Post(models.Model):
#     author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
#     title = models.CharField(max_length=200)
#     text = models.TextField()
#     created_date = models.DateTimeField(
#             default=timezone.now)
#     published_date = models.DateTimeField(
#             blank=True, null=True)
#
#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()
#
#     def __str__(self):
#         return self.title
#
#
# @python_2_unicode_compatible
# class Director(models.Model):
#     name = models.CharField(max_length=120)
#     image = models.CharField(max_length=400, default = '', blank = True)
#
#     def __str__(self):
#         return self.name
#
# class Film(models.Model):
#     title = models.CharField(max_length=150)
#     image = models.CharField(max_length=400, default = '', blank = True)
#     director = models.ForeignKey('Director',on_delete=models.PROTECT, null = True, blank = True, )
#     year = models.PositiveIntegerField(null = True, blank = True)
#     videovk = models.CharField(max_length=400, null = True, blank = True)
#     material = models.TextField(blank=True)
#     kp_id = models.PositiveIntegerField(null = True, blank = True)
#
#     def __str__(self):
#         return self.title
#
# class Video(models.Model):
#     link  = models.CharField(max_length=150)
#     title = models.CharField(max_length=150)
#     film = models.ForeignKey('Film', on_delete=models.PROTECT, null = True, blank = True)
#     duration = models.PositiveIntegerField(null = True, blank = True)
#     hd = models.PositiveIntegerField(null = True, blank = True)
#     status = models.CharField(max_length=150, null = True, blank = True)
#
#     def __str__(self):
#         return self.title
#
# # LI_CHOICES = (
# #     ('D','Director'),
# #     ('F','Film'),
# # )
#
# # class List_Elem(models.Model):
# #     type_of_choice = models.CharField(max_length=1, choices = LI_CHOICES, default = 'D')
# #     director = models.ForeignKey('Director',null=True, blank = True)
# #     film = models.ForeignKey('Film', null=True, blank = True)
# #     #title = models.ForeignKey('Director', models.SET_NULL, null = True)
# #     text = models.TextField()
# #     order = models.IntegerField()
#
# class List(models.Model):
#     title = models.CharField(max_length = 400)
#     intro = models.TextField()
#
#     def __str__(self):
#         return self.title
#
#
# class Film_List_Elem(models.Model):
#     film = models.ForeignKey('Film', on_delete=models.PROTECT)
#     text = models.TextField()
#     order = models.IntegerField()
#     owner_list = models.ForeignKey('List',  on_delete=models.PROTECT, null = True, blank = True, default = 1)
#
#     def __str__(self):
#         return self.film.title
#
# class Inbox(models.Model):
#     film = models.ForeignKey('Film', on_delete=models.PROTECT)
#
#     #published_date
#
#
# # class Movie()
# #     title
# #     director
#
