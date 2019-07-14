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
    beg_time = (2019, 6, 1, 0, 0, 0, 0, 0, 0)
    end_time = (2019, 7, 1, 0, 0, 0, 0, 0, 0)
    beg_ts = time.mktime(beg_time)
    end_ts = time.mktime(end_time)
    print (month_ago_ts, beg_ts, end_ts)
    till = month_ago_ts #request.GET.get("till", 0)
    #vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts).order_by('-reposts').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    # vk_posts = VKPost.objects.all().order_by('-date').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts, reposts__gte = 45).order_by('-reposts')#.exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    len_base = len(vk_posts)
    #узнать кто я по acces token

    # #этот блок выводит топ месяца в консоль
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
                #понять какой фильм
                if (att.video.film):
                    print ('«'+att.video.film.title+'»', 'смотреть онлайн',
                           'drugoekino.top/film/'+att.video.film.slug +'/')
        #ссылка на сайт, для этого адо понять о каком фильме речь

        print

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

#функция для обзора концептов
def list_concepts (request):
    concepts = Concept.objects.all()
    # print(*concepts[:15], sep = "\n")
    for c in concepts[20:35]:
        if (c.film()):
            print (c.film())
            print (c.film().videos())
            # posts = VKPost.objects.filter()

    # test = input('Введите')
    # print (test)

    return HttpResponse('')


def get_posts(request, start = 0, limit = 100):
    print ("get posts")
    vkpost_fields = set(v.name for v in VKPost._meta.get_fields())
    start = int(start)
    limit = int (limit)
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
from filmscrap.views import search_kp_id, clean_kp_film,get_kp_data, google_kp

from django.utils import timezone


def update_kp(request):

    # апдейтим по одному с кинопоиска, актуально! может еще добавить динамику
    # альтернативные названия и т.п.
    for_updating = Film.objects.filter(year__gte = 2017, modified = None)
    for film in for_updating[:1]:
        # print  (film.__dict__)
        print (film.kp_id)
        print (film.title, film.year)
        print (film.votes)
        print (film.rating)

        kp_data = get_kp_data(film.kp_id)
        kp_data.pop('kp_id', None)
        kp_data.pop('id', None)
        kp_data['modified'] = timezone.now()
        # print(kp_data)
        # print('here kp data')

        Film.objects.filter(kp_id=film.kp_id).update(**kp_data)
        # m = Film.objects.get(kp_id=film.kp_id)
        #
        # for (key, value) in kp_data.items():
        #     setattr(m, key, value)
        #     print (m['key'])


        # upd_film = Film.objects.get(kp_id = m.kp_id)
        # upd_film = m
        # m.save()
        m = Film.objects.get(kp_id=film.kp_id)
        print (m.votes)
        print (m.rating)
        # print (m.__dict__)
        return HttpResponse('')

import json

def get_kp_id():
    kp_id = input('enter kp_id: ')
    kp_id = kp_id.strip()
    if kp_id.isdigit():
        return int(kp_id)
    else:
        print ('get_kp_id cant found this film')
        return None

def search_strings(f):
    print(f.title, f.director, f.year, f.rating, f.votes)
    search_strings = []
    str1 = f.title + ' ' + str(f.director)
    search_strings.append(str1)
    str2 = f.title + ' ' + str(f.year)
    search_strings.append(str2)
    str3 = f.title + ' ' + str(f.year + 1)
    search_strings.append(str3)
    str4 = f.title
    if len(str4) > 6:
        search_strings.append(str4)
    elif f.title_en:
        search_strings.append(f.title + ' ' + f.title_en)
    return search_strings


#эта пусть по kp_id ищет?ви
def find_new_long_2file(request):
    print ('find_new_long_2file')
    kp_id = (get_kp_id())
    film = Film.objects.get(kp_id = kp_id)
    print (search_strings(film))

    search_feeds = []
    search_feeds.append(film.id)
    for string in search_strings(film):
        search_feed = vk_api.newsfeed.search(v='5.75', q=string, count=200)
        sleep(0.33)
        search_feeds.append(search_feed['items'])

    with open('search_feeds.json', 'w', encoding='utf-8') as outfile:
        json.dump(search_feeds, outfile, ensure_ascii=False, indent=2)

    film.last_search = timezone.now()
    film.save()
    print(film.last_search)

    return HttpResponse('')

