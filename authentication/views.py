from django.contrib.auth import logout as auth_logout, login, authenticate as auth
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic.edit import FormView

from .forms import LoginForm


class Login(FormView):
    template_name = 'authentication/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, auth(username=form.cleaned_data['username'], password=form.cleaned_data['password']))
        messages.info(self.request, 'Login successful')
        return super(Login, self).form_valid(form)


class Logout(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)
            messages.info(request, 'Logout successful')

        return HttpResponseRedirect(self.success_url)
