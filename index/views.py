# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.


def index(request):
    # return HttpResponseRedirect('vk/top/')
    return render(request, 'index/index.html')