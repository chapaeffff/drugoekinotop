# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from .models import Video
from .forms import VKVideoLinkForm
from filmscrap.forms import VideoForm
from filmscrap.views import clean_title

# Create your views here.

#как-то помаленьку но массово закоплять видео
#а) прогнал название видео через гугл_кп
#б) да все как для одного, проверил наличие,


def video(request):
    videos = Video.objects.all()
    vi_fi = Video.objects.filter(film__isnull = False)

     # vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts, reposts__gte = 45).order_by('-reposts').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    v_len = len(videos)
    vi_fi = len(vi_fi)
    #узнать кто я по acces token

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


    return render(request, 'video/video.html',{'len': v_len, 'vi_fi':vi_fi})#, 'vk_posts':vk_posts})

def get_vk_video_link(request):
    form = VKVideoLinkForm()
    if request.method=='POST':
        # print (' got it')
        link = (request.POST.get('link'))
        parts = link.split('_')
        print(parts)
        owner_id = parts[0].split('video')[1]
        video_id = parts[1]
        print(owner_id, video_id)
        # video = Video.objects.get(owner_id=owner_id, video_id=video_id)
        # admin = 'http://127.0.0.1:8000/admin/video/video/'+str(video.id)+'/change/'
        # print (admin)
        # print(video)
        # print(video.kp_id)
        # if video:
        #     print('video here')
        # # print (videos)
        # if not video.kp_id:
        #     print(' no kp_id')
        # form = VideoForm(instance = video)

        # clean_title = title.replace( '')  # 'murmurian'
        # print (title)
        request.session['owner_id'] = owner_id
        request.session['video_id'] = video_id

        return redirect('/video/edit')

        # return render('/scrap/video/dechaos', {'form': form})
            # return redirect(request, 'filmscrap/video_dechaos.html', {'form': form})

        # cd = form.cleaned_data
        # link = cd.get('link')
        # print (link)
        # form = MyForm(request.POST)
        # if form.is_valid():
        #     cd = form.cleaned_data
        #     #now in the object cd, you have the form as a dictionary.
        #     a = cd.get('a')
    return render(request, 'video/get_vk_link.html', {'form': form})#, 'vk_posts':vk_posts})

from vkgrab.views import check_video

import vk
access_token = '9b778d9a0a4d6b24bdd3c3ae1cdf59185e9e163902090df400ef7d9eb288c19619cedc9f1fcef39f4a86d'

session = vk.Session(access_token=access_token)
vk_api = vk.API(session)
v = '5.75'
import time

# att_data['video'] = check_video(att['video'])


def video_edit(request):
    if request.method == "POST":
        if '_save' in request.POST:
            video_id = (request.POST['video_id'])
            owner_id = (request.POST['owner_id'])
            video_instance = Video.objects.get(video_id = video_id,  owner_id = owner_id)

            form = VideoForm(request.POST, instance = video_instance)
            if form.is_valid():
                form.save(commit=False)
                form.save()
                # return redirect('/scrap/video/dechaos')
        elif '_delete' in request.POST:
            video_id = (request.POST['video_id'])
            owner_id = (request.POST['owner_id'])
            video_instance = Video.objects.get(video_id=video_id, owner_id=owner_id)
            video_instance.delete()
            return redirect('/scrap/video/dechaos')
        else: #отправляем на опознание
            title = request.POST['title']
            request.session['title'] = clean_title(title)
            return redirect('/scrap/film/new', title = clean_title)

    else:
        owner_id = request.session.get('owner_id')
        video_id = request.session.get('video_id')
        vk_video = vk_api.video.get(videos = str(owner_id)+'_'+str(video_id), v = v)['items'][0]
        # print (vk_video['items'][0])
        video =  check_video(vk_video)
        print (video)#Video.objects.get(owner_id=owner_id, video_id=video_id)
        form = VideoForm(instance = video)
    return render(request, 'filmscrap/video_dechaos.html', {'form': form})


