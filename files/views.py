import os
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponseRedirect
from scienceshaped import admin_history
from django.conf import settings

from .models import Image
from .forms import ImageUpload, ImageSearch, ImageEdit
from tags.models import Tag


def findId(title):
    number = 1
    for element in Image.objects.order_by('-time'):
        savename = element.title.lower()
        while ' ' in savename:
            savename = savename.replace(' ', '_')
        if title.lower() == savename:
            return element.number + 1
    return number


def fileExt(name):
    return str(name.split('.')[-1:][0].lower())


def saveImage(file, title, description, tags):
    savename = title.lower()
    savename = savename.replace(' ', '_')
    number = findId(savename)
    if number > 1:
        file.name = savename + '_' + str(number) + '.' + fileExt(file.name)
    else:
        file.name = savename + '.' + fileExt(file.name)
    instance = Image(file=file, title=title, description=description, time=timezone.now(), number=number)
    instance.save()
    instance.tags.clear()
    for tag in tags:
        instance.tags.add(tag)
    return instance


def renameImage(instance, title):
    savename = title.lower()
    while ' ' in savename:
        savename = savename.replace(' ', '_')
    instance.number = findId(title)
    oldpath = instance.file.name
    directory = settings.MEDIA_ROOT
    if instance.number > 1:
        instance.file.name = 'images/' + savename + '_' + str(instance.number) + '.' + fileExt(instance.file.name)
    else:
        instance.file.name = 'images/' + savename + '.' + fileExt(instance.file.name)
    # try:
    os.rename(directory + '/' + oldpath, directory + '/' + instance.file.name)
    # except FileNotFoundError:
    #    pass
    instance.save()
    return instance


@permission_required('files.add_image')
def imageUpload(request):
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            image = saveImage(
                file=request.FILES['file'],
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                tags=form.cleaned_data['tags']
            )
            admin_history.log_addition(request, image, image.title)
            return render(request, 'files/image_upload_done.html')
    else:
        form = ImageUpload(initial={
            'description': '',
            'title': '',
            'tags': '',
            'file': '',
        })

    context = {
        'form': form,
        'image_tags': Tag.objects.filter(group__title='images'),
    }
    return render(request, 'files/image_upload.html', context)


@permission_required('files.view_image_control_panel')
def images(request):
    searchText = ''
    if request.method == 'POST':
        form = ImageSearch(request.POST)
        images = []
        if form.is_valid():
            searchText = form.cleaned_data['search']
            search = searchText.lower()
            for image in Image.objects.order_by('-time'):
                if search in image.title.lower() or search in Tag.stringlist(image.tags):
                    images.append(image)
        else:
            images = Image.objects.order_by('-time')
    else:
        images = Image.objects.order_by('-time')
    form = ImageSearch()
    context = {
        'images': images,
        'form': form,
        'searchText': searchText,
    }
    return render(request, 'files/images.html', context)


@permission_required('files.delete_image')
def imageDelete(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
        image.delete()
        admin_history.log_deletion(request, image)
    except Image.DoesNotExist:
        pass
    return HttpResponseRedirect('/files/images')


def imageView(request, image_id):
    try:
        image = Image.objects.get(pk=image_id)
        return HttpResponseRedirect('/media/' + str(image.file))
    except Image.DoesNotExist:
        return HttpResponseRedirect('/')


@permission_required('files.change_image')
def imageEdit(request, image_id):
    if request.method == 'POST':
        form = ImageEdit(request.POST)
        if form.is_valid():
            try:
                image = Image.objects.get(pk=image_id)
                title = form.cleaned_data['title']
                if title != image.title:
                    image = renameImage(image, title)
                image.title = title
                image.description = form.cleaned_data['description']
                image.tags.clear()
                for tag in form.cleaned_data['tags']:
                    image.tags.add(tag)
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
            'description': image.description,
            'tags': image.tags.all(),
            'file': image.file,
        })

    context = {
        'form': form,
        'image_tags': Tag.objects.filter(group__title='images'),
    }

    return render(request, 'files/image_edit.html', context)
