from rest_framework import serializers 
from .models import ProgresoLeccion

class ProgresoLeccionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProgresoLeccion
        fields = ['progreso', 'unidad_id']