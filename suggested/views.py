# -*- coding: utf-8 -*-
#
from django.shortcuts import render
from .models import *
from django.http import HttpResponse
import vk
from django.conf import settings

access_token = settings.VK_TOKEN

session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.75'

# Create your views here.

def get_suggested(request):
    print ("suggested")
    suggs = vk_api.wall.get(v=v, count=100, owner_id=-4569, offset=50, filter = 'suggests')
    # print (suggs)

    vkpost_fields = set(v.name for v in Suggested._meta.get_fields())
    video_fields = set(v.name for v in VideoSugg._meta.get_fields())

    # print (suggested_fields)

    for post in suggs['items']:
        try:
            atts = (post['attachments'])
        except KeyError:
            continue

        best18 = 'лучшее_что_я_видел_в_2018@drugoekino'
        data_clean = {k: v for k, v in post.items() if k in vkpost_fields}
        if best18 in data_clean['text']:
            data_clean['rating'] = 7

        sugg, created = Suggested.objects.update_or_create(post_id=post['id'], defaults=data_clean)

        for c, att in enumerate(atts):
            type = att['type']

            att_data = {'type': type, 'order': c, 'post_owner': sugg}

            if type == 'video':
                print (att['video'])

                # print (att)

                att = att['video']
                video_data_clean = {k: v for k, v in att.items() if k in video_fields}
                # video_data_clean.pop('owner_id')


                # # print (video_data_clean)
                #добавить проверку - есть ли видос уже в моих видео? если есть - то пусть просто отдельная процедура?
                #но я хочу сохранять порядок. А значит мне нужно куда-то его писать.
                try:
                    video_sugg, created = VideoSugg.objects.update_or_create(video_id=att['id'],
                                                                             sugg_post = sugg,
                                                                             defaults=video_data_clean)

                except:
                    pass





    # start = 200
    # limit = 1000
    # while start < limit:
    #     posts = vk_api.wall.get(v=v, count=100, owner_id=-4569, offset=start)

    return HttpResponse('')

def suggested(request):
    suggs_array = []
    suggs = Suggested.objects.filter(rating__gte = 6).order_by('date').order_by('-rating')
    for sugg in suggs:
        s = {}
        s['sugg']=sugg
        videos = VideoSugg.objects.filter(sugg_post = sugg)
        s['videos']=videos
        suggs_array.append(s)
    # print (videos)
    return render(request, 'suggested/suggested.html',{'suggs_array': suggs_array})

