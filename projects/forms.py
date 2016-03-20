from django import forms

class IllustrationFilter(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.HiddenInput())
