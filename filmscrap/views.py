from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from kinopoisk.movie import Movie

from blog.models import *
from video.models import *

from .forms import FilmForm, VideoForm


def search(request):
    print('search')
    return render(request, 'filmscrap/search.html')


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

        google_kp(message)
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

from bs4 import BeautifulSoup
import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

def google_kp(name):
    # name = name.replace('Trailer', '')
    # name = name.replace('Трейлер', '')
    # name = name.replace('трейлер', '')
    # name = name.replace('тизер', '')

    google_link =  'http://www.google.ru/search?q=' + name + ' kinopoisk'
    print(google_link)
    r = requests.get(google_link, headers = headers)
    soup = BeautifulSoup(r.text, "lxml")
    print (soup)
    kp_link = soup.find('div', {'class': 'r'}).a['href']
    print (kp_link)
    try:
        kp_id = (kp_link.split('film')[1].split('/')[1].split('-'))[-1]#[:-1])
    except:
        pass


    # i = 0
    # h3s = soup.findAll('h3', {'class': 'r'})
    # for h3 in h3s:
    #     link = h3.find('a')['href']
    #     if 'film' in link:
    #         print (link)
    #         beg_kp = max(link.rfind('-'), link[:-2].rfind('/'))
    #         print(beg_kp)
    #
    #         kp_id = link[beg_kp+1:-1]
    #         print(kp_id)
    #         break
    # print (not kp_id.isdigit())
    if not 'kp_id' in locals() or not kp_id.isdigit():
            kp_id = 0
    print(kp_id)

    return kp_id

def clean_kp_film(m):
    data = (vars(m))
    data = dict(data, kp_plot=data['plot'], kp_id = data['id'])
    fields = set(f.name for f in Film._meta.get_fields())
    data_clean = {k: v for k, v in data.items() if k in fields}
    return data_clean


def search_kp_id(kp_id):
    # film = Film()
    print ('here')
    print (kp_id)
    m = Movie(id=kp_id)
    print (m)
    print (m.title)
    m.get_content('main_page')
    print(m.directors)
    dir_name = m.directors[0]
    print (dir_name)
    dir_kp_id = m.directors[0].id
    print (m.directors)
    director, created = Director.objects.get_or_create(name = dir_name, kp_id = dir_kp_id)
    print (created)

    film = Film(director = director, **clean_kp_film(m))
    # print (film, created)
    # video_instance, created = Video.objects.update_or_create(video_id=att['id'],
    #                                                       owner_id=att['owner_id'],
    #                                                       defaults=video_data_clean)
    # d = check_or_create_director(dir_name,kp_id)
    # f = Film (director = d, **clean_kp_film(m))
    # f.save()
    return film


def film_new(request):
    form = FilmForm()
    if request.method == "POST":
        kp_id = request.POST['kp_id']
        title = request.POST['title']
        if '_search_kp_id' in request.POST:
            if kp_id is '':
                print ('no kpid')
                kp_id = google_kp(title)
            else:
                print (kp_id)
            check = Film.objects.filter(kp_id=kp_id)
            if len (check)>0:
                print (check)
            else:
                print ('no entry')
                search_kp_id(kp_id)
        #      return redirect('film_edit', pk=check.first().pk)

    return render(request, 'filmscrap/film_edit.html', {'form': form})


def filmscrap(request):
    #
    # till = request.GET.get("till", 0)
    # # posts = VKPost.objects.all()
    # month_ago_ts = time.time() - 30*24*3600
    # beg_time = (2019, 1, 1, 0, 0, 0, 0, 0, 0)
    # end_time = (2019, 2, 1, 0, 0, 0, 0, 0, 0)
    # beg_ts = time.mktime(beg_time)
    # end_ts = time.mktime(end_time)
    # print (month_ago_ts, beg_ts, end_ts)
    # till = month_ago_ts #request.GET.get("till", 0)
    # #vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts).order_by('-reposts').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    # # vk_posts = VKPost.objects.all().order_by('-date').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    # vk_posts = VKPost.objects.filter(date__gte=beg_ts, date__lte = end_ts, reposts__gte = 45).order_by('-reposts').exclude(show_in_raw_rating = False) #exclude(widget__exact='').
    # len_base = len(vk_posts)
    # #узнать кто я по acces token
    #
    # # for post in vk_posts:
    # #     text = post.text
    # #     name = text[:text.find('\n')]
    # #     print(name)
    # #     # # print (post['reposts']['count'], name)
    # #     print('http://vk.com/wall-' + '4569' + '_' + str(post.post_id))
    # #     # print(post)
    # #     atts = VideoAtt.objects.filter(post_owner = post, video__duration__gte = 3600)
    # #     if (len(atts))<5:
    # #         for att in atts:
    # #             # print (att.video.title)
    # #             print ('https://vk.com/video'+str(att.video.owner_id) + '_' + str(att.video.video_id))
    # #
    # #     print()


    return render(request, 'filmscrap/filmscrap.html') #,{'len': len_base, 'vk_posts':vk_posts})

import re
def clean_title(title):
    to_clean = ['трейлер', 'на русском', 'отрывок', '/', 'trailer', 'hd', '720p']
    title = title.lower()
    for word in to_clean:
        print (word)
        title = title.replace (word, '')
    return title
    #
    # def RemoveBannedWords(toPrint, database):
    #     statement = toPrint
    #     pattern = re.compile("\\b(Good|Bad|Ugly)\\W", re.I)
    #     return pattern.sub("", toPrint)
    #
    # toPrint = 'Hello Ugly Guy, Good To See You.'
    #
    # print
    # RemoveBannedWords(toPrint, bannedWord)


