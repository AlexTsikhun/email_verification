from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .utils import send_email_for_veiry

User = get_user_model()

# redefine new form
class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class AuthenticationForm(DjangoUserCreationForm):
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache.email_verify:
                send_email_for_veiry(self.request, self.user_cache)
                raise ValidationError(
                    'Email is not verify, check your email',
                    code='invalid_login',
                )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data