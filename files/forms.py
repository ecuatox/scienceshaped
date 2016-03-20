from django import forms

class ImageUpload(forms.Form):
    title = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=100, required=False)
    file = forms.FileField()

class ImageSearch(forms.Form):
    search = forms.CharField(max_length=100)

class ImageSelect(forms.Form):
    defaultImage = forms.CharField(max_length=100)
