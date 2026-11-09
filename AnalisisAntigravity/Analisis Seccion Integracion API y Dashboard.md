INFORME DE REVISIÓN TÉCNICA: DASHBOARD KANBAN
1. HALLAZGOS DE NIVEL CRÍTICO
Hallazgo C-1: Credenciales quemadas en el código (Hardcoded credentials) y auto-login forzado
Archivo: src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 429–444
Problema: El frontend ejecuta automáticamente una llamada a loginApi("test@test.com", "123456") cada vez que se carga la página, guardando el token resultante en sessionStorage.setItem("access_token", data.access_token).
Por qué puede ocurrir: Se implementó como un script de prueba o demostración durante el desarrollo para evitar autenticarse manualmente y quedó en el código fuente.
Impacto: Si un usuario real inicia sesión en Flask (current_user), el frontend sobrescribe su token y opera con la identidad de test@test.com. Si dicho usuario de prueba no existe en la base de datos o cambia su contraseña, el tablero no carga ninguna tarea. Supone además una fuga crítica de credenciales en el cliente.
Recomendación: Eliminar el auto-login en la plantilla. El JWT debe ser generado por el backend al momento del inicio de sesión web y transferido de manera segura (por ejemplo, inyectándolo en una variable de contexto segura o mediante cookies HttpOnly) o solicitando que el usuario ingrese sus credenciales.
Hallazgo C-2: Vulnerabilidad de Cross-Site Scripting (XSS Almacenado) en tarjetas Kanban
Archivo: src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 545–565
Problema: En la función createTaskCard(), el título y el contenido de la tarea se interpolan directamente dentro de article.innerHTML = usando ${task.title} y ${task.content ?? ""} sin ningún tipo de escape o sanitización.
Por qué puede ocurrir: Se utilizó una plantilla literal de JavaScript (template string) con innerHTML por rapidez para construir el nodo HTML de la tarjeta.
Impacto: Cualquier usuario que cree una tarea con contenido HTML/JavaScript malicioso (ej. <img src=x onerror=...> o <script>) provocará la ejecución arbitraria de código en el navegador de quien visualice el tablero, permitiendo el robo del JWT en sessionStorage.
Recomendación: Construir los nodos asignando contenido textual seguro mediante textContent o innerText, o aplicar una función de escape HTML antes de insertar los valores en innerHTML.
Hallazgo C-3: Referencia a variable inexistente data en deleteTask y updateTaskStatus (ReferenceError)
Archivo: src/main/templates/main/dahsboard.html y src/main/templates/main/dahsboard.html
Ubicación aproximada: Línea 686 y Línea 953
Problema:
En deleteTask: si !response.ok, se ejecuta showMessage(data.error || "Error al eliminar la tarea", "error");, pero la variable data nunca fue declarada ni leída (response.json() no fue invocado).
En updateTaskStatus: si !response.ok, se ejecuta showMessage(data.error || "Error al Actualizar el Estado", "error");, donde data tampoco existe.
Por qué puede ocurrir: Se copió el patrón de manejo de errores de otros bloques (como taskForm.submit) donde const data = await response.json(); sí había sido ejecutado previamente.
Impacto: Cuando el servidor responde con un código de error HTTP (por ejemplo, 401, 404 o 500), el navegador lanza una excepción Uncaught ReferenceError: data is not defined. Esto interrumpe la ejecución, no muestra el mensaje al usuario y deja la interfaz en un estado inconsistente.
Recomendación: Antes de evaluar data.error, parsear la respuesta con const data = await response.json().catch(() => ({})); o leer únicamente response.statusText.
Hallazgo C-4: Bloqueo de actualización y posible error 500 al editar tareas con descripción vacía
Archivo: src/api/routes.py
Ubicación aproximada: Líneas 200–208
Problema: En el endpoint PUT /api/v1/tasks/<task_id>, el backend valida:
python
if "content" in data:
    if not data["content"].strip():
        return error_response("El contenido no puede estar vacío", 400)
