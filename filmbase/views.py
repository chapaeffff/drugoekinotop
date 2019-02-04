from django.shortcuts import render, get_object_or_404, redirect


from blog.models import *
from video.models import *

def film_detail(request, pk):
    film = get_object_or_404(Film, pk=pk)
    # video = get_object_or_404(Video, film=film)

    try:
        videos = Video.objects.filter(film = film)
    except Video.DoesNotExist:
        videos = None

    try:
        from_lists = Film_List_Elem.objects.get(film=film)
    except Film_List_Elem.DoesNotExist:
        from_lists = None

    return render(request, 'filmbase/film_detail.html', {'film': film, 'videos': videos,
                                                     'from_lists': from_lists})
    # return render(request, 'filmbase/film_detail.html', {'pk': pk})