# -*- coding: utf-8 -*-
#
from django.shortcuts import render
from vkposts.models import VKPost
from django.http import HttpResponse

from vkposts.models import VKPost, VKAtt, VideoAtt, PhotoAtt, Photo, ElseAtt
from video.models import Video
from filmbase.models import *


import vk
access_token = '9b778d9a0a4d6b24bdd3c3ae1cdf59185e9e163902090df400ef7d9eb288c19619cedc9f1fcef39f4a86d'

session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.75'
import time


def vkgrab(request):

    till = request.GET.get("till", 0)
    # posts = VKPost.objects.all()
    month_ago_ts = time.time() - 30*24*3600
    beg_time = (2019, 3, 1, 0, 0, 0, 0, 0, 0)
    end_time = (2019, 4, 1, 0, 0, 0, 0, 0, 0)
    beg_ts = time.mktime(beg_time)
    end_ts = time.mktime(end_time)
    print (month_ago_ts, beg_ts, end_ts)
    till = month_ago_ts #request.GET.get("till", 0)
    #vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts).order_by('-reposts').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    # vk_posts = VKPost.objects.all().order_by('-date').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts, reposts__gte = 45).order_by('-reposts')#.exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    len_base = len(vk_posts)
    #узнать кто я по acces token

    #этот блок выводит топ месяца в консоль
    # for post in vk_posts:
    #     text = post.text
    #     name = text[:text.find('\n')]
    #     print(name)
    #     # # print (post['reposts']['count'], name)
    #     print('http://vk.com/wall-' + '4569' + '_' + str(post.post_id))
    #     # print(post)
    #     atts = VideoAtt.objects.filter(post_owner = post, video__duration__gte = 3600)
    #     if (len(atts))<5:
    #         for att in atts:
    #             # print (att.video.title)
    #             print ('https://vk.com/video'+str(att.video.owner_id) + '_' + str(att.video.video_id))
    #
    #     print()


    return render(request, 'vkgrab/vkgrab.html',{'len': len_base, 'vk_posts':vk_posts})


# def vk_posts(request):
#     till = request.GET.get("till", 0)
#     #>1538841928
#     print (till)
#     vk_posts = VKPost.objects.filter(date__gte=till).order_by('-reposts') #exclude(widget__exact='').
#     print (vk_posts.count())
#     # for vk_post in vk_posts:
#     #     print (vk_post)
#     return render(request, 'blog/vk_posts.html', {'vk_posts': vk_posts})


def check_video(att):
    print (att)
    #на входе - видео из атта?
    #на выходе?
    video_fields = set(v.name for v in Video._meta.get_fields())
    video_data_clean = {k: v for k, v in att.items() if k in video_fields}
    video_data_clean.pop('id')

    # print (video_data_clean)

    video_instance, created = Video.objects.update_or_create(video_id=att['id'],
                                                          owner_id=att['owner_id'],
                                                          defaults=video_data_clean)
    return video_instance



def get_posts(request):
    print ("get posts")
    vkpost_fields = set(v.name for v in VKPost._meta.get_fields())
    start = 0
    limit = 50
    while start < limit:
        posts = vk_api.wall.get(v=v, count=100, owner_id=-4569, offset=start)
        time.sleep((0.33))
        start+=100
        print (start)
        # video_fields = set(v.name for v in Video._meta.get_fields())

        for post in posts['items']:
            try:
                atts = (post['attachments'])
            except KeyError:
                continue

            data_clean = {k: v for k, v in post.items() if k in vkpost_fields}
            data_clean['reposts'] = post['reposts']['count']

            if 'copy_history' in post:
                data_clean['copy'] = True
                print('copy')
            # print (VKPost.objects.filter(post_id = post['id']))
            # vkpost = VKPost(post_id=post['id'], **data_clean)
            # vkpost.save()pdate_or_create
            vkpost, created = VKPost.objects.update_or_create(post_id=post['id'], defaults=data_clean)
            # print ('updating')
            #1
            # print (atts)
            for c, att in enumerate(atts):
                type = att['type']

                att_data = {'type':type, 'order':c, 'post_owner':vkpost}

                if type == 'video':
                    # print(att)
                    # video_data_clean = {k: v for k, v in att['video'].items() if k in video_fields}
                    # video_data_clean.pop('id')
                    #
                    # video_instance, created = Video.objects.get_or_create(video_id =att['video']['id'],
                    #                                                        owner_id=att['video']['owner_id'],
                    #                                                        defaults=video_data_clean)
                    att_data['video']= check_video(att['video'])

                    video_att,created = VideoAtt.objects.get_or_create(**att_data)#(type=type, order=c,post_owner=vkpost)
                    # print (created, video_att)

                elif type == 'photo':
                    photo = att['photo']
                    # print (photo)
                    photo_instance, created = Photo.objects.get_or_create(photo_id=photo['id'], owner_id=photo['owner_id'],
                                           full_att=photo)


                    att_data['photo'] = photo_instance

                    photo_att, created = PhotoAtt.objects.get_or_create(**att_data)
                else:
                    att_data['att_text'] = att[type]
                    else_att, created = ElseAtt.objects.get_or_create(**att_data)


                #     # print (video_att)
                #     # video_att.video = video_instance
                #     # print (video_att.video)
                #     # video_att.save()
                #     att = video_att
                #
                #     # video_att, created = VideoAtt.objects.get_or_create(type=type, order=c,
                #     #                                             post_owner=vkpost,
                #     #                                             video=video_instance)
                #
                #     # print(video_att)
                # # a, created = VKAtt.objects.get_or_create(type=type, order=c,
                # #                                          post_owner=vkpost)
                # att.type = type
                # att.order = c
                # att.post_owner = vkpost
                # att.save()
                # # print(a)

    return HttpResponse('')



