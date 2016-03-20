from django.shortcuts import render
from .models import Image
from .forms import ImageUpload, ImageSearch, ImageSelect
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse

def image_upload(request):
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            title = str(form.cleaned_data['title'])
            tags = str(form.cleaned_data['tags'])
            while " " in title:
                title = title.replace(" ", "_")
            file = request.FILES['file']

            number = 1
            for element in Image.objects.order_by('-time'):
                if title == element.title:
                    number = element.number + 1
                    break

            ext = file.name.split(".")[-1:][0]
            file.name = title+"_"+str(number)+"."+ext
            instance = Image(file=file, title=title, tags=tags, time=timezone.now(), number=number)
            instance.save()
            context = {
                'src': file.name,
            }
            return render(request, 'image_upload_done.html', context)
    else:
        form = ImageUpload()

    context = {
        'form': form,
    }
    return render(request, 'image_upload.html', context)

def images(request):
    searchText = ""
    defaultImage = ""
    if request.method == 'POST':
        form = ImageSearch(request.POST)
        images = []
        if form.is_valid():
            searchText = str(form.cleaned_data['search'])
            search = searchText.lower()
            for image in Image.objects.order_by('-time'):
                if search in image.title.lower() or search in image.tags.lower():
                    images.append(image)
        else:
            images = Image.objects.order_by('-time')
            form = ImageSelect(request.POST)
            if form.is_valid():
                defaultImage = str(form.cleaned_data['defaultImage'])
    else:
        images = Image.objects.order_by('-time')
    form = ImageSearch()
    context = {
        'images': images,
        'form': form,
        'searchText': searchText,
        'defaultImage': defaultImage,
    }
    return render(request, 'images.html', context)
