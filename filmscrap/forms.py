from django import forms

from filmbase.models import Film
from video.models import Video

class FilmForm(forms.ModelForm):

    class Meta:
        model = Film
        # fields = '__all__'
        exclude = ('image', 'material', 'budget',)

class VideoForm(forms.ModelForm):

    class Meta:
        model = Video
        fields = '__all__'
        # exclude = ('image', 'material', 'budget',)