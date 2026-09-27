import time

from src.extensions import celery, db
from src.models import Task


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
    time.sleep(30)

    print(f"Procesamiento de la tarea {task_id} finalizado")

    return f"Tarea {task_id} procesada correctamente."


@celery.task
def tarea_con_error():
    """
    Tarea utilizada para comprobar el manejo
    de errores en Celery.
    """

    print("Iniciando tarea con error...")

    # Provocamos intencionalmente una excepción.
    raise ValueError("Se produjo un error de prueba.")


@celery.task
def dividir(a, b):
    """
    Divide dos números.

    Permite comprobar los estados
    SUCCESS y FAILURE.
    """

    resultado = a / b

    print(f"Resultado: {resultado}")

    return resultado


@celery.task
def procesar_task(task_id):
    """
    Procesa una tarea del Kanban de forma asíncrona.
    """

    # Buscamos la tarea utilizando SQLAlchemy 2.x.
    task = db.session.get(Task, task_id)

    # Si no existe, informamos del problema.
    if not task:
        raise ValueError(f"La tarea {task_id} no existe.")

    print(f"Procesando tarea: {task.title}")

    # Aquí podremos incorporar posteriormente
    # procesos más complejos.

    return {
        "task_id": task.id,
        "title": task.title,
        "message": "Tarea procesada correctamente."
    }