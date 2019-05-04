# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponseRedirect

# Create your views here.


def index(request):
    return HttpResponseRedirect('vk/top/')
    # return render(request, 'blog/index.html')


def lists(request):
    lists = List.objects.all()
    return render(request, 'blog/lists.html', {'lists': lists})


def list(request, slug):
    type = request.GET.get('type', 'html')
    print (type)
    # # do processing

    print ('im here')
    cur_list = get_object_or_404(List, slug=slug)
    print (slug)
    print(cur_list)
    if cur_list.compact:
        type = 'compact'
    items = Film_List_Elem.objects.filter(owner_list=cur_list.pk).order_by('section')
    # items_all = Film_List_Elem.objects.all()
    prev_section = ''
    for item in items:
        if item.section:
            now_section = item.section.name
        else:
            now_section = ''
        #
        if prev_section != now_section: #now_section:
            print ('=', item.section)
            prev_section = now_section
        print (item)

    #надо сперва отсортировать по секциям
    sorted_by_section = {}
    sections = Section.objects.filter(owner = cur_list)
    for section in sections:
        print ('=',section)

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