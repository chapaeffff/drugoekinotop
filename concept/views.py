# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import *
from vkposts.models import *
import time
import re

from time import sleep

import vk
access_token = '9b778d9a0a4d6b24bdd3c3ae1cdf59185e9e163902090df400ef7d9eb288c19619cedc9f1fcef39f4a86d'

session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.75'

def index(request):
    # form = ImageForm()

    timestamp = int(time.time())            # мне надо придать вес
    three_month = 60*60*24*30*3
    three_month_ago= timestamp-three_month
    #
    # concept1 = Concept.objects.get(pk=13)
    # print (concept1)
    # connection = Connection.objects.filter(concept=concept1)
    # print(connection[0].connectionfilm) posts = VKPost.objects.all().order_by('-id')#objects.all()[:10]
    # limit = 350
    # count = 0
    # print ('---------------------------')

    posts = VKPost.objects.all().order_by('-id')#objects.all()[:10]
    print ('------------')
    count = 0
    years = 0
    for post in posts[:30]:

        first_line = post.text.split(sep ='\n')[0]
        # print(first_line[:200])
        try:
            year = int(re.findall(r'\d+', first_line)[-1])
        except:
            year = 0
            # print (year)
        if int(year) > 1890:
            print (first_line[:200])
            years+=year
            count +=1
            if count > 5:
                break
            print()
    avg_year = years/count
    print ('среднй год: ', years/count, 'из', count)
    mid_year = 2012
    delta =mid_year - avg_year #если среднее больше года-центра, то свежесть фильма будет минус-множителем
    if delta >=0:
        newbetter = False
    else:
        newbetter = True
    print (delta, newbetter)
        # till_slash = first_line.split(sep = '/')[0].strip()
        #
        # try:
        #     year = re.findall(r'\d+', first_line)[-1]
        # except:
        #     year = 0




    concepts = Concept.objects.all()
    concepts_ext = {}

    #чтобы учитывать предыдущие посты мне нужно как-то вывести коэф из них
    #для этого мне нужно учесть содержимое последних постов
    #для начала просто взять первые линии или 200 символов
    #первая линия была

    for concept in concepts:
        # print (concept)
        c = {}
        c['rating'] = 0
        connections = Connection.objects.filter(concept=concept)
        # print (connections)
        for connection in connections:
            #к каждому концепту я прикладываю словарь
            try:
                # print (connection.connectionfilm)
                year = (connection.connectionfilm.film.year)
                year_k = delta *(year-mid_year)
                c['rating'] += year_k
                # if newbetter:
                #     c['rating']+=delta
                # else:
                #     c['rating'] -= delta


            except:
                pass
            try:
                vk = (connection.connectionvkpost.post)
                # print (vk.date)
                if (vk.date>three_month_ago):
                    c['rating']*=0
                # print ('here date')
                # print (datetime.time)
                c['published'] = vk.date
            except:
                pass
            # print()
        c['rating']*=concept.k10
        concepts_ext[concept] = c
        # print(concepts_ext[concept]['rating'])
    for s in sorted(concepts_ext.items(),
                    key = lambda k_v: k_v[1]['rating'], reverse = True)[2:3]:
        # print (concepts_ext[s[0]], s[0])

        con_film = ConnectionFilm.objects.filter(concept= (s[0]))
        if len(con_film)==1:
            print(con_film)
            the_film = con_film[0].film
            videos = Video.objects.filter(film = the_film)
            # print (videos)
            fvids = []

            desc_new = 'страница фильма "' + the_film.title + ' (' \
                       + str(the_film.year) \
                       + '): drugoekino.top/film/' + str(the_film.id)

            for v in videos:
                if v.duration >36:
                    fvid = str(v.owner_id) + '_' + str(v.video_id)
                    print('vk.com/video' +fvid)
                    if v.owner_id == -4569:
                        fvids.append(fvid)
                        print (v.title)

                        # vk_api.video.edit(owner_id=-4569, video_id=v.video_id,
                        #                   desc = desc_new, v = v, name = v.title)
                        # sleep(0.33)

                        #
            # vkvideos = vk_api.video.get(v=v, videos = fvids)[1:]
            # print (vkvideos)
            # for video in vkvideos:
            #     print (video['title'], video['description'])


            # vk_api.video.edit(owner_id = -4569, video_id = )
            print (desc_new)
            print (fvids)
            print()


        # concepts_ext[concept] = connections
    # print (concepts_ext)
    # connections = Connection.objects.all()
    # for c in connections:
    #     print (c.strname)

    # print (connections.strname)

    return render(request, 'concept/index.html', {'concepts': concepts})
    # return render(request, 'vkgrab/vkgrab.html',{'len': len_base, 'vk_posts':vk_posts})

