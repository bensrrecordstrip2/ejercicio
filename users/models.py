from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
#creación de la tabla permisos
class Permission(models.Model):
    name = models.CharField(max_length=200)



#creación de la tabla Role
class Role(models.Model):
    name = models.CharField(max_length=200)
    permissions = models.ManyToManyField(Permission)


#creacion de la tabla usuario
class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password =models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    username = None
    #entramos por medio del email al sistema
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
