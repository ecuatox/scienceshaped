from django import forms

class IllustrationEdit(forms.Form):
    title = forms.CharField(max_length=100, label='Title')
    short = forms.CharField(widget=forms.Textarea, max_length=200, required=False, label='Short Description')
    description = forms.CharField(widget=forms.Textarea, max_length=500, required=False, label='Description')
    tags = forms.CharField(max_length=500, required=False, label='Tags')

    thumbnail = forms.IntegerField(required=False, label='Thumbnail')
    thumbnail_size = forms.CharField(max_length=4, label='Thumbnail size (%)')

    date = forms.CharField(max_length=100, label='Date')

    numberOfImages = forms.IntegerField()

    image1 = forms.IntegerField(required=False, label='Image')
    image2 = forms.IntegerField(required=False, label='Image')
    image3 = forms.IntegerField(required=False, label='Image')

class TestimonialEdit(forms.Form):
    person = forms.CharField(max_length=100, label="Person")
    job = forms.CharField(max_length=300, required=False, label="Job")
    message = forms.CharField(max_length=1000, label="Message")

    date = forms.CharField(max_length=100, label='Date')
    
    thumbnail = forms.IntegerField(required=False, label='Thumbnail')
