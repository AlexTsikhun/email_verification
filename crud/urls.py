from django.urls import include, path
from django.views.generic import TemplateView

from crud import views

urlpatterns = [
    # redefine existing `login`
    path('login/', views.MyLoginView.as_view(), name='login'),

    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('users/', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
    
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('confirm_email/', TemplateView.as_view(template_name='registration/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', views.EmailVerify.as_view(), name='verify_email'),
    path(
        'invalid_verify/', 
        TemplateView.as_view(template_name='registration/invalid_verify.html'), 
        name='invalid_verify',
        ),
    path('user/<int:user_id>', views.UserInfoView.as_view(), name='user_info'),
    path('delete_user/<int:user_id>', views.DeleteUserView.as_view(), name='delete_user'),
    path('update_user/<int:user_id>', views.UpdateUserView.as_view(), name='update_user'),
]