def video_dechaos(request):
    # added = 0

    if request.method == "POST":
        print ('post dechaos')
        if '_save' in request.POST:
            data = request.POST
            # v = form.save(commit=False)
            # data['film'] = request.film
            # video = Video.objects.filter(video_id = request.POST)
            video_id = (request.POST['video_id'])
            owner_id = (request.POST['owner_id'])
            video_instance = Video.objects.get(video_id = video_id,  owner_id = owner_id)

            form = VideoForm(request.POST, instance = video_instance)
            # print (form)
            # print (request.film.title)
            if form.is_valid():
                print (form['film'].value)
                form.save(commit=False)
                # v.film =
                form.save()
                return redirect('/scrap/video/dechaos')
        elif '_delete' in request.POST:
            data = request.POST
            # v = form.save(commit=False)
            # data['film'] = request.film
            # video = Video.objects.filter(video_id = request.POST)
            video_id = (request.POST['video_id'])
            owner_id = (request.POST['owner_id'])
            video_instance = Video.objects.get(video_id=video_id, owner_id=owner_id)
            video_instance.delete()
            return redirect('/scrap/video/dechaos')
        else: #отправляем на опознание
                # request.session['title'] = form.title
            title = request.POST['title']

            # clean_title = title.replace( '')  # 'murmurian'
            # print (title)
            request.session['title'] = clean_title(title)
            # film_new(request)
            # return render('/scrap/film/new', {'title': clean_title})

            return redirect('/scrap/film/new', title = clean_title)
            # film_new(request)

    else:
    # video = Video.objects.order_by('-date').first()
        video = Video.objects.filter(film__isnull = True).order_by('-date').first()
  # print (videos)
        kp_id = google_kp(clean_title(video.title))
        if int(kp_id) > 0:
            film = Film.objects.filter(kp_id=kp_id)
            if len (film)>0:
                film = film[0]
            else:
                film = search_kp_id(kp_id)
            video.film = film
            video.kp_id = kp_id

        form = VideoForm(instance =  video)


    # for video in videos['items']:
    #
    #     if (check_video(video)):
    #         # print(video)
    #         added+=1
    # print ('добавлено ', added)


    # return HttpResponse('')
    return render(request, 'filmscrap/video_dechaos.html', {'form': form})


def film_new(request):
    form = FilmForm(initial = {'title': request.session.get('title')})
    # form = FilmForm(title = title)
    # if request.method == "GET":
    #     fget = Film(title=request)
    # #     titleget = title
    # # # f = Film.objects.filter(pk=pk).first()
    # form = FilmForm(instance=fget)
    # form = FilmForm()
    # for field in (request.GET):
    #     print (field)
    # print (title)
    # print (request.method)
    if request.method == "POST":
        print (request.POST['title'])
        kp_id = request.POST['kp_id']
        title = request.POST['title']
        # form = FilmForm(initial={'title': title})
        if '_search_kp_id' in request.POST:
            if kp_id is '':
                print ('no kpid')
                kp_id = google_kp(title)
            else:
                print (kp_id)
            check = Film.objects.filter(kp_id=kp_id)
            if len (check)>0:
                print (check)
            else:
                print ('no entry')
                film = search_kp_id(kp_id)
                form = FilmForm(instance=film)
        elif '_save' in request.POST:
            form = FilmForm(request.POST)
            if form.is_valid():
                form.save()
        #      return redirect('film_edit', pk=check.first().pk)
    # elif request.method == "GET":
    #     title = title
    #     form = FilmForm(initial={'title': title})

    return render(request, 'filmscrap/film_edit.html', {'form': form})


def video_addbylink(request):
    print('adbylink')
    return render(request, 'filmscrap/video_addbylink.html')


# def video_link2form(request):
#     print ('link2forms')
#     return HttpResponse('')

def video_link2form(request):
    if 'q' in request.GET:
        link =  (request.GET['q'])
        parts = link.split('_')
        print (parts)
        owner_id = parts[0].split('video')[1]
        video_id = parts[1]
        print (owner_id, video_id)
        video = Video.objects.get(owner_id = owner_id, video_id = video_id)
        print (video)
        print (video.kp_id)
        if video:
            print ('video here')
        # print (videos)
        if not video.kp_id:
            print (' no kp_id')
            kp_id = google_kp(clean_title(video.title))
    #
        if int(kp_id) > 0:
            film = Film.objects.filter(kp_id=kp_id)
            if len(film) > 0:
                film = film[0]
            else:
                film = search_kp_id(kp_id)
            video.film = film
            video.kp_id = kp_id
    #
        form = VideoForm(instance=video)
    #
    #     # for video in videos['items']:
    #     #
    #     #     if (check_video(video)):
    #     #         # print(video)
    #     #         added+=1
    #     # print ('добавлено ', added)
    #
    #     # return HttpResponse('')
    return redirect(request, 'filmscrap/video_dechaos.html', {'form': form})

    #     query_string = request.GET['q']
    #     # message = "You searched for: %r" % request.GET['q']
    #     movie_list = Movie.objects.search(query_string)
    #     m = movie_list[0]
    #     # print (vars(m))
    #     # f = Movie(id = m.id)
    #     #
    #     # print (vars(f))
    #     #
    #     message = m.title
    #
    #     google_kp(message)
    #     #
    #     # movie_list = Movie.objects.search('Redacted')
    #     # print(movie_list[0].id)
    #
    #     # m = Movie(id=160977)
    #     # m.get_content('main_page')
    #     # print(m.title)  # вывод: Апокалипсис
    #     # print(m.directors)  # вывод: []
    #
    # else:
    #     message = "You submitted an empty form."
    # return HttpResponse('')