def delete_broken_video(request):
    video_link = input('enter full link to broken vk video:')
    first_div = (video_link.split('_'))
    video_id = first_div[1]
    second_div = first_div[0].split('video')
    owner_id = second_div[1]
    print (owner_id, video_id)

    deleted = Video.objects.filter(owner_id = owner_id, video_id = video_id).delete()
    print (deleted)

    return HttpResponse('')

from os import listdir, stat
from os.path import isfile, join, dirname, abspath
import requests
from pathlib import Path

def upload_2_private(request):
    print ('upload_2_private')
    group_id = 184015130
    new_settings = vk_api.groups.edit(v=v, group_id=group_id, video = 2) #вкл огр видео

    mypath = ('H:/3/upload_2_private/')
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    first_file = files[0]
    full_path = mypath + first_file
    size = stat(full_path).st_size
    est_loading = size/5000000
    print ('file size is: ', size)
    video_file = open(full_path, 'rb')
    print (video_file)
    #сделаем словарь
    for_upload = dict()
    for_upload['group_id'] = group_id
    for_upload['name'] = first_file
    for_upload['description'] = 'test desc'
    for_upload['v'] = v
    # print (for_upload)
    files = {'video_file': video_file}

    #
    upload_url = vk_api.video.save(**for_upload)['upload_url']
    #
    # print (upload_url)
    vid = upload_url[upload_url.find('&vid')+5:upload_url.find('&fid')]

    preload_video_adress = str(-group_id) + '_' + str(vid)
    preload_video = vk_api.video.get(v=v, videos = preload_video_adress)
    print('preload_video: ', preload_video)
    new_name = 'sdflsv32342j3'
    start_loading = time.time()
    print ('loading...')
    print ('прибл время загрузки ', est_loading)
    print(datetime.datetime.now())

    request = requests.post(upload_url, files=files)
    print('время загрузки ', time.time() - start_loading)
    renamed = vk_api.video.edit \
        (v=v, owner_id=str(-group_id), video_id=str(vid), name=new_name)

    #хочу получить данные этого видео
    vid = (request.json()['video_id'])

    print(files)
    video_file.close()
    loaded_video_adress = str(-group_id) + '_' + str(vid)

    loaded_video = vk_api.video.get(v=v, videos = loaded_video_adress)
    print('loaded_video: ', loaded_video)
    print ('***************')
    settings = vk_api.groups.getSettings(v = v, group_id = group_id)
    video_state = (settings['video'])
    print ('video_state было: ', video_state)
    sleep(0.33)
    if int(video_state) == 2:
        video_state = 0
    else:
        video_state = 2

    new_settings = vk_api.groups.edit(v=v, group_id=group_id, video = 0) #выкл видео

    # video_state = (new_settings['video'])

    # print('video_state стало: ',  video_state)

    #пока найдем только с расширением mp4

    return HttpResponse('')



#эту переделай чтобы джсон сохраняла в файл
def no_long_videos_feed2file(request):
    #найти НОВЫЕ фильмы С РЕЙТИНГОМ для которых нет видео
    month_ago = timezone.now()-datetime.timedelta(days=30)
    films = Film.objects.filter(year__gte = 2017,  rating__gte = 6.5)
    for_upd = films.filter(last_search__lte = month_ago)|films.filter(last_search = None)
    films = for_upd
    print (films)
    api_count = 0
    api_break = 1
    for f in films:
        print(api_count)
        if api_count>=api_break:
            break
        v = Video.objects.filter(film=f, duration__gte = f.runtime*60 - 60)
        print (v)

        if not v:

            # print (f.title, f.director, f.year, f.rating, f.votes)
            # search_strings = []
            # str1 = f.title + ' ' + str(f.director)
            # search_strings.append(str1)
            # str2 =  f.title + ' ' + str(f.year)
            # search_strings.append(str2)
            # str3 = f.title + ' ' + str(f.year+1)
            # search_strings.append(str3)
            # str4 = f.title
            # if len (str4)>6:
            #     search_strings.append(str4)
            # elif f.title_en:
            #     search_strings.append(f.title + ' ' + f.title_en)
            #


            api_count += 1

            search_feeds = []
            search_feeds.append (f.id)
            for string in search_strings(f):
                search_feed = vk_api.newsfeed.search(v='5.75', q=string, count=200)
                sleep(0.33)
                search_feeds.append(search_feed['items'])

            with open('search_feeds.json', 'w', encoding='utf-8') as outfile:
                json.dump(search_feeds, outfile, ensure_ascii=False, indent=2)

        print(f.last_search)
        f.last_search =  timezone.now()

        f.save()
        print(f.last_search)


    return HttpResponse('')


