from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):

        user = self.create_user(
            email,
            password=password,
            **extra_fields
        )
        user.is_superuser = user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email Address', unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    photo = models.ImageField(blank=True, null=True, upload_to='account/photos/')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)


class Department(Group):

    class Meta:
        proxy = True


