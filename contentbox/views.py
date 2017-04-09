from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import ContentBox
from .forms import ContentBoxForm


@permission_required('contentbox.add_contentbox')
@permission_required('contentbox.change_contentbox')
def contentbox(request, title):
    if request.method == 'POST':

        form = ContentBoxForm(request.POST)
        if form.is_valid():
            contentBox = ContentBox.get(title)
            contentBox.content = form.cleaned_data['content']
            contentBox.save()
            # messages.add_message(request, messages.SUCCESS, 'Content of %s was successfully saved' % title)

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
