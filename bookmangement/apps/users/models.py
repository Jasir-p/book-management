from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomeUser (AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateField(auto_now_add=True)



