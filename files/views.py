from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from scienceshaped import admin_history
from django.db.models import Q
from .models import Image
from .forms import ImageUpload, ImageEdit
from tags.models import Tag


@permission_required('files.view_image_control_panel')
def images(request):
    searchRaw = ''
    images = []
    if request.method == 'POST':
        if 'search' in request.POST:
            searchRaw = request.POST['search']
            search = Image.slugify(request.POST['search'])
            images = Image.objects.filter(Q(slug__contains=search) | Q(tags__label__contains=search)).distinct().order_by('-time')

    if not searchRaw:
        images = Image.objects.order_by('-time')

    context = {
        'images': images,
        'search': searchRaw,
    }
    return render(request, 'files/images.html', context)


@permission_required('files.add_image')
def imageUpload(request):
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            image = Image.saveImage(
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


@permission_required('files.change_image')
def imageEdit(request, image_id):
    if request.method == 'POST':
        form = ImageEdit(request.POST)
        if form.is_valid():
            try:
                image = Image.objects.get(pk=image_id)
                title = form.cleaned_data['title']
                if title != image.title:
                    image = image.renameImage(title)

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
