# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponseRedirect


# Create your views here.


def index(request):
    return HttpResponseRedirect('vk/top/')
    # return render(request, 'blog/index.html')


def lists(request):
    lists = List.objects.filter(publish='1')
    print (lists)
    return render(request, 'blog/lists.html', {'lists': lists})


def lists_adm(request):
    lists = List.objects.filter(publish=False)
    for list in lists:
        total = Film_List_Elem.objects.filter(owner_list = list).exclude(maybe = True).exclude(to_drop = True).count()
        list.total = total
        list.maybes = Film_List_Elem.objects.filter(owner_list = list, maybe = True ).count()
        list.to_drop = Film_List_Elem.objects.filter(owner_list = list, to_drop  = True).count()


    return render(request, 'blog/lists_adm.html', {'lists': lists})

import requests, json

def list(request, slug):
    print ('list')
    type = request.GET.get('type', 'html')
    print (type)
    # # do processing

    print ('im here')
    cur_list = get_object_or_404(List, slug=slug)
    # print (slug)
    # print(cur_list)
    if cur_list.compact:
        type = 'compact'
    items = Film_List_Elem.objects.filter(owner_list=cur_list.pk).order_by('section').exclude(maybe = True)
    # items_all = Film_List_Elem.objects.all()
    for item in items:
        item.put_link = False
        if (item.film.videos()):
            item.put_link = True
        if not item.put_link:

            week_ago = timezone.now() - datetime.timedelta(days=7)
            if not item.film.last_kodik_search:
                print ('not searched')
                item.film.last_kodik_search = timezone.now() - datetime.timedelta(days=14)
                item.film.save()
                print ('2weeks setted')
            if item.film.last_kodik_search < week_ago:

                print ('last search was earlier')
                print(item.film.last_kodik_search, week_ago)
                item.film.last_kodik_search = timezone.now()
                item.film.save()
                print(item.film.last_kodik_search)
                kodik_link = 'https://kodikapi.com/search?token=6c4f14a88c532aa24b15287e39ecb68c&kinopoisk_id=' \
                             + str(item.film.kp_id) + '&camrip=false'
                print (kodik_link)
                response = requests.get(kodik_link)
                data = json.loads(response.text)['results']
                if data:
                    item.put_link = True
                    print (data)
                    item.film.kodik = True
                    item.film.save()
            elif item.film.kodik == True:
                    item.put_link = True


        else:
            print('no film')

    prev_section = ''
    for item in items:
        if item.section:
            now_section = item.section.name
        else:
            now_section = ''
        #
        if prev_section != now_section: #now_section:
            # print ('=', item.section)
            prev_section = now_section

    sorted_by_section = {}
    sections = Section.objects.filter(owner = cur_list)
    for section in sections:
        # print ('=',section)

        section_items = items.filter(section = section)
        if len(section_items)>0:
            sorted_by_section[section] = section_items

    print (sorted_by_section)
        # for section_item in  (section_items):
        #     print (section_item)
    #   #тут уже собрались все итемы секции - их я занесу в дикт

    # for itema in items_all:
    #     try:
    #         print(itema.elem_image.image.url)
    #     except:
    #         itema.elem_image = None
    #         itema.save()

    if type == 'html':
        return render(request, 'blog/list.html', {'list': cur_list, 'items': items})
    elif type == 'zen':
        return render(request, 'blog/list_zen.html', {'list': cur_list, 'items': items})
    elif type == 'compact':
        return render(request, 'blog/list_compact.html', {'list': cur_list, 'items': items, 'sorted_by_section': sorted_by_section})


def list_adm(request, slug):
    print ('list')
    type = request.GET.get('type', 'html')
    print (type)
    # # do processing

    print ('im here')
    cur_list = get_object_or_404(List, slug=slug)
    # print (slug)
    # print(cur_list)
    if cur_list.compact:
        type = 'compact'
    items = Film_List_Elem.objects.filter(owner_list=cur_list.pk).order_by('section').exclude(maybe = True).exclude(to_drop = True)
    # items_all = Film_List_Elem.objects.all()
    for item in items:
        if (item.film.videos()):
            item.put_link = True
    prev_section = ''
    for item in items:
        if item.section:
            now_section = item.section.name
        else:
            now_section = ''
        #
        if prev_section != now_section: #now_section:
            # print ('=', item.section)
            prev_section = now_section

    sorted_by_section = {}
    sections = Section.objects.filter(owner = cur_list)
    for section in sections:
        # print ('=',section)

        section_items = items.filter(section = section)
        if len(section_items)>0:
            sorted_by_section[section] = section_items

    print (sorted_by_section)
        # for section_item in  (section_items):
        #     print (section_item)
    #   #тут уже собрались все итемы секции - их я занесу в дикт

    # for itema in items_all:
    #     try:
    #         print(itema.elem_image.image.url)
    #     except:
    #         itema.elem_image = None
    #         itema.save()

    if type == 'html':
        return render(request, 'blog/list_adm.html', {'list': cur_list, 'items': items})
    # elif type == 'zen':
    #     return render(request, 'blog/list_zen.html', {'list': cur_list, 'items': items})
    # elif type == 'compact':
    #     return render(request, 'blog/list_compact.html', {'list': cur_list, 'items': items, 'sorted_by_section': sorted_by_section})



# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post
# from .forms import PostForm
#
# from django.shortcuts import render
# from django.utils import timezone
# from .models import * #Post, Director, List_Elem, Film_List_Elem
#
# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})
#
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
#
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})
#
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})
#
# #def post_dir(request, pk)
#
# def directors_list(request):
#     directors = Director.objects.all()
#     return render(request, 'blog/directors.html', {'directors':directors})
#
# def director_detail(request, pk):
#     director = get_object_or_404(Director, pk=pk)
#     return render(request, 'blog/director_detail.html', {'director': director})
#
# def film_detail(request, pk):
#     film = get_object_or_404(Film, pk=pk)
#     video = get_object_or_404(Video, film=film)
#     return render(request, 'blog/film_detail.html', {'film': film, 'video': video})
#
# def items_list(request):
#     items = List_Elem.objects.all()
#     return render(request, 'blog/items.html', {'items':items})
#
# def film_items_list(request):
#     items = Film_List_Elem.objects.all()
#     return render(request, 'blog/film_items.html', {'items':items})
#
# def list(request, pk):
#     cur_list = get_object_or_404(List, pk=pk)
#     items = Film_List_Elem.objects.filter(owner_list = pk)
#     return render(request, 'blog/list.html', {'list': cur_list, 'items':items})