def get_videos(request):
    added = 0
    videos = vk_api.video.get(v=v, count=200, owner_id=-4569, offset=0)
    for video in videos['items']:

        if (check_video(video)):
            # print(video)
            added+=1
    print ('добавлено ', added)


    return HttpResponse('')


def next_post(request):
    top = VKPost.objects.all().order_by('-reposts')[20:30]
    for c, item in enumerate(top):
        print (c, ': ', item.text.splitlines()[0], item.reposts, '\n')

    return HttpResponse('')


from django.db.models import Count
from kinopoisk.movie import Movie

def test_func(request):

    #найти остров собак в базе фильмов:
    print ('-----------')
    search = 'Остров собак'
    films = Film.objects.filter(title__icontains = search)
    print (films)
    videos = Video.objects.filter(film = films[0])
    for v in videos:
        if v.duration > 3600:
            print('--Видео--', v.duration, v.owner_id, v)
            v_atts = VideoAtt.objects.filter(video=v)
            # print(v_atts)
            for v_att in v_atts:
                post = v_att.post_owner
                print(post.date, post.text[:50])
                print('===')
            # print('---===0000')

    #https: // vk.com / video - 4569_456243153

    #https: // vk.com / video - 4569_456243154


    # search = 'KИCЛOTA'
    # videos = Video.objects.filter(title__icontains=search)
    # print (videos)
    # for video in videos:
    #     print()
    #     print(video)
    # # posts = VKPost.objects.filter(text__icontains = search)
    # print (posts)

    # video1 = '-4569_456243148' #капернаум
    # video1 = '-4569_456243154'  # ахмед
    # video1 = '-4569_456243155'  # долгий день
    #
    # video = vk_api.video.get(videos = str(video1), v=v)
    # print (video)

    # movie_list = Movie.objects.search('Redacted')
    #
    # print( movie_list[0].id)
    # movie = Movie(id=257818)
    # print (movie.year)
    # print ('hey')
    # name = "Саакянц"
    #
    # # # name = "Алексей Балабанов"
    #
    # posts = VKPost.objects.filter(text__contains = name).order_by('-date')
    # print(len(posts))
    #
    # for post in posts:
    #     print (post)
    #     print ('-------------')


    # # title = "Война"
    # dir_base = Director.objects.filter(name = name)
    # for dir in dir_base:
    #     print(dir.kp_id)

    # dir_films = Film.objects.filter(director__name = name)
    # # print (dir_base)
    # # print(dir_films)
    #
    # dupes = Director.objects.values('name')\
    #     .annotate(Count('id'))\
    #     .order_by()\
    #     .filter(id__count__gt=1)
    #
    # fdupes = Film.objects.values('title')\
    #     .annotate(Count('id'))\
    #     .order_by()\
    #     .filter(id__count__gt=1)
    #
    #
    # # dupes2 = Director.objects.filter(name__in=[item['name'] for item in dupes])
    #
    # fdupes2 = Film.objects.filter(title__in=[item['title'] for item in fdupes])
    #
    # for fdupe in fdupes2:
    #     print(fdupe)
    #     # print (Film.objects.filter(director__name = dupe))


    # # print (dupes2)
    # for dupe in dupes2:
    #     print(dupe)
    #     print (Film.objects.filter(director__name = dupe))

    # dups = Director.objects.values('name')\
    #     .annotate(Count('id'))\
    #     .order_by()\
    #     .filter(id__count__gt=1)

    # top = VKPost.objects.all().order_by('-reposts')[20:30]
    # for c, item in enumerate(top):
    #     print (c, ': ', item.text.splitlines()[0], item.reposts, '\n')

    return HttpResponse('')

def get_hidden(request):
    hidden = Video.objects.filter(views__lte = 5000, duration__gte = 600,  owner_id = -4569).order_by('-views')

    for video in hidden:
    #     if not brand.cars_set.all().exists():
    # # delete
        if not video.videoatt_set.all().exists():
            print (video.title, video.views)


    # for video in hidden[5:20]:
    #     print ("Отобрано: ", video.title)
    #     posted = VideoAtt.objects.filter(video = video)
    #     print('Запощено: ', len(posted))
    #     for c, post in enumerate(posted):
    #         squad = (VideoAtt.objects.filter(post_owner = post.post_owner))
    #         print (c, ": в наборе видео, штук -", len(squad), ' позиция -', post.order )
    #     print ('----------')

    #есть ли пост ккоторому прилеплено видео?
    #если есть пост - есть видеоатт, к которому прилеплено.


    #     atts = VideoAtt.objects.filter(post_owner = post, video__duration__gte = 3600)
    #     if (len(atts))<5:
    #         for att in atts:
    #             # print (att.video.title)
    #             print ('https://vk.com/video'+str(att.video.owner_id) + '_' + str(att.video.video_id))
    #
    #     print()


    return HttpResponse('')


