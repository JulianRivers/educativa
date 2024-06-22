from django.db import models

# Create your models here.
class Actividad(models.Model):
    titulo = models.CharField('Titulo', max_length=100)

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return f"{self.usuario} nota: {self.resultado}"
