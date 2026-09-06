from src.extensions import celery


@celery.task
def saludar(nombre):
    mensaje = f"Hola {nombre}, esta tarea fue ejecutad por Celery"

    print(mensaje)

    return mensaje


@celery.task
def sumar(a, b):
    resultado = a + b

    mensaje = f"La suma es: {resultado}"

    print(mensaje)
    return mensaje