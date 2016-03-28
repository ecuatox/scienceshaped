from django import forms

class Mail(forms.Form):
    email = forms.CharField(max_length=300, label='Email')
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(max_length=1000, label='Message')
