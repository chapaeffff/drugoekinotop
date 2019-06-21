# -*- coding: utf-8 -*-
#
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from vkposts.models import VKPost
from django.http import HttpResponse

from vkposts.models import VKPost, VKAtt, VideoAtt, PhotoAtt, Photo, ElseAtt
from video.models import Video
from filmbase.models import *
from concept.models import *
from blog.models import *



import vk
from django.conf import settings

access_token = settings.VK_TOKEN

session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.75'
import time


def vkgrab(request):

    till = request.GET.get("till", 0)
    # posts = VKPost.objects.all()
    month_ago_ts = time.time() - 30*24*3600
    beg_time = (2019, 5, 1, 0, 0, 0, 0, 0, 0)
    end_time = (2019, 6, 1, 0, 0, 0, 0, 0, 0)
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
    for post in vk_posts:
        text = post.text
        name = text[:text.find('\n')]
        print(name)
        # # print (post['reposts']['count'], name)
        print('http://vk.com/wall-' + '4569' + '_' + str(post.post_id))
        # print(post)
        atts = VideoAtt.objects.filter(post_owner = post, video__duration__gte = 3600)
        if (len(atts))<5:
            for att in atts:
                # print (att.video.title)
                print ('https://vk.com/video'+str(att.video.owner_id) + '_' + str(att.video.video_id))

        print()


    return render(request, 'vkgrab/vkgrab.html',{'len': len_base, 'vk_posts':vk_posts})


def vk_posts(request):
    till = request.GET.get("till", 0)
    #>1538841928
    print (till)
    vk_posts = VKPost.objects.filter(date__gte=till).order_by('-reposts') #exclude(widget__exact='').
    print (vk_posts.count())
    # for vk_post in vk_posts:
    #     print (vk_post)
    return render(request, 'blog/vk_posts.html', {'vk_posts': vk_posts})


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
    start = 5600
    limit = 9600
    count = min (limit, 100)
    while start < limit:
        posts = vk_api.wall.get(v=v, count=count, owner_id=-4569, offset=start)
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

            check = VKPost.objects.filter(post_id = post['id'])

            vkpost, created = VKPost.objects.update_or_create(post_id=post['id'], defaults=data_clean)
            if created:
                print ('создан новый')
            else:
                print ('обновляем')

            #если новый - то создается, если старый - то апдейт. А
            #а если в базе есть, а на стене нет?
            #и если в базе нет - а на стене есть - то он добавится снова, даже удаленный. т.е. либо надо метку
            #не добавляйся, либо удалять вслед за стеной - это проще?

            #беру 100 постов записанных.
            #беру 100 постов
            #надо обозначить границы
            #айди первого поста
            #айди последнего поста


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


    #учитываем закреп - берем пост со второго

    #начало - найти пост с макс айди, который есть в обеих
    #конец - найти пост с мин айд, которые есть в обеих выборках

    print ('---------------------')
    count = 100
    posts = vk_api.wall.get(v=v, count=count, owner_id=-4569, offset=1)

    for newest, post in enumerate(posts['items']):
        if VKPost.objects.filter(id = post['id']):
            print ('первое совпадение: ', post['id'], post['text'][:100])
            newest = post['id']
            break

    for oldest, post in enumerate(reversed(posts['items'])):
        if VKPost.objects.filter(id = post['id']):
            print ('последнее совпадение: ', post['id'], post['text'][:100])
            oldest = post['id']
            break

    # for post in posts['items'][newest: oldest]:
    #     if not VKPost.objects.filter(id = post['id']):
    #         print ('нЕ НАЙДЕНО: ', post['id'], post['text'][:100])

    #наоборот надо
    dbposts = VKPost.objects.filter(id__lte = newest, id__gte = oldest).order_by('-id')
    # print(dbposts[0].id, dbposts[0].text[:100])
    # print('-')
    # print(dbposts.last().id, dbposts.last().text[:100])
    print()
    for dbpost in dbposts:
        finded = False
        for post in posts['items']:
            if post['id'] == dbpost.id:
                #совпадение найдено
                finded = True
            if finded:
                continue
        if not finded:
            print('нет совпадения: ', dbpost.id,  dbpost.text[:50])
            dbpost.delete()

        #если айди этого поста нет в свежей выдаче.
        #как проверить: пошагово сравнить? id и з

    #
    # p
    #
    #
    #
    # print('-')
    # print('-')
    # print(posts['items'][0]['id'], posts['items'][0]['text'][:100])
    # print('-')
    # print(posts['items'][98]['id'], posts['items'][98]['text'][:100])
    #
    # print('-------')
    # dbposts = VKPost.objects.all().order_by('-id')[:100]
    # print(dbposts[0].id, dbposts[0].text[:100])
    # print('-')
    # print(dbposts[96].id, dbposts[96].text[:100])

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


