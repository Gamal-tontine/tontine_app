from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from .manage import CustomeUser

statue_choise = [
    ('user', 'utilisateur'),
    ('admin', 'gestionnaire'),
]

class User(AbstractUser,PermissionsMixin):
    first_name = models.CharField(max_length=30,null= False, blank= False)
    last_name = models.CharField(max_length=30,null= False, blank= False)
    email = models.EmailField(null= False, blank= False, unique=True)
    phone_number = models.IntegerField(null=True, blank= False)
    profil = models.ImageField(upload_to='media/user', null= True, blank= True)
    statue = models.CharField(max_length=30, default='user', choices=statue_choise)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    date_joined = models.DateField(default=timezone.now)
    username = None

    objects = CustomeUser()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','password']

    def __str__(self):
        return f'le nom {self.fist_name} {self.last_name}'