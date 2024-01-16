from re import template

from django.urls import include, path
from django.views.generic import TemplateView

from crud import views

urlpatterns = [
    # redefine existing `login`
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('users/', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', views.EmailVerify.as_view(), name='verify_email'),
    path(
        'invalid_verify/', 
        TemplateView.as_view(template_name='registration/invalid_verify.html'), 
        name='invalid_verify',
        ),
]