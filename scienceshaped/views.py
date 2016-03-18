from django.shortcuts import render
from projects.models import Illustration

def index(request):
    illustration_list = Illustration.objects.order_by('-pub_date')
    context = {
        'illustration_list': illustration_list,
    }

    return render(request, 'index.html', context)
