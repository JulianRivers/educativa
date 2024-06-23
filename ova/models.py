from django.db import models


# Create your models here.
class Unidad(models.Model):
    titulo = models.CharField('Titulo', max_length=100)
    ariaLabel = models.CharField('Aria Label', max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'unidades'

class Lecciones(models.Model):
    titulo = models.CharField('Titulo', max_length=100)
    link = models.CharField('Link', max_length=100)
    template = models.CharField('Template', max_length=255)
    unidad = models.ForeignKey(Unidad, related_name='lecciones', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'lecciones'

    def __str__(self):
        return f"{self.titulo}"

class Actividad(models.Model):
    titulo = models.CharField('Titulo', max_length=100)
    leccion = models.ForeignKey(Lecciones, related_name='actividades', on_delete=models.SET_NULL, null=True)
    is_sumativo = models.BooleanField('sumativa', default=False)
    class Meta:
        db_table = 'actividades'

    def __str__(self):
        ''' Obtener cadena representativa de nuestro usuario '''
        return f"{self.titulo}"

class ProgresoLeccion(models.Model):
    usuario = models.ForeignKey("usuario.UserProfile", on_delete=models.SET_NULL, null=True, blank=True)
    unidad = models.ForeignKey(Lecciones, on_delete=models.SET_NULL, null=True, blank=True)
    progreso = models.IntegerField(default=0)
    completado = models.BooleanField(default=False)

    class Meta:
        db_table = 'progreso_lecciones'

    def __str__(self):
        return f"{self.usuario.username} - {self.unidad.nombre}"