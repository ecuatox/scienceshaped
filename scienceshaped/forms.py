from django import forms
from ckeditor.widgets import CKEditorWidget

class Mail(forms.Form):
    email = forms.CharField(max_length=300, label='Email')
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(max_length=1000, label='Message')

class ContentBoxEdit(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())
