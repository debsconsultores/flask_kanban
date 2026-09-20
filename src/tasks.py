import time

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


@celery.task
def procesar_tarea(task_id):
    """
    Simula un procesamiento que requiere tiempo.
    """

    print(f"Iniciando procesamiento de la tarea {task_id}")

    # Simulamos un proceso que tarda algunos segundos.
    time.sleep(10)

    print(f"Procesamiento de la tarea {task_id} finalizado")

    return f"Tarea {task_id} procesada correctamente."