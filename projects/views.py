from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Illustration, Testimonial
from files.models import Image
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

    return render(request, 'projects/illustrations.html', context)

def illustration(request, illustration_id):
    illustration = Illustration.objects.get(pk=illustration_id)
    context = {
        'illustration': illustration,
    }

    return render(request, 'projects/illustration.html', context)

def getIllustrationTags():
    illustrations = Illustration.objects.all()
    tags = set([])
    for illustration in illustrations:
        tags.update(illustration.tags.split(", "))
    while '' in tags:
        tags.remove('')
    return sorted(tags)

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
    images = []
    if request.method == 'POST' and groups.inGroup(request.user, 'editor'):
        form = IllustrationEdit(request.POST)

        try:
            raw_images = dict(request.POST)['image']
            while '' in raw_images:
                raw_images.remove('')
            images.extend(raw_images)
        except KeyError:
            pass

        if form.is_valid():
            if int(illustration_id) == 0:
                illustration = Illustration()
                illustration.save()
            else:
                illustration = Illustration.objects.get(pk=illustration_id)
            illustration.title = form.cleaned_data['title']
            illustration.description = form.cleaned_data['description']
            illustration.short = form.cleaned_data['short']
            illustration.tags = form.cleaned_data['tags']
            illustration.url = form.cleaned_data['url']
            illustration.hidden = form.cleaned_data['hidden']
            if 'pdf' in request.FILES:
                illustration.pdf = request.FILES['pdf']
            else:
                illustration.pdf = None
            thumbnail_raw = form.cleaned_data['thumbnail']
            try:
                thumb_id = int(thumbnail_raw)
                illustration.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, ValueError, Image.DoesNotExist):
                illustration.thumbnail = None

            illustration.images.clear()
            for image in images:
                try:
                    image_id = int(image)
                    illustration.images.add(Image.objects.get(id=image_id))
                except (TypeError, ValueError, Image.DoesNotExist):
                    pass

            illustration.thumbnail_size = form.cleaned_data['thumbnail_size']
            illustration.date = datetime.strptime(form.cleaned_data['date'], '%B %d, %Y').date()
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
                'short': '',
                'tags': '',
                'url': '',
                'pdf': '',
                'thumbnail': '0',
                'thumbnail_size': 100,
                'date': datetime.strftime(timezone.now(), '%B %d, %Y'),
            })
        else:
            try:
                illustration = Illustration.objects.get(pk=illustration_id)
            except Illustration.DoesNotExist:
                return HttpResponseRedirect('/projects/illustration/0/edit')

            images.extend([image.id for image in illustration.images.all()])

            try:
                thumb = illustration.thumbnail.id
            except AttributeError:
                thumb = 0

            form = IllustrationEdit(initial={
                'title': illustration.title,
                'description': illustration.description,
                'short': illustration.short,
                'tags': illustration.tags,
                'hidden': illustration.hidden,
                'url': illustration.url,
                'pdf': illustration.pdf_getname(),
                'thumbnail': thumb,
                'thumbnail_size': illustration.thumbnail_size,
                'date': datetime.strftime(illustration.date + timedelta(days=1), '%B %d, %Y'),
            })
            new = False

    context = {
        'form': form,
        'images': images,
        'new': new,
    }

    return render(request, 'projects/illustration_edit.html', context)

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
    testimonials = Testimonial.objects.order_by('-date')
    context = {
        'testimonials': testimonials,
    }

    return render(request, 'projects/testimonials.html', context)

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
            testimonial.hidden = form.cleaned_data['hidden']
            testimonial.date = datetime.strptime(form.cleaned_data['date'], '%B %d, %Y').date()
            thumbnail_raw = form.cleaned_data['thumbnail']
            try:
                thumb_id = int(thumbnail_raw)
                testimonial.thumbnail = Image.objects.get(id=thumb_id)
            except (TypeError, ValueError, Image.DoesNotExist):
                testimonial.thumbnail = None
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
                'thumbnail': '0',
                'date': datetime.strftime(timezone.now(), '%B %d, %Y'),
            })
        else:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect('/projects/testimonial/0/edit')
            try:
                thumb_id = testimonial.thumbnail.id
            except AttributeError:
                thumb_id = 0
            form = TestimonialEdit(initial={
                'person': testimonial.person,
                'job': testimonial.job,
                'message': testimonial.message,
                'hidden': testimonial.hidden,
                'thumbnail': thumb_id,
                'date': datetime.strftime(testimonial.date + timedelta(days=1), '%B %d, %Y'),
            })
            new = False
    context = {
        'form': form,
        'new': new,
    }

    return render(request, 'projects/testimonial_edit.html', context)
