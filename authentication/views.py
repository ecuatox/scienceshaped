from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from .forms import Login
from django.contrib.auth import login as auth_login, logout as auth_logout

def login(request):
    message = ''
    form = Login(initial={
        'username': '',
    })

    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    message = 'Account disabled'
            else:
                message = 'Wrong password'


    context = {
        'form': form,
        'message': message,
    }

    return render(request, 'authentication/login.html', context)

def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)

    return HttpResponseRedirect('/')
