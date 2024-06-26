from ova.views import index, lecciones, subirFormativa, subirSumativa, update_progress, get_progress
from django.urls import path
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('lecciones', lecciones, name='lecciones'),
    path('update_progress/', update_progress, name='update_progress'),
    path('subir-sumativa/', subirSumativa),
    path('subir-formativa/', subirFormativa),
    path('obtener-progreso/', get_progress, name='update_progress')
]