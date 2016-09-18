from django.shortcuts import render
from projects.models import Illustration, Testimonial
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import EmailMessage
from .forms import Mail, ContentBoxEdit
from .models import ContentBox
from django.conf import settings
import projects.views
from authentication.templatetags import authentication_groups as groups

def index(request, tag='all', action=''):
    toast = ''
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
            toast = 'Your message was submitted successfully!'
        else:
            toast = 'Please correct the error(s)'
    else:
        mailForm = Mail(initial={
            'email': '',
            'subject': '',
            'message': ''
        })
    try:
        aboutContent = ContentBox.objects.get(title='About').content
    except ContentBox.DoesNotExist:
        ContentBox(title='About', content='').save()
        aboutContent = ''
    aboutForm = ContentBoxEdit(initial={
        'content': aboutContent,
    })

    try:
        infoContent = ContentBox.objects.get(title='Info').content
    except ContentBox.DoesNotExist:
        ContentBox(title='Info', content='').save()
        infoContent = ''
    infoForm = ContentBoxEdit(initial={
        'content': infoContent,
    })

    context = {
        'illustrations': illustrations,
        'testimonials': testimonials,
        'mailForm': mailForm,
        'aboutForm': aboutForm,
        'aboutContent': aboutContent,
        'infoForm': infoForm,
        'infoContent': infoContent,
        'tags': tags,
        'toast': toast,
        'action': action,
        'hidden': settings.HIDDEN,
    }
    return render(request, 'index.html', context)

def login(request):
    return HttpResponseRedirect('/authentication/login')

def infoEdit(request):
    if groups.inGroup(request.user, 'editor'):
        if request.method == 'POST':
            infoForm = ContentBoxEdit(request.POST)
            if infoForm.is_valid():
                try:
                    contentBox = ContentBox.objects.get(title='Info')
                except ContentBox.DoesNotExist:
                    contentBox = ContentBox(title='Info', content='').save()
                contentBox.content = infoForm.cleaned_data['content']
                contentBox.save()
            return HttpResponseRedirect('/')
        else:
            return index(request, action='infoEdit')
    else:
        return HttpResponseRedirect('/')
