from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class EmailVerification():
    email = models.EmailField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email

# redefined base user
class User(AbstractUser):
    pass