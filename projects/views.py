from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Illustration, Testimonial
from .forms import IllustrationFilter, IllustrationEdit, TestimonialEdit
from scienceshaped import admin_history
from authentication import templatetags

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
    if request.method == 'POST' and templatetags.tags.inGroup(request.user, 'editor'):
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
            return HttpResponseRedirect('/#illustrations')
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
            except Illustration.DoesNotExist:
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
    if templatetags.tags.inGroup(request.user, 'editor'):
        try:
            illustration = Illustration.objects.get(pk=illustration_id)
            illustration.delete()
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
    if templatetags.tags.inGroup(request.user, 'editor'):
        try:
            testimonial = Testimonial.objects.get(pk=testimonial_id)
            testimonial.delete()
        except Testimonial.DoesNotExist:
            pass

    return HttpResponseRedirect('/#testimonials')

def testimonialEdit(request, testimonial_id):
    new = True
    if request.method == 'POST'  and templatetags.tags.inGroup(request.user, 'editor'):
        form = TestimonialEdit(request.POST)
        if form.is_valid():
            if int(testimonial_id) == 0:
                testimonial = Testimonial()
            else:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
            testimonial.title = form.cleaned_data['title']
            testimonial.person = form.cleaned_data['person']
            testimonial.message = form.cleaned_data['message']
            testimonial.thumbnail = form.cleaned_data['thumbnail']
            testimonial.save()
            if int(testimonial_id) == 0:
                admin_history.log_addition(request, testimonial)
            else:
                admin_history.log_change(request, testimonial)
            return HttpResponseRedirect('/#testimonials')
    else:
        if int(testimonial_id) == 0:
            form = TestimonialEdit(initial={
                'title': '',
                'person': '',
                'message': '',
                'thumbnail': '/static/img/click_to_select.png',
            })
        else:
            try:
                testimonial = Testimonial.objects.get(pk=testimonial_id)
            except Testimonial.DoesNotExist:
                return HttpResponseRedirect('/projects/testimonial/0/edit')

            form = TestimonialEdit(initial={
                'title': testimonial.title,
                'person': testimonial.person,
                'message': testimonial.message,
                'thumbnail': testimonial.thumbnail,
            })
            new = False
    context = {
        'form': form,
        'new': new,
    }

    return render(request, 'testimonial_edit.html', context)
