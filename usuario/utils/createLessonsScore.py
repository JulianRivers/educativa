from ova.models import ProgresoLeccion, Lecciones

def createLessonScore(user):
    lecciones = Lecciones.objects.all()
    for leccion in lecciones:
        ProgresoLeccion.objects.create(
            usuario=user,
            unidad=leccion
        )