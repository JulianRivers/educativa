from django.db.models import Prefetch
from ova.models import Unidad, Lecciones

def obtener_estructura():
    # Realizar una sola consulta que obtenga todas las unidades con sus lecciones
    unidades = Unidad.objects.prefetch_related(
        Prefetch('lecciones', queryset=Lecciones.objects.all(), to_attr='lecciones_list')
    ).all()

    # Procesar los resultados para crear la estructura deseada
    estructura = []
    i=0
    for unidad in unidades:
        unidad_dict = {
            "title": unidad.titulo,
            "items": [
                {
                    "label": leccion.titulo,
                    "url": leccion.link,
                    "i": i + index,
                }
                for index, leccion in enumerate(unidad.lecciones_list)
            ],
            "ariaLabel": unidad.ariaLabel or f"index-{unidad.titulo.lower().replace(' ', '-')}"
        }
        i += len(unidad.lecciones_list)
        estructura.append(unidad_dict)

    return estructura