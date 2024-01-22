from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View

from crud import models
from crud.forms import AuthenticationForm, UserCreationForm

from .utils import is_verify_email, send_email_for_veiry

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

            # Check email, but form also checks
            if is_verify_email(email):
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
    

class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request):
        data = models.User.objects.all()
        return render(request, self.template_name, {'table_data':data})


class UserInfoView(View):
    template_name = 'user_info.html'
    def get(self, request, user_id):
        user_info = models.User.objects.get(id=user_id)
        context = {
            'user_info': user_info,
        }
        return render(request, self.template_name, context)


class DeleteUserView(View):
    def get(self, request, user_id):
        # delete_user = get_object_or_404(models.User, id=user_id)
        delete_user = models.User.objects.get(id=user_id)
        delete_user.delete()
        return redirect('dashboard')


class UpdateUserView(View):
    def  get(self, request, user_id):
        # get updated data from modal window
        username = request.GET.get('username')
        email = request.GET.get('email')
        verified = request.GET.get('verified')
        date_joined = request.GET.get('date_joined')
        
        obj = models.User.objects.get(id=user_id)
        # change actual data to modified
        obj.username = username
        obj.email = email
        obj.email_verified = verified
        obj.date_joined = date_joined

        obj.save()

        user = {
                'username': obj.username,
                'email': obj.email,
                'email_verified': obj.email_verified,
                'date_joined': obj.date_joined,
        }
        print(user)
        data = {
            'user': user,
        }
        return JsonResponse(data)