#а эта пусть из файла читает
def no_long_videos_get_from_file(request):
    with open('search_feeds.json', encoding="utf-8") as data_file:
        search_feeds = json.load(data_file,  encoding='utf-8')
        print (len(search_feeds))
    f = Film.objects.get(id = search_feeds[0])
    print (f)
    full_video_ids = [] #это будет список video_id, которые я уже добавил
    full_videos = []
    full_video_posts = []
    for search_feed in search_feeds[1:]:
        # print (search_feed)
        for s in search_feed:
            full_video = False

            videos_limit = 6
            videos_counter = 0
            try:
                atts= (s['attachments'])
                for att in atts:
                    if att['type'] ==  'video':
                        videos_counter +=1

                if videos_counter<videos_limit:
                    for att in atts:
                        if att['type'] == 'video':
                            video = att['video']
                            # print (video)
                            #считаем количество прикрепов виедо, елсли
                            # #отсечь дубли (достаточно если по номеру video
                            # if video['id'] in checked_video_ids:
                            #     pass
                            #
                            if (f.runtime*60 +150)> video['duration']>(f.runtime*60 -150):
                                full_video =  True
                                if video['id'] not in full_video_ids:
                                    full_video_ids.append(video['id'])
                                    full_videos.append(video)
                                    full_video_posts.append(s)
                                #таким образом я получил три списка, где все находится на одинаковых позициях

            # #тут у меня все видео по одному, и мне хорошо бы их проверить через вк_апи
            # #если отклика нет - то пропустим, а вот если есть - то выведем для ручной проверки

                            #эти видосы я хочу добавить в список
                            #и также хочу иметь и ссылки на посты



                            # full_video_fields = []
                            # full_video_fields.append(video['duration'])
                            # full_video_fields.append(video['title'])
                            #
                            # full_video_fields.append\
                            #     ('vk.com/video'+str(video['owner_id'])+ '_'+str(video['id']))



                            # full_video_fields = []
                            # full_video_fields.append(video['duration'])
                            # full_video_fields.append(video['title'])
                            #
                            # full_video_fields.append\
                            #     ('vk.com/video'+str(video['owner_id'])+ '_'+str(video['id']))

                #
                # if full_video:
                #     if videos_counter <videos_limit:
                #         for field in full_video_fields:
                #             print (field)
                #         print('vk.com/wall'+str(s['owner_id'])+ '_' + str(s['id']))
                #         # print (s)
                #         print('---------------------------')
                #         print('---------------------------')
            except:
                pass
    vk_video_ids = []
    for i, full_video in enumerate(full_videos):

        print(full_video['id'], full_video['title'][:200])
        if 'platform' in full_video:
            print (full_video['platform'])
        else:
            print ('no platform')
            vk_video_ids.append(str(full_video['owner_id']) + '_' + str(full_video['id']))

        print ('vk.com/video' + str(full_video['owner_id']) + '_' + str(full_video['id']))
        # print (full_video)
        post = full_video_posts[i]
        print('vk.com/wall'+str(post['owner_id'])+ '_' + str(post['id']))

        print ('------')
        pass

    vk_videos = vk_api.video.get(v=v, videos = vk_video_ids)['items']

    print('------')
    print('------')

    for vk_video in vk_videos:
        if vk_video:
            print('vk.com/video' + str(vk_video['owner_id']) + '_' + str(vk_video['id']))
            print (vk_video['title'][:200])
            if 'width' in  vk_video:
                print ('width', vk_video['width'])

        print ('***')



        # if not full_video:
        #     print ('no full videos in fieed')



    return HttpResponse('')


def concept_is_for_single_film(connection):
    concept_connections = ConnectionFilm.objects.filter(concept=connection.concept)
    if (len(concept_connections) == 1):
        return True
    else:
        return False

