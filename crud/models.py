from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class EmailVerification():
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email

# redefined base user
class User(AbstractUser):
    # redefine email - field should be unique
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    USERNAME_FIELD = 'email'  # For authentication
    REQUIRED_FIELDS = ['username']  # For superuser
