from django import forms

class VKVideoLinkForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    link = forms.CharField(max_length=80)
    #All my attributes here