#проходит по новым видео, которых нет в аттачах в базе и сортирует их по рейтингу кп (но база не обновлялась)
def new_fulls(request):



    # фильмы для которых есть длинное видео, но которых нет в постах.
    # еще проще - длинное видео, которого нет в постах
    # #да концепты могут оперировать разными видео, но пока ведь мы не просто так добавляем новое длинное видео?
    new_full_videos = []
    videos = Video.objects.filter(duration__gte = 3600).order_by('-id')
    count = 0
    for v in videos:

        v_atts = VideoAtt.objects.filter(video = v)
        if not v_atts:
            # print (v.title, 'vk.com/video'+str(v.owner_id)+ '_'+ str(v.video_id))
            count +=1
            # print (v.film)
            if not v.film and v.kp_id:
                print (v.kp_id)
                film = Film.objects.filter(kp_id = v.kp_id)
                if film:
                    print (film)
                    v.film = film[0]
                    v.save()
            if v.film:
                full_videos = Video.objects.filter(duration__gte = 3600, film = v.film)
                # print(len(full_videos))
                # if (len(full_videos))>1:
                #     print ('MANYMANY!!!')
                # print (full_videos)
                new_full_videos.append(v.film)
                #получить связь
                connections = ConnectionFilm.objects.filter(film=v.film)
                # print (connections)
                #связь этого фильма с концептами, их может быть несколько
                for_single = False #из всех связей - фильм-концепт и фильм из списка - концепт, существует ли хоть одна связь фильм-концепт | если связей вообще нет - то стается False, иначе - если связь одна или больше, становится True если найден концепт, к  которому првязан ТОЛЬКО один этот фильм, иначе - остается False
                for c in connections:
                    if concept_is_for_single_film(c):
                        print (c.concept, '<- for single film')
                        for_single = True
                if not for_single: #нет 1фильм-концепт и мы его создадим
                    new_concept = Concept.objects.create()
                    new_film_conn = ConnectionFilm.objects.create(concept=new_concept, film=v.film)
                    #посты здесь не анализируются, если были посты - то они уже привязан, значит строка ниже не нужна
                    # new_vk = ConnectionVKPost.objects.create(concept=new_concept, post=post)
                    print(v.film, '<- это фильм из базы')

                    print('ПОДВЯЗАЛИ !фильм к концепту, проверь повторным запуском')
                    #потом этот концепт будет, но будут ли к нему подвязаны посты?
                    #если постов опознанных не было, то не будет
                    #но это возможно посты найдутся в таком случае - это надо проверить в posts2concept

                #есть ли альтернативный способ?



#где-то проверить - есть ли концепт для фильма
            # print ('-----')

        if count > 55:
            new_full_sorted = sorted(new_full_videos, key = lambda x: (x.rating is None, x.rating))
            for new_full in new_full_sorted:
                print (new_full.rating, new_full, new_full.director, new_full.year)
                videos = Video.objects.filter(film = new_full)
                for v in videos:
                    print (v. duration, 'vk.com/video' + str(v.owner_id) + '_' + str(v.video_id))
                print ('----------')
            # for s in sorted(concepts_ext.items(),
            #                 key=lambda k_v: k_v[1]['rating'], reverse=True)[7:9]:
            # print (new_full_videos[0].rating)
            print (new_full_sorted)

            #проверить - есть ли концепт для этого видео?

            break
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

def posts2concept(request):
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

        connectionsVK = ConnectionVKPost.objects.filter(post=post)
        if (len(connectionsVK) >0):
            print('пост подвязан, не надо ничего искать')
            print (post)
            pass

        else:

            first_line = post.text.split(sep ='\n')[0]

            till_slash = first_line.split(sep = '/')[0].strip()

            try:
                year = re.findall(r'\d+', first_line)[-1]
            except:
                year = 0

            #сначала надо выяснить - не подвязан ли уже этот пост (может вручную)
            #предположим пост может быть подвязан только к одному концепту?



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
                film_id = input('enter film id or (s)kip or (d)elete this post: ').strip()
                if film_id == 's':
                    pass
                elif film_id == 'd':
                    #delete post
                    #
                    posts = VKPost.objects.all().order_by('-id')  # objects.all()[:10]
                    VKPost.objects.filter(pk=post.pk).delete()


                else:
                    film = Film.objects.get(pk=int(film_id))
                    print ('есть такой фильм')
                    new_concept = Concept.objects.create()
                    # print ('concept created:', created)
                    new_film_conn = ConnectionFilm.objects.create(concept=new_concept, film=film)
                    # print('film_conn created:', created)
                    new_vk = ConnectionVKPost.objects.create(concept=new_concept, post=post)
                    # print('vk_conn created:', created)
                    print(first_line, '<- это из поста')
                    print(year)
                    print(film, '<- это фильм из базы')


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

    # тестируем тмдб
    #
    # m = tmdb.Movies(507076)
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

    return HttpResponse('')


