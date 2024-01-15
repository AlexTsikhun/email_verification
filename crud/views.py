from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View

from crud import models
from crud.forms import UserCreationForm


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
            login(request, user)
            return redirect('home')
        xt = {
            'form': form,
        }
        return render(request, self.template_name, xt)


class ProfileView(View):
    template_name = 'profile.html'

    def get(self, request):
        data = models.User.objects.all()
        return render(request, self.template_name, {'data':data})

