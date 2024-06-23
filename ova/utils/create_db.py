from ova.models import Actividad, Lecciones,Unidad

# contenidos de la base de datos y del ova
CONTENTS = [
        {
            "title": 'Conceptos fundamentales',
            "items": [
                {
                    "label": '¿Qué es un patrón de diseño?',
                    "url": 'que-es-un-patron-de-diseno',
                    "sumativa": False
                },
                {
                    "label": 'Importancia y aplicación ',
                    "url": 'importancia-y-aplicacion',
                    "sumativa": False
                },
                {
                    "label": 'Componentes esenciales de un patrón de diseño',
                    "url": 'componentes-esenciales-de-un-patron-de-diseno',
                    "sumativa": False
                },
                {
                    "label": 'Examen de Conceptos Fundamentales',
                    "url": 'examen-de-conceptos-fundamentales',
                    "sumativa": True
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
                    "sumativa": False
                },
                {
                    "label": 'Abstract Factory',
                    "url": 'abstract-factory',
                    "sumativa": False
                },
                {
                    "label": 'Builder',
                    "url": 'builder',
                    "sumativa": False
                },
                {
                    "label": 'Prototype',
                    "url": 'protoype',
                    "sumativa": False
                },
                {
                    "label": 'Singleton',
                    "url": 'singleton',
                    "sumativa": False
                },
                {
                    "label": 'Examen de Patrones Creacionales',
                    "url": 'examen-de-patrones-creacionales',
                    "sumativa": True
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
                    "sumativa": False
                },
                {
                    "label": 'Bridge',
                    "url": 'bridge',
                    "sumativa": False
                },
                {
                    "label": 'Decorator',
                    "url": 'decorator',
                    "sumativa": False
                },
                {
                    "label": 'Facade',
                    "url": 'facade',
                    "sumativa": False
                },
                {
                    "label": 'Examen de Patrones Estructurales',
                    "url": 'examen-de-patrones-estructurales',
                    "sumativa": True
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
                    "sumativa": False
                },
                {
                    "label": 'Observer',
                    "url": 'observer',
                    "sumativa": False
                },
                {
                    "label": 'Strategy',
                    "url": 'strategy',
                    "sumativa": False
                },
                {
                    "label": 'Examen de Patrones de Comportamiento',
                    "url": 'examen-de-patrones-de-comportamiento',
                    "sumativa": True
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
                    "sumativa": False
                },
                {
                    "label": 'Casos de estudio y ejemplos de aplicación',
                    "url": 'casos-de-estudio-y-ejemplos-de-aplicacion',
                    "sumativa": False
                },
                {
                    "label": 'Aspectos concretos del uso de patrones en POO',
                    "url": 'aspectos-concretos-del-uso-de-patrones-en-poo',
                    "sumativa": False
                },
                {
                    "label": 'Examen de Aplicaciones Prácticas de Patrones de Diseño',
                    "url": 'examen-de-aplicaciones-practicas-de-patrones',
                    "sumativa": True
                }
            ]
        }
    ]

def createDB():
    # Crear primero las unidades
    # Crear segundo las lecciones
    # Crear tercero las actividades

    # borramos todo primero
    Actividad.objects.all().delete()
    Lecciones.objects.all().delete()
    Unidad.objects.all().delete()

    unidades = []
    lecciones = []
    actividades = []

    print("Creando la base de datos...")

    for content in CONTENTS:
        # agreamos las unidades a la lista
        unidades.append(
            Unidad(
                titulo=content['title'],
                ariaLabel=content['ariaLabel']
            )
        )    
    
    print("Creando las unidades...")
    # con bulk_create podemos crear varios registros a la vez
    unidades = Unidad.objects.bulk_create(unidades)
    print("Unidades creadas exitosamente...")

    
    # creamos las lecciones
    for index, content in enumerate(CONTENTS):
        unidad = unidades[index]
        for item in content['items']:
            lecciones.append(
                Lecciones(
                    titulo=item['label'],
                    link=item['url'],
                    template=item['url'] + '.html',
                    unidad=unidad
                )
            )
    
    print("Creando las lecciones...")
    lecciones = Lecciones.objects.bulk_create(lecciones)
    print("Lecciones creadas exitosamente...")

    # creamos las actividades
    for content in CONTENTS:
        for index, item in enumerate(content['items']):
            leccion = lecciones[index]
            actividades.append(
                Actividad(
                    titulo=item['label'],
                    leccion=leccion,
                    is_sumativo=item['sumativa']
                )
            )
    
    print("Creando las actividades...")
    actividades = Actividad.objects.bulk_create(actividades)
    print("Actividades creadas exitosamente...")

    print("Base de datos creada exitosamente 😊...")


    