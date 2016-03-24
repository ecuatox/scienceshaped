from django.shortcuts import render
from projects.models import Illustration, Testimonial
from projects.forms import IllustrationFilter
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    illustrations = Illustration.objects.order_by('-pub_date')
    testimonials = Testimonial.objects.order_by('-pub_date')
    if request.method == 'POST':
        form = IllustrationFilter(request.POST)
        if form.is_valid():
            search = str(form.cleaned_data['search']).lower()
            if search != "all":
                illustrations = []
                for illustration in Illustration.objects.order_by('-pub_date'):
                    if search in illustration.tags.lower():
                        illustrations.append(illustration)
    form = IllustrationFilter()
    context = {
        'illustrations': illustrations,
        'testimonials': testimonials,
        'form': form,
    }

    return render(request, 'index.html', context)

def login(request):
    return HttpResponseRedirect('/authentication/login')
