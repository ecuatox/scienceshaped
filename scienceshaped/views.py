from django.shortcuts import render
from projects.models import Illustration, Testimonial
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage
from .forms import Mail
from contentbox.models import ContentBox
from django.conf import settings
import projects.views
from django.contrib import messages
from authentication.templatetags import authentication_groups as groups

def index(request, tag='all'):

    testimonials = Testimonial.objects.order_by('-date')

    if tag == 'all':
        illustrations = Illustration.objects.order_by('-date')
    else:
        tag = tag.lower()
        illustrations = []
        for illustration in Illustration.objects.order_by('-date'):
            if tag in illustration.tags.lower():
                illustrations.append(illustration)

    tags = projects.views.getIllustrationTags()

    if request.method == 'POST':
        mailForm = Mail(request.POST)
        if mailForm.is_valid():
            email = mailForm.cleaned_data['email']
            subject = mailForm.cleaned_data['subject']
            message = 'This mail was generated by the contactform on scienceshaped.com\n'
            message += 'The users email adress: ' + email + '\n\n'
            message += mailForm.cleaned_data['message']
            EmailMessage(subject, message, email, [settings.CONTACT_EMAIL], reply_to=[email], headers={'From': 'ScienceShaped Contactform'}).send()
            mailForm = Mail(initial={
                'email': '',
                'subject': '',
                'message': ''
            })
            messages.add_message(request, messages.SUCCESS, 'Your message was submitted successfully!')
        else:
            messages.add_message(request, messages.ERROR, 'Please correct the error(s)')
    else:
        mailForm = Mail(initial={
            'email': '',
            'subject': '',
        })

    context = {
        'illustrations': illustrations,
        'testimonials': testimonials,
        'mailForm': mailForm,
        'aboutContent': ContentBox.getContent('about'),
        'infoContent': ContentBox.getContent('info'),
        'tags': tags,
    }
    return render(request, 'scienceshaped/index.html', context)

def login(request):
    return HttpResponseRedirect('/authentication/login')
