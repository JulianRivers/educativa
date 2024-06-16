from django.shortcuts import render

# Create your views here.
# manejamos esto como una Base de Datos de contenidos
contents = [
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
            ],
            "ariaLabel": 'index-creational-patters'
        },
        {
            "title": 'Patrones Estrucutrales',
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
                }
            ]
        },
        {
            "title": 'Aplicación Práctica de Patrones de Diseño',
            "ariaLabel": 'index-practical-application',
            "items": [
                {
                    "label": 'Casos de estudio y ejemplos de aplicación',
                    "url": 'casos-de-estudio-y-ejemplos-de-aplicacion',
                },
                {
                    "label": 'Aspectos concretos del uso de patrones en POO',
                    "url": 'aspectos-concretos-del-uso-de-patrones-en-poo',
                },
                {
                    "label": 'Análisis de la necesidad y beneficios de su uso',
                    "url": 'analisis-de-la-necesidad-y-beneficios-de-su-uso',
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

    for content in contents:
        data.append({
            'sectionTitle': content['title'],
            'lessons': []
        })
        for item in content['items']:
            htmlTemplatesNames[item['url']] = item['url'] + '.html'
            data[-1]['lessons'].append({
                'label': item['label'],
                'url': item['url']
            })
    
   

    return render(request, htmlTemplatesNames[view], {'secciones': data})