Sin embargo:
En el frontend (dahsboard.html línea 849), si el usuario deja el campo descripción vacío, envía content: "". Esto causa un error 400 Bad Request, impidiendo guardar o editar cualquier tarea sin descripción o borrar una descripción existente.
En schemas.py, content permite allow_none=True. Si el cliente envía content: null, la llamada a data["content"].strip() en Python lanza una excepción no controlada AttributeError: 'NoneType' object has no attribute 'strip', resultando en un error 500 Internal Server Error.
En models.py, content = db.Column(db.Text) es nullable.
Por qué puede ocurrir: Inconsistencia de criterio entre la creación (content opcional) y la edición (donde se intentó forzar que no fuera una cadena vacía de forma inconsistente con el modelo y el schema).
Impacto: Los usuarios no pueden editar tareas sin descripción ni borrar la descripción existente.
Recomendación: Permitir que content sea vacío o None, o verificar primero if data["content"] is not None: y respetar la opcionalidad definida en el modelo.
2. HALLAZGOS DE NIVEL IMPORTANTE
Hallazgo I-1: Typo en variable global no declarada para eliminación (taskToDeleted vs taskToDeleteId)
Archivo: src/main/templates/main/dahsboard.html y src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 644–646 y 1022–1039
Problema: En la línea 1022 se declara let taskToDeleted = null; (con d al final), pero en las líneas 644, 1025, 1033 y 1037 se usa taskToDeleteId (con Id al final).
Por qué puede ocurrir: Error tipográfico al declarar la variable de estado para el modal de eliminación.
Impacto: taskToDeleteId se crea implícitamente como una variable global en el objeto window (en modo no estricto). Si se llegara a usar 'use strict' o empaquetadores modernos, el código lanzaría ReferenceError: taskToDeleteId is not defined al intentar abrir el modal de eliminación. Además, la variable declarada taskToDeleted queda como código muerto.
Recomendación: Corregir la declaración a let taskToDeleteId = null; y ubicarla antes de los escuchadores de eventos.
Hallazgo I-2: Contenedores vacíos del Kanban impiden el evento "Drop" en columnas sin tareas
Archivo: src/main/templates/main/dahsboard.html y src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 314, 341, 365 y Líneas 971–986
Problema: En el DOM, los contenedores que escuchan el drop son: <div class="space-y-4" id="tasks-pending"></div>. No poseen una altura mínima (como min-h-[200px]). Si una columna no tiene tareas, su altura es de 0px. Además, el detector de eventos en JavaScript busca: event.target.closest("#tasks-pending, #tasks-in-progress, #tasks-completed"). Si el usuario suelta la tarjeta sobre el área de la columna (<section class="rounded-xl bg-gray-100 p-4">), closest() devuelve null porque <section> es el elemento padre del div, no hijo ni el elemento mismo.
Por qué puede ocurrir: Se vinculó el ID al div interno de tarjetas en lugar del elemento <section> de la columna completa, omitiendo dimensiones mínimas para el estado vacío.
Impacto: Si una columna queda vacía (o al inicio sin tareas), es físicamente imposible arrastrar y soltar una tarjeta dentro de ella.
Recomendación: Asignar una altura mínima a los contenedores (ej. min-h-[200px]) o vincular el id o atributos data-status directamente a la etiqueta <section> que cubre toda la columna.
Hallazgo I-3: update_task no verifica el borrado lógico (Task.delete_at.is_(None))
Archivo: src/api/routes.py
Ubicación aproximada: Líneas 179–186
Problema: Al consultar la tarea a modificar en update_task:
python
statement = select(Task).where(
    Task.id == task_id,
    Task.user_id == int(user_id)
)
No se incluye la condición Task.delete_at.is_(None).
Por qué puede ocurrir: Se omitió la condición que sí fue incluida correctamente en get_tasks.
Impacto: Si un cliente realiza un PUT /api/v1/tasks/<id> con el ID de una tarea previamente eliminada mediante soft-delete, la tarea se modifica en la base de datos sin retornar un error 404 Not Found. Lo mismo ocurre en delete_task, donde se puede volver a eliminar una tarea ya eliminada.
Recomendación: Agregar Task.delete_at.is_(None) al filtro del select() tanto en update_task como en delete_task.
Hallazgo I-4: Falta de comprobación de response.ok en loadTasks()
Archivo: src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 467–486
Problema: En loadTasks(), tras invocar fetch("/api/v1/tasks"), se ejecuta directamente:
javascript
tasks = await response.json();
...
tasks.forEach(task => { ... });
Por qué puede ocurrir: Se asumió que la promesa de fetch solo falla en errores de red.
Impacto: Si la API devuelve un código de error (ej. 401 Unauthorized por token vencido o inválido), tasks recibe un objeto de error (ej. {"code": 401, "message": "..."}) en lugar de un arreglo. Al llegar a tasks.forEach, se lanza una excepción TypeError: tasks.forEach is not a function.
Recomendación: Validar if (!response.ok) throw new Error(...) antes de procesar el JSON, y verificar que Array.isArray(tasks) sea verdadero.
Hallazgo I-5: Desconexión entre la sesión web (Flask-Login) y el JWT (SessionStorage)
Archivo: src/auth/routes.py y src/main/templates/main/dahsboard.html
Ubicación aproximada: auth/routes.py líneas 125–134; dahsboard.html línea 463
Problema: La ruta web /auth/dashboard está protegida por @login_required (cookie de sesión de Flask-Login), pero las llamadas al API usan JWT en Authorization: Bearer <token>. Al hacer /auth/logout, se destruye la sesión web en Flask, pero el JWT persiste indefinidamente en sessionStorage hasta que la pestaña del navegador se cierre por completo.
Por qué puede ocurrir: Coexistencia híbrida entre una aplicación web tradicional con vistas renderizadas por servidor y una API REST desacoplada que usa tokens sin una capa unificada de logout.
Impacto: Si otro usuario utiliza el mismo navegador y accede al dashboard, o si el usuario cierra sesión, el token anterior puede seguir siendo consumido por llamadas residuales en el frontend.
Recomendación: Implementar un script en la acción de logout para limpiar sessionStorage.removeItem("access_token") o migrar el token JWT a una cookie HttpOnly gestionada por el servidor.
3. HALLAZGOS DE NIVEL MEJORA
Hallazgo M-1: Contadores de resumen y cabeceras de columnas estáticos / hardcodeados
Archivo: src/main/templates/main/dahsboard.html y src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 255–286 y 307–362
Problema: Los contadores de resumen ("Pendientes: 2", "En progreso: 1", "Completadas: 1") y los badges numéricos de cada columna están escritos de forma estática en el HTML (2, 1, 1). El JavaScript no los actualiza al cargar, crear, mover o eliminar tareas.
Por qué puede ocurrir: Se maquetaron con valores de ejemplo en el diseño inicial y no se conectaron a las funciones de renderizado en JavaScript.
Recomendación: Asignar identificadores a estos elementos (ej. id="count-pending") y recalcular sus valores dinámicamente dentro de loadTasks().
Hallazgo M-2: Typo en clase CSS Tailwind para el botón Editar (text-blud-600)
Archivo: src/main/templates/main/dahsboard.html
Ubicación aproximada: Línea 530
Problema: En createTaskCard(), la clase aplicada al botón de edición es: editButton.className = "edit-task text-sm text-blud-600 hover:text-blue-800";
Por qué puede ocurrir: Error tipográfico (blud en lugar de blue).
Recomendación: Corregir a text-blue-600.
Hallazgo M-3: Nombre del archivo de plantilla con errata (dahsboard.html)
Archivo: src/main/templates/main/dahsboard.html y src/auth/routes.py
Ubicación aproximada: Nombre del archivo y línea 120 de src/auth/routes.py
Problema: El archivo se llama dahsboard.html (transposición de las letras 's' y 'h').
Por qué puede ocurrir: Typo al momento de crear el archivo original en el sistema de archivos.
Recomendación: Renombrar el archivo a dashboard.html y actualizar la referencia en render_template('main/dashboard.html').
Hallazgo M-4: Duplicación innecesaria de asignación de clases y botón de opciones inerte
Archivo: src/main/templates/main/dahsboard.html y src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 517–518, 541–542 y 552–558
Problema:
article.className se asigna dos veces consecutivas con el mismo valor dentro de createTaskCard().
Se renderiza un botón con el icono de opciones vertical ⋮, pero no posee ningún controlador de eventos, menú desplegable ni acción asociada.
Por qué puede ocurrir: Limpieza incompleta de código durante la iteración del maquetado.
Recomendación: Remover la asignación duplicada y dar funcionalidad o remover el botón ⋮.
Hallazgo M-5: Inconsistencia en validación de títulos con espacios en blanco entre Create y Update
Archivo: src/api/routes.py y src/api/routes.py
Ubicación aproximada: Líneas 128–140 frente a 195–198
Problema: En create_task, la validación de title que verificaba .strip() está comentada (líneas 131–134). Como TaskCreateSchema solo exige que title sea string (sin validate.Length(min=1)), se puede crear una tarea cuyo título sea una cadena de puros espacios "   ". En cambio, en update_task se rechaza explícitamente si not data["title"].strip().
Por qué puede ocurrir: Se confió exclusivamente en Marshmallow para la creación sin configurar validadores de longitud mínima en el schema.
Recomendación: Agregar validate=validate.Length(min=1) en TaskCreateSchema y TaskUpdateSchema.
Hallazgo M-6: Inconsistencia de serialización con Flask-Smorest en get_tasks
Archivo: src/api/routes.py
Ubicación aproximada: Líneas 39–65
Problema: La ruta @bp.route("/tasks") está decorada con @bp.response(200, tasks_schema). Sin embargo, dentro de la función se hace:
python
result = tasks_schema.dump(tasks)
return jsonify(result), 200
Mientras que en create_task y update_task se retorna directamente el objeto de modelo task y Smorest se encarga de serializarlo.
Por qué puede ocurrir: Refactorización a Flask-Smorest donde se actualizó create_task y update_task, pero se dejó la serialización manual antigua en get_tasks.
Recomendación: Mantener la homogeneidad retornando directamente return tasks para que Flask-Smorest aplique el schema.
Hallazgo M-7: Peticiones redundantes de diagnóstico al cargar la página
Archivo: src/main/templates/main/dahsboard.html
Ubicación aproximada: Líneas 376–402
Problema: Cada vez que el usuario ingresa al tablero se disparan dos peticiones HTTP adicionales (/api/v1/info y /api/v1/test) cuyos callbacks compiten por modificar el texto de apiStatus.
Por qué puede ocurrir: Se agregaron para verificar que la API estaba viva durante las pruebas iniciales.
Recomendación: Eliminar estas dos llamadas o unificarlas en una sola comprobación silenciosa.
4. ASPECTOS EVALUADOS COMO CORRECTOS
Aspecto OK-1: Convención y diseño de endpoints REST
Archivos: src/api/routes.py y src/main/templates/main/dahsboard.html
Evaluación: El diseño de los endpoints sigue las convenciones REST estándar:
GET /api/v1/tasks: Lista tareas.
POST /api/v1/tasks: Crea una tarea (responde 201).
PUT /api/v1/tasks/<id>: Actualiza atributos de la tarea (responde 200).
DELETE /api/v1/tasks/<id>: Borra la tarea (responde 200). El frontend consume las URLs y métodos HTTP exactos para cada operación.
Aspecto OK-2: Aislamiento por usuario autenticado (user_id)
Archivo: src/api/routes.py
Evaluación: Todos los endpoints protegidos obtienen la identidad desde el JWT (user_id = get_jwt_identity()) y aplican el filtro Task.user_id == int(user_id). Un usuario no puede leer, modificar ni eliminar tareas que pertenezcan a otro usuario.
Aspecto OK-3: Manejo de los tres estados del Kanban (pending, in_progress, completed)
Archivos: src/models.py, src/api/routes.py, src/main/templates/main/dahsboard.html
Evaluación: Hay consistencia exacta en la nomenclatura de los estados en la base de datos (default "pending"), en la validación del backend (allowed_statuses), en las opciones del <select> y en los contenedores del tablero Kanban (tasks-pending, tasks-in-progress, tasks-completed).
Aspecto OK-4: Prevención de duplicación de tarjetas en recargas
Archivo: src/main/templates/main/dahsboard.html
Evaluación: La función loadTasks() limpia explícitamente los contenedores (pendingContainer.innerHTML = "", etc.) antes de iterar sobre las tareas devueltas por la API, garantizando que tras crear, editar, mover o eliminar una tarea no se dupliquen las tarjetas existentes en el DOM.
Aspecto OK-5: Implementación del Soft-Delete
Archivos: src/models.py y src/api/routes.py
Evaluación: El borrado de tareas es lógico a través del método task.delete() del mixin SoftDeleteMixin, fijando delete_at, y get_tasks() filtra adecuadamente Task.delete_at.is_(None).
Aspecto OK-6: Asociación y propagación de identificadores de tareas
Archivo: src/main/templates/main/dahsboard.html
Evaluación: El ID numérico de cada tarea se asocia correctamente en los atributos de datos (article.dataset.taskId, button.dataset.taskId, select.dataset.taskId) y viaja como payload en event.dataTransfer.setData("text/plain", task.id) durante el arrastre, asegurando que las operaciones individuales apunten a la tarea correcta.
5. CONCLUSIÓN GENERAL
Coherencia entre Frontend, API y Modelo