# import tmdbsimple as tmdb
# tmdb.API_KEY = 'aef80e218767375116820b75d9dddf69'

from time import sleep
from filmscrap.views import search_kp_id, clean_kp_film,get_kp_data

from django.utils import timezone




def next_post(request):

    #апдейтим по одному с кинопоиска, актуально! может еще добавить динамику
    #альтернативные названия и т.п.
    # for_updating = Film.objects.filter(year__gte = 2017, modified = None)
    # for film in for_updating[:1]:
    #     # print  (film.__dict__)
    #     print (film.kp_id)
    #     print (film.title, film.year)
    #     print (film.votes)
    #     print (film.rating)
    #
    #     kp_data = get_kp_data(film.kp_id)
    #     kp_data.pop('kp_id', None)
    #     kp_data.pop('id', None)
    #     kp_data['modified'] = timezone.now()
    #     # print(kp_data)
    #     # print('here kp data')
    #
    #     Film.objects.filter(kp_id=film.kp_id).update(**kp_data)
    #     # m = Film.objects.get(kp_id=film.kp_id)
    #     #
    #     # for (key, value) in kp_data.items():
    #     #     setattr(m, key, value)
    #     #     print (m['key'])
    #
    #
    #     # upd_film = Film.objects.get(kp_id = m.kp_id)
    #     # upd_film = m
    #     # m.save()
    #     m = Film.objects.get(kp_id=film.kp_id)
    #     print (m.votes)
    #     print (m.rating)
    #     # print (m.__dict__)


    #тестируем тмдб
    #
    # m = tmdb.Movies(507076)
    # response = m.info( language = 'ru')
    # d = m.__dict__
    # # print (d)
    # # print (m.alternative_titles())
    # # print (m.release_dates())
    # releases = (m.release_dates()['results'])
    # print()
    # # print (releases)
    # for r in releases:
    #     if r['iso_3166_1'] == 'RU':
    #         print (r)
    # for r in releases:
    #     print (r)
    # q = 'Экстаз'
    #
    # search = tmdb.Search()
    # response = search.movie(query=q)
    # for s in search.results[:1]:
    #     print(s['title'], s['id'], s['release_date'], s['popularity'])
    #     print (s)






    # top = VKPost.objects.all().order_by('-reposts')[20:30]
    # for c, item in enumerate(top):
    #     print (c, ': ', item.text.splitlines()[0], item.reposts, '\n')

    # concepts = Concept.objects.all()[:10]
    # for concept in concepts:
    #
    # postpone = vk_api.wall.get(v=v, count=10, owner_id=-4569, filter = 'postponed')
    # print (postpone)
    # post = vk_api.wall.get(v=v, count=1, owner_id=-4569, offset = 1)
    # print (post)

    # films = Film.objects.all()
    # for film in films:
    #     print (film.slug)
    #     film.save()
    #     print (film.slug)
    # q = "Дама пик"
    # films = Film.objects.filter(title__contains=q)
    # # print (film)
    # for film in films:
    #     film.save()
    #     print ('film/'+film.slug)
    #     videos = Video.objects.filter(film = film)
    #     # print (str(videos))
    #     for v in videos:
    #         print (v)
    #         print ('vk.com/video' + str (v.owner_id)+ '_' + str(v.video_id))

    #найти НОВЫЕ фильмы С РЕЙТИНГОМ для которых нет видео
    # month_ago = timezone.now()-datetime.timedelta(days=30)
    # films = Film.objects.filter(year__gte = 2017,  rating__gte = 6.5)
    # for_upd = films.filter(last_search__lte = month_ago)|films.filter(last_search = None)
    # films = for_upd
    # print (films)
    # api_count = 0
    # api_break = 1
    # for f in films:
    #     if api_count>=api_break:
    #         break
    #     v = Video.objects.filter(film=f, duration__gte = 600)
    #
    #     if not v:
    #         print (f.title, f.director, f.year, f.rating, f.votes)
    #         str1 = f.title + ' ' + str(f.director)
    #         str2 =  f.title + ' ' + str(f.year)
    #         str3 = f.title + ' ' + str(f.year+1)
    #         str4 = f.title
    #         #здесь выбираем поиск строку
    #         q = str1
    #         print ('q', q)
    #
    #         # search = vk_api.video.search( v = '5.75', q = f.title + ' ' + str(f.director), longer = 3600) # + str(f.year)
    #         print('---------------------------------')
    #         search_feed = vk_api.newsfeed.search(v= '5.75', q = q, count = 200)
    #         api_count +=1
    #         # sleep(0.33)
    #
    #         for s in search_feed['items']:
    #             full_video = False
    #             try:
    #                 atts= (s['attachments'])
    #                 for att in atts:
    #                     if att['type'] ==  'video':
    #                         video = att['video']
    #                         if (video['duration'])>(f.runtime*60 -450):
    #                             full_video =  True
    #                             print (video['duration'])
    #                             print(video['title'])
    #
    #                             print('vk.com/video'+str(video['owner_id'])+ '_'+str(video['id']))
    #                             print(video)
    #                             print()
    #                 if full_video:
    #                     print('vk.com/wall'+str(s['owner_id'])+ '_' + str(s['id']))
    #                     # print (s)
    #                     print('---------------------------')
    #                     print('---------------------------')
    #             except:
    #                 pass
    #         print(f.last_search)
    #         f.last_search =  timezone.now()
    #
    #         f.save()
    #         print(f.last_search)

    # фильмы для которых есть длинное видео, но которых нет в постах.
    # еще проще - длинное видео, которого нет в постах
    # #да концепты могут оперировать разными видео, но пока ведь мы не просто так добавляем новое длинное видео?
    new_full_videos = []
    videos = Video.objects.filter(duration__gte = 3600).order_by('-id')
    count = 0
    for v in videos:
        if count > 15:
            new_full_sorted = sorted(new_full_videos, key = lambda x: x.rating)
            for new_full in new_full_sorted:
                print (new_full.rating, new_full, new_full.director, new_full.year)
            # for s in sorted(concepts_ext.items(),
            #                 key=lambda k_v: k_v[1]['rating'], reverse=True)[7:9]:
            # print (new_full_videos[0].rating)
            print (new_full_sorted)

            break
        v_atts = VideoAtt.objects.filter(video = v)
        if not v_atts:
            # print (v.title, 'vk.com/video'+str(v.owner_id)+ '_'+ str(v.video_id))
            count +=1
            # print (v.film)
            if v.film:
                full_videos = Video.objects.filter(duration__gte = 3600, film = v.film)
                # print(len(full_videos))
                # if (len(full_videos))>1:
                #     print ('MANYMANY!!!')
                # print (full_videos)
                new_full_videos.append(v.film)
            # print ('-----')

    #тут я нашел список длинных видео, не прикрепленных к постам
    #а теперь хорошо бы проверить - есть ли посты, с другим видео на этот же фильм
    #1) надо определить фильм

    #
    #
    #     # films = Film.objects.all()
    #     # for f in films:
    #     #     ConnectionVKPost



    return HttpResponse('')


