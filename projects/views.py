from django.shortcuts import render
from .models import Illustration
from .forms import IllustrationFilter

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
