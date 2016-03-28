from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Illustration, Testimonial
from .forms import IllustrationEdit, TestimonialEdit
from scienceshaped import admin_history
from authentication.templatetags import authentication_groups as groups
from django.utils import timezone
from datetime import datetime, timedelta

def illustrations(request):
    illustrations = Illustration.objects.order_by('-date')
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

def getIllustrationTags():
    illustrations = Illustration.objects.all()
    tags = set([])
    for illustration in illustrations:
        tags.update(illustration.tags.split(", "))
    return tags

def illustrationTagDelete(request, tag):
    if groups.inGroup(request.user, 'editor'):
        illustrations = Illustration.objects.all()
        for illustration in illustrations:
            tags = illustration.tags.split(', ')
            while tag in tags:
                tags.remove(tag)
            newTags = ''
            for t in tags:
                newTags += t + ', '
            if newTags.endswith(', '):
                newTags = newTags[:-2]
            illustration.tags = newTags
            illustration.save()
    return HttpResponseRedirect('/')

def illustrationEdit(request, illustration_id):
    new = True
    if request.method == 'POST' and groups.inGroup(request.user, 'editor'):
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
            illustration.date = datetime.strptime(form.cleaned_data['date'], '%d %B, %Y').date()
            illustration.save()
            if int(illustration_id) == 0:
                admin_history.log_addition(request, illustration)
            else:
                admin_history.log_change(request, illustration)
            return HttpResponseRedirect('/#illustrations')
    else:
        if int(illustration_id) == 0:
            form = IllustrationEdit(initial={
                'title': '',
                'description': '',
                'tags': '',
                'thumbnail': '/static/img/click_to_select.png',
                'thumbnail_size': 100,
                'date': datetime.strftime(timezone.now(), '%-d %B, %Y'),
            })
        else:
            try:
                illustration = Illustration.objects.get(pk=illustration_id)
            except Illustration.DoesNotExist:
                return HttpResponseRedirect('/projects/illustration/0/edit')

            form = IllustrationEdit(initial={
                'title': illustration.title,
                'description': illustration.description,
                'tags': illustration.tags,
                'thumbnail': illustration.thumbnail,
                'thumbnail_size': illustration.thumbnail_size,
                'date': datetime.strftime(illustration.date + timedelta(days=1), '%-d %B, %Y'),
            })
            new = False
    context = {
        'form': form,
        'new': new,
    }

    return render(request, 'illustration_edit.html', context)

def illustrationDelete(request, illustration_id):
    if groups.inGroup(request.user, 'editor'):
        try:
            illustration = Illustration.objects.get(pk=illustration_id)
            illustration.delete()
            admin_history.log_deletion(request, illustration)
        except Illustration.DoesNotExist:
            pass

    return HttpResponseRedirect('/#illustrations')

def testimonials(request):
    testimonials = Testimonial.objects.order_by('-pub_date')
    context = {
        'testimonials': testimonials,
    }

    return render(request, 'testimonials.html', context)

def testimonialDelete(request, testimonial_id):
    if groups.inGroup(request.user, 'editor'):
        try:
            testimonial = Testimonial.objects.get(pk=testimonial_id)
            testimonial.delete()
            admin_history.log_deletion(request, testimonial, testimonial.person)
        except Testimonial.DoesNotExist:
            pass

    return HttpResponseRedirect('/#testimonials')

def testimonialEdit(request, testimonial_id):
    new = True
    if request.method == 'POST'  and groups.inGroup(request.user, 'editor'):
        form = TestimonialEdit(request.POST)
        if form.is_valid():
            if int(testimonial_id) == 0:
                testimonial = Testimonial()
            else:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
            testimonial.person = form.cleaned_data['person']
            testimonial.job = form.cleaned_data['job']
            testimonial.message = form.cleaned_data['message']
            testimonial.thumbnail = form.cleaned_data['thumbnail']
            testimonial.save()
            if int(testimonial_id) == 0:
                admin_history.log_addition(request, testimonial, testimonial.person)
            else:
                admin_history.log_change(request, testimonial, testimonial.person)
            return HttpResponseRedirect('/#testimonials')
    else:
        if int(testimonial_id) == 0:
            form = TestimonialEdit(initial={
                'person': '',
                'job': '',
                'message': '',
                'thumbnail': '/static/img/click_to_select.png',
            })
        else:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect('/projects/testimonial/0/edit')

            form = TestimonialEdit(initial={
                'person': testimonial.person,
                'job': testimonial.job,
                'message': testimonial.message,
                'thumbnail': testimonial.thumbnail,
            })
            new = False
    context = {
        'form': form,
        'new': new,
    }

    return render(request, 'testimonial_edit.html', context)
