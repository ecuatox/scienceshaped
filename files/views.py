from django.shortcuts import render
from .models import Image
from .forms import ImageUpload, ImageSearch, ImageSelect, ImageEdit
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from scienceshaped import admin_history
import os
from django.conf import settings
from authentication.templatetags import authentication_groups as groups

def findId(title):
    number = 1
    for element in Image.objects.order_by('-time'):
        if title.lower() == element.title.lower():
            return element.number + 1
    return number

def fileExt(name):
    return name.split(".")[-1:][0]

def saveImage(file, title, tags):
    while " " in title:
        title = title.replace(" ", "_")
    number = findId(title)
    if number > 1:
        file.name = title.lower()+"_"+str(number)+"."+fileExt(file.name)
    else:
        file.name = title.lower()+"."+fileExt(file.name)
    instance = Image(file=file, title=title, tags=tags, time=timezone.now(), number=number)
    instance.save()
    return instance

def renameImage(instance, title):
    while " " in title:
        title = title.replace(' ', '_')
    instance.number = findId(title)
    oldpath = instance.file.name
    directory = settings.MEDIA_ROOT
    print(instance.file.name)
    if instance.number > 1:
        instance.file.name = 'images/'+title.lower()+'_'+str(instance.number)+'.'+fileExt(instance.file.name)
    else:
        instance.file.name = 'images/'+title.lower()+'.'+fileExt(instance.file.name)
    #try:
    os.rename(directory+'/'+oldpath, directory+'/'+instance.file.name)
    #except FileNotFoundError:
    #    pass
    instance.save()
    return instance

def imageUpload(request):
    if request.method == 'POST' and groups.inGroup(request.user, 'editor'):
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            img = saveImage(request.FILES['file'], str(form.cleaned_data['title']), str(form.cleaned_data['tags']))
            context = {
                'src': img.file.name,
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

def imageDelete(request, image_id):
    if groups.inGroup(request.user, 'editor'):
        try:
            image = Image.objects.get(pk=image_id)
            image.delete()
            admin_history.log_deletion(request, image)
        except Image.DoesNotExist:
            pass

    return HttpResponseRedirect('/files/images')

def imageEdit(request, image_id):
    if request.method == 'POST' and groups.inGroup(request.user, 'editor'):
        form = ImageEdit(request.POST)
        if form.is_valid():
            try:
                image = Image.objects.get(pk=image_id)
                title = str(form.cleaned_data['title'])
                if title != image.title:
                    image = renameImage(image, str(form.cleaned_data['title']))
                image.title = title
                image.tags = str(form.cleaned_data['tags'])
                image.save()
                admin_history.log_change(request, image)
            except Image.DoesNotExist:
                pass
            return HttpResponseRedirect('/files/images')
    else:
        try:
            image = Image.objects.get(pk=image_id)
        except Image.DoesNotExist:
            return HttpResponseRedirect('/files/images')

        form = ImageEdit(initial={
            'title': image.title,
            'tags': image.tags,
            'file': image.file,
        })
    context = {
        'form': form,
    }

    return render(request, 'image_edit.html', context)
