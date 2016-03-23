from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Illustration
from .forms import IllustrationFilter, IllustrationEdit
from scienceshaped import admin_history

def illustrations(request):
    illustrations = Illustration.objects.order_by('-pub_date')
    form = IllustrationFilter()
    context = {
        'illustrations': illustrations,
        'form': form,
    }

    return render(request, 'illustrations.html', context)

def illustration(request, illustration_id):
    illustration = Illustration.objects.get(pk=illustration_id)
    context = {
        'illustration': illustration,
    }

    return render(request, 'illustration.html', context)

def illustrationEdit(request, illustration_id):
    new = True
    if request.method == 'POST':
        form = IllustrationEdit(request.POST)
        if form.is_valid():
            if int(illustration_id) == 0:
                illustration = Illustration()
            else:
                illustration = Illustration.objects.get(pk=illustration_id)
            illustration.title = form.cleaned_data['title']
            illustration.description = form.cleaned_data['description']
            illustration.tags = form.cleaned_data['tags']
            illustration.thumbnail = form.cleaned_data['thumbnail']
            illustration.thumbnail_size = form.cleaned_data['thumbnail_size']
            illustration.save()
            if int(illustration_id) == 0:
                admin_history.log_addition(request, illustration)
            else:
                admin_history.log_change(request, illustration)
            return HttpResponseRedirect('/')
    else:
        if int(illustration_id) == 0:
            form = IllustrationEdit(initial={
                'title': '',
                'description': '',
                'tags': '',
                'thumbnail': '/static/img/click_to_select.png',
                'thumbnail_size': 100,
            })
        else:
            try:
                illustration = Illustration.objects.get(pk=illustration_id)
            except illustrations.DoesNotExist:
                return HttpResponseRedirect('/projects/illustration/0/edit')

            form = IllustrationEdit(initial={
                'title': illustration.title,
                'description': illustration.description,
                'tags': illustration.tags,
                'thumbnail': illustration.thumbnail,
                'thumbnail_size': illustration.thumbnail_size,
            })
            new = False
    context = {
        'form': form,
        'new': new,
    }

    return render(request, 'illustration_edit.html', context)

def illustrationDelete(request, illustration_id):
    try:
        illustration = Illustration.objects.get(pk=illustration_id)
        illustration.delete()
    except Illustration.DoesNotExist:
        pass

    return HttpResponseRedirect('/')
