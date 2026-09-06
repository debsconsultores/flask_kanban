from src.extensions import celery


@celery.task
def saludar(nombre):
    mensaje = f"Hola {nombre}, esta tarea fue ejecutad por Celery"

    print(mensaje)

    return mensaje
