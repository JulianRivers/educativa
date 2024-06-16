from ova.views import index, lecciones
from django.urls import path
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('lecciones', lecciones, name='lecciones')
]