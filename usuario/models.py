from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager)
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

from ova.models import Actividad
# Modelos de la base de datos relacionados a los usuarios clientes o administrador

class UserProfileManager(BaseUserManager):
    """ Manager del Modelo de Perfil de Usarios """

    def create_user(self, email, name, apellidos, password=None):
        """ Crear nuevo UserProfile"""
        if not email:
            raise ValueError('Usuario debe tener un email')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, apellidos=apellidos)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, apellidos, password):
        """ Crear un Super Usuario"""
        user = self.create_user(email, name, apellidos, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Modelo Base de datos para Usuarios en el Sistema """
    email = models.EmailField('Email', max_length=255, unique=True)
    name = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    direccion = models.CharField('Direccion', max_length=500)
    celular = models.CharField('Celular', max_length=20, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    class Meta(AbstractUser.Meta):
        pass

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', "apellidos"]

    def get_full_name(self):
        ''' Obtener nombre completo del usuario'''
        return self.name

    def get_short_name(self):
        ''' Obtener nombre corto del usuario '''
        return self.name

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return self.name

class Puntaje(models.Model):
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    resultado = models.DecimalField('Resultado', max_digits=5, decimal_places=2)
    is_sumativo = models.BooleanField()

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return f"{self.usuario} nota: {self.resultado}"
