from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, User, AbstractUser
from django.db import models

User._meta.get_field('email')._unique = True
User._meta.get_field('email')._blank = False
