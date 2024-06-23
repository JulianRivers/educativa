from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from ova.models import Actividad
from usuario.models import Puntaje

# Create your views here.
# manejamos esto como una Base de Datos de contenidos
contents = [
        {
            "title": 'Introducción a los patrones de diseño',
            "items": [
                {
                    "label":'Video Introductorio',
                    "url": 'video-intro',
                }
            ],
            "ariaLabel": "index-introduction"
        },
        {
            "title": 'Conceptos fundamentales',
            "items": [
                {
                    "label": '¿Qué es un patrón de diseño?',
                    "url": 'que-es-un-patron-de-diseno',
                },
                {
                    "label": 'Importancia y aplicación ',
                    "url": 'importancia-y-aplicacion',
                },
                {
                    "label": 'Componentes esenciales de un patrón de diseño',
                    "url": 'componentes-esenciales-de-un-patron-de-diseno',
                },
                {
                    "label": 'Examen de Conceptos Fundamentales',
                    "url": 'examen-de-conceptos-fundamentales',
                }
                
            ],
            "ariaLabel": 'index-fundamentals'
        },
        {
            "title": 'Patrones creacionales',
            "items": [
                {
                    "label": 'Factory Method',
                    "url": 'factory-method',
                },
                {
                    "label": 'Abstract Factory',
                    "url": 'abstract-factory',
                },
                {
                    "label": 'Builder',
                    "url": 'builder',
                },
                {
                    "label": 'Prototype',
                    "url": 'protoype',
                },
                {
                    "label": 'Singleton',
                    "url": 'singleton',
                },
                {
                    "label": 'Examen de Patrones Creacionales',
                    "url": 'examen-de-patrones-creacionales',
                }
            ],
            "ariaLabel": 'index-creational-patters'
        },
        {
            "title": 'Patrones Estructurales',
            "ariaLabel": 'index-structural-patters',
            "items": [
                {
                    "label": 'Adapter',
                    "url": 'adpter',
                },
                {
                    "label": 'Bridge',
                    "url": 'bridge',
                },
                {
                    "label": 'Decorator',
                    "url": 'decorator',
                },
                {
                    "label": 'Facade',
                    "url": 'facade',
                },
                {
                    "label": 'Examen de Patrones Estructurales',
                    "url": 'examen-de-patrones-estructurales',
                }
            ]
        },
        {
            "title": 'Patrones de comportamiento',
            "ariaLabel": 'index-behavioral-patters',
            "items": [
                {
                    "label": 'Iterator',
                    "url": 'iterator',
                },
                {
                    "label": 'Observer',
                    "url": 'observer',
                },
                {
                    "label": 'Strategy',
                    "url": 'strategy',
                },
                {
                    "label": 'Examen de Patrones de Comportamiento',
                    "url": 'examen-de-patrones-de-comportamiento',
                }
            ]
        },
        {
            "title": 'Aplicación Práctica de Patrones de Diseño',
            "ariaLabel": 'index-practical-application',
            "items": [
                {
                    "label": 'Análisis de la necesidad y beneficios de su uso',
                    "url": 'analisis-de-la-necesidad-y-beneficios-de-su-uso',
                },
                {
                    "label": 'Casos de estudio y ejemplos de aplicación',
                    "url": 'casos-de-estudio-y-ejemplos-de-aplicacion',
                },
                {
                    "label": 'Aspectos concretos del uso de patrones en POO',
                    "url": 'aspectos-concretos-del-uso-de-patrones-en-poo',
                },
                {
                    "label": 'Examen de Aplicaciones Prácticas de Patrones de Diseño',
                    "url": 'examen-de-aplicaciones-practicas-de-patrones',
                }
            ]
        }
    ]

def index(request):
    # montamos los contenidos del ova
    
    return render(request, 'index.html', {
        'contents': contents
    })

def lecciones(request):
    view = request.GET.get('view', None)
    
    htmlTemplatesNames = {}
    data = []
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
                'index': i
            })
            i += 1
    
    return render(request, htmlTemplatesNames[view], {'secciones': data})

@csrf_exempt
def update_progress(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        progress = data.get('progress')
        # Aquí puedes guardar el progreso en la base de datos, por ejemplo, usando request.user para obtener el usuario actual
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)

def subirSumativa(request):
    if request.method == 'GET':
        score = request.GET.get('score')
        actividad = request.GET.get('actividad')
        print(actividad)
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
            try:
                score = int(score)
                usuario = request.user
                nuevo_puntaje = Puntaje.objects.create(
                    usuario=usuario, 
                    actividad=actividad, 
                    resultado=score, 
                    is_sumativo=False  # Puedes ajustar este valor según sea necesario
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