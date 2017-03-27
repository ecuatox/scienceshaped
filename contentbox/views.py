from django.shortcuts import render
from django.http import HttpResponseRedirect
from authentication.templatetags import authentication_groups as groups
from .models import ContentBox
from .forms import ContentBoxForm

def contentbox(request, title):
    if groups.inGroup(request.user, 'editor'):
        if request.method == 'POST':

            form = ContentBoxForm(request.POST)
            if form.is_valid():
                contentBox = ContentBox.get(title)
                contentBox.content = form.cleaned_data['content']
                contentBox.save()
                #messages.add_message(request, messages.SUCCESS, 'Content of %s was successfully saved' % title)

            return HttpResponseRedirect('/')

        else:
            contentBox = ContentBox.get(title)
            form = ContentBoxForm(initial={
                'title': contentBox.title,
                'content': contentBox.content,
            })
            context = {
                'form': form,
            }
            return render(request, 'contentbox/contentbox.html', context)
    else:
        return HttpResponseRedirect('/')
