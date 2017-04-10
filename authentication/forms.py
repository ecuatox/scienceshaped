from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(AuthenticationForm):
    def clean(self):
        form_data = self.cleaned_data

        try:
            form_data['username'] = form_data['username'].lower()
            user = authenticate(
                username=form_data['username'],
                password=form_data['password'],
            )
        except KeyError:
            raise ValidationError({'password': 'All fields are required'}, code='required')

        if not user:
            try:
                inactive_user = User.objects.get(username=form_data['username'])
                if inactive_user.check_password(form_data['password']):
                    raise ValidationError({'password': 'Account disabled'}, code='invalid')
            except User.DoesNotExist:
                pass

            raise ValidationError({'password': 'Wrong password'}, code='invalid')

        return form_data