def check_videos(request):
    print ('check_videos')

    #есть еще c film_id откуда-то


    videos = Video.objects.filter().order_by('-id')[0:100]
    print (videos)
    #где хранится инфа о том, что видео связано с фильмом?
    #если пост, в котором это видео связан с фильмом - значит и видео связано с фильмом?
    for v in videos:
        if v.film_id:
            film = Film.objects.get(pk = v.film_id)
            if not v.kp_id:
                v.kp_id = film.kp_id
                v.save()
        if v.kp_id:
            print (Film.objects.filter(kp_id = v.kp_id))
        else:
            kp_updated = False
            #ищем аттачи в которых это видео, а потом ищем соответствующие посты, потом концепты, потом фильм, связанный с концептом
            v_atts = VideoAtt.objects.filter(video = v)

            if v_atts:
                vk_posts = VKPost.objects.filter(id = v_atts[0].post_owner_id)
                #а пост у меня может быть привязан к концепту
                #если
                if vk_posts:
                    conn_vk = ConnectionVKPost.objects.filter(post_id = vk_posts[0].id)
                    # print (len(conn_vk))
                    if conn_vk:
                        print(v.title)
                        print(v_atts)

                        print('посты: ', vk_posts)
                        # concept = Concept.objects.filter(id = conn_vk[0].concept_id)
                        # print (concept)
                        conn_film = ConnectionFilm.objects.filter(concept_id = conn_vk[0].concept_id)

                        #можно обращаться через фильтры, но у меня вроде есть способ попроще прямой
                        #print(conn_film[0].film.kp_id)
                        v.kp_id = (conn_film[0].film.kp_id)
                        v.save()
                        kp_updated = True
                        # year = (connection.connectionfilm.film.year)
                        print('----------')
            if not kp_updated:
                #тут надо добавить процедурку по search_kp_id
                kp_id_auto = google_kp(v.title)
                # film = search_kp_id(kp_id)
                # print (film.title, film.year, film.director)

                kp_id = input('Press Enter if right, or enter kp_id manually or (s)kip: ', ).strip() or kp_id_auto
                if kp_id == 's':
                    pass
                else:
                    v.kp_id = (int(kp_id))
                    v.save()
                    kp_updated = True
                    #потом надо прогнать видосы у которых есть kpid но нет фильма




    return HttpResponse('')


def free_video2concepts  (request):
    #есть эта функция в new_fulls (дорабатывать

    return HttpResponse('')

def first_line(text):
    return str(text).split('\n')[0]


