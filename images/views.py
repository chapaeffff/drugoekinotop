# -*- coding: utf-8 -*-

from django.shortcuts import render


# Create your views here.
from .forms import ImageForm

def image_new(request):
    form = ImageForm()
    return render(request, 'images/image_new.html', {'form': form})