Arquitectura y Modelo de Datos:
El modelo Task y los schemas de Marshmallow presentan una estructura sólida y bien pensada para el flujo básico (soft delete, asociación a usuario, estados bien definidos). Sin embargo, existe una incoherencia puntual en los campos opcionales: mientras el modelo y el schema de creación tratan el content (descripción) como opcional, el endpoint de actualización PUT lo trata de forma obligatoria y no nula, provocando fallas cuando el usuario edita una tarea con descripción vacía.

Seguridad e Integración de Autenticación:
La desconexión más crítica reside en el manejo de la autenticación: conviven dos esquemas (Flask-Login por sesión/cookie para servir la vista web y Flask-JWT-Extended para la API). Al no haberse implementado un puente seguro para proveer el JWT al usuario autenticado, se recurrió a un auto-login con credenciales hardcodeadas en JavaScript, lo cual compromete el aislamiento de datos entre usuarios. Sumado a esto, la interpolación no sanitizada de datos en innerHTML abre una vulnerabilidad de XSS Almacenado.

Interactividad del Frontend (Kanban y JavaScript):
El ciclo de vida del Kanban (distribución en 3 columnas, apertura de formularios modales, drag & drop y select de estados) está bien planteado en su flujo nominal. No obstante, adolece de errores de variables no declaradas o con nombres erróneos (data y taskToDeleteId) que romperán la ejecución al presentarse errores HTTP o al intentar eliminar tareas en entornos estrictos. Asimismo, el Drag & Drop presenta un defecto de usabilidad importante al no definir áreas de soltado con altura mínima cuando las columnas quedan desiertas.