def ts_to_date(ts):

    return (datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

from math import sqrt
def calc_rating(request):
    print ('concepts_ratinig')

    published_ids = []

    for c in Concept.objects.all():
        if c.published():
            published_ids.append(c.id)

    published_concepts = Concept.objects.filter(id__in=published_ids)
    print(published_concepts)
    for pc in published_concepts:
        rating = 0
        last_post = pc.last_published()
        ts = (last_post.date)
        ts_now = time.time()
        days_ago = (int(((ts_now - ts)/(24*3600))))
        print (days_ago, 'дней с момента публикации')
        # print (ts_to_date(ts))
        print(first_line(pc.last_published()))
        print (last_post.reposts, 'репостов')
        reposts = last_post.reposts
        year = (pc.film().year)

        #получить год
#        year = (connection.connectionfilm.film.year)

        year_k = int(((year-1900)**2)/200)
        print (year, year_k)
        calc_rating = (days_ago%100 +  days_ago//100 + (reposts) + year_k)

        pc.calc_rating=calc_rating
        pc.save()


        print('---')
        #дата публикации последнего поста



    #
    # queryset = ConnectionVKPost.objects.filter(concept = )
    #
    # Concept.objects.annotate(published=Exists(queryset))....

    #сейчас я фильтрую вручную
    # concepts = Concept.objects.all()
    # concepts_published = []
    # for c in concepts:
    #     if ConnectionVKPost.objects.filter(concept=c):
    #         concepts_published.append(c)


    #
    # #а хотелось бы так:
    # concepts_published = Concept.objects.filter(published = True)
    # #где published вычисляется на основание другого queryset

    # print (len(concepts))


#    Foo.objects.order_by(F('A') - F('B'))

    return HttpResponse('')

# def new_films(request):


def concept_rating(request):
    print ('concept rating')
    print ('concept rating')

    print ('concept rating')


    # top_rating = Concept.objects.all().order_by('-calc_rating')
    # for t in top_rating[:10]:
    #     print (t, t.calc_rating)


    #!!! WEEK!!! что я готов повторить через неделю
    #- фильм не старше трех лет
    # new_films = Film.objects.filter(year__gte = 2016).values('id')
    # print (new_films)
    # conn_films = ConnectionFilm.objects.filter(film_id__in = new_films)
    # print (conn_films)

    # new_films = Film.objects.filter(year__gte = 2016)
    # print (new_films)
    conn_films = ConnectionFilm.objects.filter(film__in = Film.objects.filter(year__gte = 2016))
    # print (conn_films.values('concept'))
    for c_f in conn_films:
        concept = c_f.concept
        if ConnectionFilm.objects.filter(concept = concept).count()==1:
                posts = ConnectionVKPost.objects.filter(concept = concept)
                if posts.count()==1:
                    #при этом я хочу чтобы считало только полнометры
                    #если я прикрепляю и не фулл-видео
                    #тогда мне нужно каждый пост проверить на наличие фулл видео
                    # print ('********')
                    for post in posts:
                        # print (first_line(post))
                        full_video = False
                        video_atts = VideoAtt.objects.filter(post_owner = post.post)
                        for v in video_atts:
                            # print ('video_att', v)
                            try:

                                video = v.video
                                # print (video)
                                # if not (video.film):
                                #     sugg_kp_id = google_kp(video.title)
                                #     try:
                                #         film = Film.objects.get(kp_id = sugg_kp_id)
                                #         print('фильм', film)
                                #     except: print ('not found')
                                #
                                #     choice = input('(r)ight choice or enter manually?')
                                #     print (choice.strip())
                                #     if choice.strip() == 'r':
                                #         print (v.video.film)
                                #     else:
                                #         film = Film.objects.get(kp_id = int(choice.strip()))
                                #     v.video.film = film
                                #     video.save()
                                #     print('вот что записано ', video.film)

                                # print ('фильм', video.film)
                                d = (video.film.runtime)
                                # print ('duration',  d)
                                #
                                # print ('runtime', d)
                                # print ('v duration', video.duration)
                                if  video.duration > d*60*0.8:
                                    full_video = True

                            except: pass #print ('no video db')
                        if full_video:
                            pass
                            # print ('full video')
                        else:
                            pass
                            # print('-------')
                            #
                            # print(first_line(post))
                            # print ('not full')
                            # print ('runtime', d*60)
                            # print ('v duration', video.duration)

                            if not (video.film):
                                sugg_kp_id = google_kp(video.title)
                                try:
                                    film = Film.objects.get(kp_id = sugg_kp_id)
                                    print('фильм', film)
                                except: print ('not found')

                                choice = input('(r)ight choice or enter manually?')
                                print (choice.strip())
                                if choice.strip() == 'r':
                                    print (v.video.film)
                                else:
                                    film = Film.objects.get(kp_id = int(choice.strip()))
                                v.video.film = film
                                video.save()
                            #     print('вот что записано ', video.film)
                            #
                            #
                            # print (video_atts)

                        #
                    #для этого найти все аттс для этого поста
                    #в них найти видео
                    #если там есть видео похожее по длине на это дело
                    post = posts[0].post
                    if post.reposts>99:
                        print (post.reposts, first_line(post))
                        videos = Video.objects.filter(film = c_f.film )
                        # print (videos)
                        for v in videos:
                            print (v.duration, 'vk.com/video'+str(v.owner_id)+ '_'+ str(v.video_id))
                        print ('------')
                        # print (posts)


    #
    # new_films = Film.objects.filter(year__gte = 2016)
    # print (new_films)
    # conn_films = ConnectionFilm.objects.filter(film__in = new_films)
    # print (conn_films)


    #
    # new_and_only_films = []
    # for film in new_films:
    #     conn_film = ConnectionFilm.objects.filter(film=film)
    #     concept = conn_film[0].concept
    #     print (concept)


    # conn_films = ConnectionFilm.objects.filter(film = new_films)
    # print (conn_films)
    #- фильм набрал больше 100 репостов
    # - фильм имел только одну публикацию
    # - поищем такие фильмы




    return HttpResponse('')


#надо найти посты, которые не подвязаны

def not_linked(request):
    print ('not linked')
    posts = VKPost.objects.all().order_by('-id')
    # print (posts[:3])
    for post in posts[:3]:

        if not ConnectionVKPost.objects.filter(post = post):
            print ('not linked', post)

    return HttpResponse('')
