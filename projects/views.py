from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from scienceshaped import admin_history
from django.utils import timezone
from datetime import datetime, timedelta

from .forms import IllustrationEdit, TestimonialEdit
from .models import Illustration, Testimonial
from files.models import Image
from tags.models import Tag


@permission_required('projects.change_illustration')
@permission_required('projects.add_illustration')
def illustrationEdit(request, illustration_id):
    new = True
    images = []
    if request.method == 'POST':
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
            illustration.tags.clear()
            for tag in form.cleaned_data['tags']:
                illustration.tags.add(tag)
            illustration.url = form.cleaned_data['url']
            illustration.hidden = form.cleaned_data['hidden']
            if 'file' in request.FILES:
                illustration.pdf = request.FILES['file']
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
                'tags': illustration.tags.all(),
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
        'illustration_tags': Tag.objects.filter(group__title='illustrations'),
    }

    return render(request, 'projects/illustration_edit.html', context)


@permission_required('projects.delete_illustration')
def illustrationDelete(request, illustration_id):
    try:
        illustration = Illustration.objects.get(pk=illustration_id)
        illustration.delete()
        admin_history.log_deletion(request, illustration)
    except Illustration.DoesNotExist:
        pass

    return HttpResponseRedirect('/#illustrations')


@permission_required('projects.delete_testimonial')
def testimonialDelete(request, testimonial_id):
    try:
        testimonial = Testimonial.objects.get(pk=testimonial_id)
        testimonial.delete()
        admin_history.log_deletion(request, testimonial, testimonial.person)
    except Testimonial.DoesNotExist:
        pass

    return HttpResponseRedirect('/#testimonials')


@permission_required('projects.change_testimonial')
@permission_required('projects.add_testimonial')
def testimonialEdit(request, testimonial_id):
    new = True
    if request.method == 'POST':
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
