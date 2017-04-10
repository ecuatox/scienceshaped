from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from projects.models import Illustration, Testimonial
from tags.models import Tag
from .forms import Mail
from contentbox.models import ContentBox


def index(request, tag='all'):
    if request.method == 'POST':
        mailForm = Mail(request.POST)
        if mailForm.is_valid():
            mailForm.send()
            mailForm = Mail()
            messages.success(request, 'Your message was submitted successfully!')
        else:
            messages.error(request, 'Please correct the error(s)')
    else:
        mailForm = Mail()

    context = {
        'illustrations': Illustration.filter_tag(tag).order_by('-date'),
        'testimonials': Testimonial.objects.order_by('-date'),
        'mailForm': mailForm,
        'aboutContent': ContentBox.getContent('about'),
        'infoContent': ContentBox.getContent('info'),
        'illustration_tags': Tag.objects.filter(group__title='illustrations'),
    }
    return render(request, 'scienceshaped/index.html', context)


def login(request):
    return HttpResponseRedirect('/authentication/login')
