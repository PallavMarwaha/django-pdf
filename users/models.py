from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom user model for adding additional user authentication fields
    """

    def __str__(self) -> str:
        return self.username
