from django.urls import include, path
from django.views.generic import TemplateView

from crud import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('users/', include('django.contrib.auth.urls')),
    path('register/', views.Register.as_view(), name='register'),
]