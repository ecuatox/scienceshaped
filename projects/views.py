from django.shortcuts import render
from .models import Illustration

def illustrations(request):
    illustration_list = Illustration.objects.order_by('-pub_date')
    context = {
        'illustration_list': illustration_list,
    }

    return render(request, 'illustrations.html', context)

def illustration(request, illustration_id):
    illustration = Illustration.objects.get(pk=illustration_id)
    context = {
        'illustration': illustration,
    }

    return render(request, 'illustration.html', context)
