from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.



class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, name,address,phone,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            username=username,
            email = self.normalize_email(email),
            name = name,
            address = address,
            phone = phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class Customers(AbstractBaseUser):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=100)
    status=models.CharField(max_length=100,default='ACTIVE')

    # required
    date_joined = models.DateTimeField(auto_now_add=True,null=True)
    last_login = models.DateTimeField(auto_now_add=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True



