# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from kinopoisk.movie import Movie

from blog.models import *
from video.models import *
from images.models import *

def film_detail(request, pk = '', slug = ''):
    if slug:
        film = get_object_or_404(Film, slug=slug)
    else:
        film = get_object_or_404(Film, pk=pk)
    # video = get_object_or_404(Video, film=film)

    try:
        videos = Video.objects.filter(film = film)
    except Video.DoesNotExist:
        videos = None

    try:
        shots = Shot.objects.filter(movie = film)
        print(shots)
    except Shot.DoesNotExist:
        videos = None


    try:
        from_lists = Film_List_Elem.objects.filter(film=film)
    except Film_List_Elem.DoesNotExist:
        from_lists = None

    reviews = Review.objects.filter(film=film)

    return render(request, 'filmbase/film_detail.html',
                  {'film': film, 'videos': videos,
                   'from_lists': from_lists, 'shots':shots, 'reviews':reviews})
    # return render(request, 'filmbase/film_detail.html', {'pk': pk})






def search(request):
    print('search')
    # # return render(request, 'index/index.html')
    # if 'q' in request.GET:
    #     query_string = request.GET['q']
    #     print (query_string)
    return render(request, 'filmbase/search.html')


def searching(request):
    if 'q' in request.GET:
        query_string = request.GET['q']
        # message = "You searched for: %r" % request.GET['q']
        movie_list = Movie.objects.search(query_string)
        m = movie_list[0]
        # print (vars(m))
        # f = Movie(id = m.id)
        #
        # print (vars(f))
        #
        message = m.title

        # google_kp(message)
        #
        # movie_list = Movie.objects.search('Redacted')
        # print(movie_list[0].id)

        # m = Movie(id=160977)
        # m.get_content('main_page')
        # print(m.title)  # вывод: Апокалипсис
        # print(m.directors)  # вывод: []

    else:
        message = "You submitted an empty form."
    return HttpResponse(message)

