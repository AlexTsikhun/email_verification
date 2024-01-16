from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View

from crud import models
from crud.forms import AuthenticationForm, UserCreationForm

from .utils import send_email_for_veiry

User = get_user_model()

class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        """ return clear form
        """
        xt = {
            'form': UserCreationForm(),
        }
        return render(request, self.template_name, xt)
  
    def post(self, request):
        """ takes data from form and do stuff
        """
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = authenticate(email=email, password=password)
            # login(request, user)
            # return redirect('home')
            send_email_for_veiry(request, user)
            return redirect('confirm_email')
        xt = {
            'form': form,
        }
        return render(request, self.template_name, xt)


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verified = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class MyLoginView(View):
    form = AuthenticationForm
    

class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        data = models.User.objects.all()
        return render(request, self.template_name, {'data':data})

