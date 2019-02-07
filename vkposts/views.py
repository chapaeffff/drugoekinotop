from django.shortcuts import render

from django.shortcuts import render

from vkposts.models import VKPost

def vktop(request):

    till = request.GET.get("till", 0)
    vk_posts = VKPost.objects.filter(date__gte=till).order_by('-reposts').exclude(show_in_raw_rating = False) #exclude(widget__exact='').

    return render(request, 'vkposts/vktop.html',{'vk_posts':vk_posts})