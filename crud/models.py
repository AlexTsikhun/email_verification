from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# redefined base user
class User(AbstractUser):
    # redefine email - field should be unique
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    email_verified = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'  # For authentication
    REQUIRED_FIELDS = ['username']  # For superuser

# DELETE WITH AJAX
# EDIT NEW PATH
