from django.shortcuts import render
from .models import Image
from .forms import ImageUpload
from django.utils import timezone
from django.http import HttpResponseRedirect

def image_upload(request):
    if request.method == 'POST':
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            title = str(form.cleaned_data['title'])
            while " " in title:
                title = title.replace(" ", "_")
            file = request.FILES['file']

            number = 0
            for element in Image.objects.order_by('-time'):
                if title == element.title:
                    number = element.number + 1
                    break

            ext = file.name.split(".")[-1:][0]
            file.name = title+"_"+str(number)+"."+ext
            instance = Image(file=file, title=title, time=timezone.now(), number=number)
            instance.save()
            return HttpResponseRedirect('/files/upload-done')
    else:
        form = ImageUpload()

    context = {
        'form': form,
    }
    return render(request, 'image_upload.html', context)

def upload_done(request):
    context = {
    }
    return render(request, 'upload_done.html', context)

def images(request):
    context = {
        'images': Image.objects.order_by('-time'),
    }
    return render(request, 'images.html', context)