from django.db.models import Count
from kinopoisk.movie import Movie

import re

from django.db.models import Q

def test_func(request):
    print ()
    # fles = Film_List_Elem.objects.all().order_by('-id')
    # for fle in fles[:1]:
    #     value = fle.text
    #     value.replace("\"", "\"")
    #     value.replace("«", "\"")
    #     value.replace("»", "\"")
    #     value.replace("<<", "\"")
    #     value.replace(">>", "\"")
    #     fle.text = value
    #     print (fle.text)

    # films = Film.objects.all().order_by('-id')[:10]
    # for film in films:
    #     print (film)
    #     film.save()
    # concepts = Concept.objects.all()
    # for con in concepts:
    #     connections = ConnectionFilm.objects.filter(concept = con)
    #     if len(connections) == 0:
    #         print ('сирота: ', con)
    # for c in connections:
    #     concept_connections=\
    #     ConnectionFilm.objects.filter(concept = c.concept)



    ##################
    posts = VKPost.objects.all().order_by('-id')#objects.all()[:10]
    limit = 8500
    count = 0
    orphan_count = 0
    print ('---------------------------')
    for post in posts:

        first_line = post.text.split(sep ='\n')[0]

        till_slash = first_line.split(sep = '/')[0].strip()

        try:
            year = re.findall(r'\d+', first_line)[-1]
        except:
            year = 0


        film = Film.objects.filter(title = till_slash, year__gte = int(year)-1, year__lte = int(year)+1)
        # try:
        #     if film[0].title == "Дама пик":
        #         print('dama pik film')
        # except:
        #     pass


        if film:
            # print(first_line, '<- это из поста')
            # print (year)
            # print(film[0], '<- это фильм из базы')
            connections = ConnectionFilm.objects.filter(film=film[0])
            # for c in connections:
            #     print (c)
            if connections:
                # print ('есть связи фильм-концепт')
                for c in connections:
                        concept_connections=\
                            ConnectionFilm.objects.filter(concept = c.concept)
                        if (len(concept_connections) == 1):

                            # print(c.concept, '<-это концепт')

                            connectionsVK = ConnectionVKPost.objects.filter(post = post)
                            if (len(connectionsVK) ==1 ):
                                # print('пост подвязан')
                                pass

                            else:
                                print ('пост не подвязан')
                                # значит надо подвязать?
                                new_vk = ConnectionVKPost.objects.create(concept = c.concept, post = post)
                                print(first_line, '<- это из поста')
                                print (year)
                                print(film[0], '<- это фильм из базы')

                                print ('ПОДВЯЗАЛИ, проверь повторным запуском')
                        else:
                            print((len(concept_connections)))
                            print(first_line)
                            print ('нет фильма-концепта (но есть какой-то другой?)')
            else:
                print (('НЕТ связи фильм-концепт'))
                #но если фильм-концепты не создаются без предв создания связи,
                #то значит нет и самого концепта
                #значит надо создать концепт и связь!
                #для этого сперва делаем концепт
                #а потом - связь
                #ну заодно и подвязать пост? ну пусть в 2 этапа сначла
                new_concept = Concept.objects.create()
                new_film_conn = ConnectionFilm.objects.create(concept = new_concept, film = film[0])
                new_vk = ConnectionVKPost.objects.create(concept=new_concept, post=post)
                print(first_line, '<- это из поста')
                print(year)
                print(film[0], '<- это фильм из базы')

                print('ПОДВЯЗАЛИ, проверь повторным запуском')
            # print()
            count += 1
        elif int(year)> 1900 and int(year)<2020:
            print(till_slash)
            print (year)
            orphan_count+=1
            # return reverse('filmscrap:film_new')
            # return redirect('/scrap/film/new', title = till_slash + year)
            if orphan_count >15:
                break


        if count > limit:
            break
    ######################
    # for post in posts[]:
    #      print(post[:50])

    #найти остров собак в базе фильмов:
    # print ('-----------')
    # search = 'Остров собак'
    # films = Film.objects.filter(title__icontains = search)
    # print (films)
    # videos = Video.objects.filter(film = films[0])
    # for v in videos:
    #     if v.duration > 3600:
    #         print('--Видео--', v.duration, v.owner_id, v)
    #         v_atts = VideoAtt.objects.filter(video=v)
    #         # print(v_atts)
    #         for v_att in v_atts:
    #             post = v_att.post_owner
    #             print(post.date, post.text[:50])
    #             print('===')
    #         # print('---===0000')

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


def test_func2(request):
    vk_posts = vk_api.wall.get(v=v, owner_id=-4569, filter = "owner")

    print ('test func 2')
    print ('записей на стене', vk_posts['count'])

    db_posts = VKPost.objects.filter()
    print ((len(db_posts)))
    date = datetime.datetime.fromtimestamp(db_posts.first().date)
    print (date)

    posts = VKPost.objects.all().order_by('-id')#objects.all()[:10]

    print ('---------------------------')
    count = 0
    print('примеры')
    for post in posts:

        first_line = post.text.split(sep ='\n')[0]

        till_slash = first_line.split(sep = '/')[0].strip()

        try:
            year = re.findall(r'\d+', first_line)[-1]
        except:
            year = 0

        #простейшая проверка что похоже на пост фильм
        if len(till_slash) > 3 and int(year) > 1900:
            count +=1

        if count%1000 == 0:
            print (first_line)

    print ('постов типа фильмп-пост',  count)


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



