from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add any custom fields you want to your user model
    bio = models.TextField(max_length=500, blank=True)
