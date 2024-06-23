from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

from ova.models import Actividad, Lecciones, Unidad, ProgresoLeccion
from usuario.models import Puntaje
from ova.utils import obtener_estructura
from .serializers import ProgresoLeccionSerializer



# Create your views here.
contents = obtener_estructura()

@login_required(login_url='/login')
def index(request):
    # montamos los contenidos del ova
    return render(request, 'index.html', {
        'contents': contents
    })

def lecciones(request):
    view = request.GET.get('view', None)
    progreso = list(ProgresoLeccion.objects.filter(usuario=request.user).values_list( 'progreso',flat=True))
    
    htmlTemplatesNames = {
        'video-intro': 'video-intro.html',
    }

    data = [{
            'sectionTitle': 'Video introduccion',
            'lessons': [
                {
                'label': 'Video introduccion',
                'url': 'video-intro',
                'index': -1,
                'progress': 100
            }
            ]
        }]
    
    i = 0
    for content in contents:
        data.append({
            'sectionTitle': content['title'],
            'lessons': []
        })
        for item in content['items']:
            htmlTemplatesNames[item['url']] = item['url'] + '.html'
            data[-1]['lessons'].append({
                'label': item['label'],
                'url': item['url'],
                'index': i,
                'progress': progreso[i] if i < len(progreso) else 0
            })
            i += 1

    return render(request, htmlTemplatesNames[view], {'secciones': data})

@csrf_exempt
def update_progress(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        progress = data.get('progress')
        index = data.get('progressIndex')

        lecciones = ProgresoLeccion.objects.filter(unidad_id=index, usuario=request.user)

        # # sino existe algun progreso para esa leccion, se crea uno nuevo
        if not lecciones.exists():
            ProgresoLeccion.objects.create(
                usuario=request.user,
                unidad_id=index,
                progreso=progress,
                completado=progress >= 80
            )
        else:
            leccion = lecciones.first()
            leccion.progreso = 100 if progress >= 60 else progress
            leccion.completado = progress >= 80
            leccion.save()

        # Aquí puedes guardar el progreso en la base de datos, por ejemplo, usando request.user para obtener el usuario actual
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

@csrf_exempt
def get_progress(request):
    if request.method == 'GET':
        lecciones = ProgresoLeccion.objects.filter(usuario=request.user)
        if lecciones.exists():
            serializer = ProgresoLeccionSerializer(lecciones, many=True)
            return JsonResponse({'status': 'success', 'progress': serializer.data})
        else:
            return JsonResponse({'status': 'success', 'progress': 0, 'completed': False})
    return JsonResponse({'status': 'failed'}, status=400)

def subirSumativa(request):
    if request.method == 'GET':
        score = request.GET.get('score')
        actividad = request.GET.get('actividad')
        print(score)
        if score is not None:
            try:
                score = int(score)
                usuario = request.user
                actividad = Actividad.objects.get(id=actividad)
                print(f'Debug: usuario={usuario}, score={score}, actividad_id={actividad}')
                puntajes = Puntaje.objects.filter(usuario=usuario, actividad=actividad)
                if puntajes.exists():
                    puntaje = puntajes.first()
                    puntaje.resultado = score
                    puntaje.is_sumativo = True  # Puedes ajustar este valor según sea necesario
                    puntaje.save()
                else:
                    nuevo_puntaje = Puntaje.objects.create(
                    usuario=usuario, 
                    actividad=actividad, 
                    resultado=score, 
                    is_sumativo=True  # Puedes ajustar este valor según sea necesario
                    )
                    nuevo_puntaje.save()
                print(f'Received score: {score}')
                return JsonResponse({'status': 'success', 'score': score})
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid score value'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'No score provided'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
def subirFormativa(request):
    if request.method == 'GET':
        score = request.GET.get('score') 
        actividad = request.GET.get('actividad')
        if score is not None:         
            score = int(score)
            usuario = request.user
            actividad = Actividad.objects.get(id=actividad)
            puntajes = Puntaje.objects.filter(usuario=usuario, actividad=actividad)
            if puntajes.exists():
                puntaje = puntajes.first()
                puntaje.resultado = score
                puntaje.is_sumativo = False
                print(puntaje.is_sumativo)
                print("aaaaaaaaaaa")
                puntaje.save()
            else:
                nuevo_puntaje = Puntaje.objects.create(
                    usuario=usuario, 
                    actividad=actividad, 
                    resultado=score, 
                    is_sumativo=False
                    )
                nuevo_puntaje.save()
                print(nuevo_puntaje.is_sumativo)
                print("aaaaaaaaaaaaaaaaaa")
            return JsonResponse({'status': 'success', 'score': score})
        else:
            return JsonResponse({'status': 'error', 'message': 'No score provided'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)