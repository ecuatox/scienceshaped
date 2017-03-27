from django import forms
from ckeditor.widgets import CKEditorWidget

class ContentBoxForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget(), required=False, label='')
