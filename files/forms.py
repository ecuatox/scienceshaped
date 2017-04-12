from django import forms
from tags.models import Tag

class ImageUpload(forms.Form):
    title = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=1000, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=100, required=False)
    file = forms.FileField()

    def clean(self):
        form_data = self.cleaned_data
        form_data['tags'] = Tag.clean_tags(form_data['tags'])
        return form_data

class ImageEdit(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    tags = forms.CharField(max_length=1000, required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=100, required=False)

    def clean(self):
        form_data = self.cleaned_data
        form_data['tags'] = Tag.clean_tags(form_data['tags'])
        return form_data
