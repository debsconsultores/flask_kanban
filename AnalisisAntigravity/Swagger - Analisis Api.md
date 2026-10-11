Listed directory flask_kanban
Listed directory src
Listed directory api
Viewed routes.py:1-327
Viewed __init__.py:1-11
Viewed schemas.py:1-15
Viewed __init__.py:1-56
Viewed extensions.py:1-41
Viewed config.py:1-52
Viewed models.py:1-62
Listed directory tests
Viewed test_api.py:1-200
Viewed test_api.py:201-282
Searched for "@bp"
Searched for "jwt_required"
Viewed test_routes.py:1-34
Ran command: `pytest`

A continuación se presenta el informe detallado de revisión de la documentación OpenAPI (Flask-Smorest) en el archivo [src/api/routes.py](file:///d:/cursos/flask/flask_kanban/src/api/routes.py), centrado en los endpoints bajo `/api/v1/tasks`.

---

### 1. Resumen de Estado por Endpoint

| Endpoint | Método | `@jwt_required()` | `security=[{"bearerAuth": []}]` | Respuesta Exitosa Documentada | Errores 401 / 404 Documentados | Coherencia con Comportamiento Real |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| `/tasks` | `GET` | ✅ Sí | ✅ Sí | ✅ Sí (`200` con [tasks_schema](file:///d:/cursos/flask/flask_kanban/src/api/schemas.py#L15)) | ✅ 401 doc. / 404 N/A | **Coherente** |
| `/tasks` | `POST` | ✅ Sí | ✅ Sí | ✅ Sí (`201` con [task_schema](file:///d:/cursos/flask/flask_kanban/src/api/schemas.py#L14)) | ✅ 401 doc. / 404 N/A | ⚠️ **Descripción incorrecta** |
| `/tasks/<int:task_id>` | `PUT` | ✅ Sí | ✅ Sí | ❌ **No** (falta `@bp.response`) | ⚠️ 404 doc. / ❌ **401 no doc.** | ⚠️ **Incompleta** (falta 200, 401 y body) |
| `/tasks/<int:task_id>` | `DELETE` | ✅ Sí | ✅ Sí | ❌ **No** (falta `@bp.response`) | ⚠️ 404 doc. / ❌ **401 no doc.** | ⚠️ **Incompleta** (falta 200 y 401) |
| `/tasks/<int:task_id>/process` | `POST` | ❌ No | ❌ No | ❌ **No** (falta `@bp.response`) | ❌ No doc. | ⚠️ **Completamente indocumentado** |

---

### 2. Análisis Detallado por Endpoint

#### `GET /api/v1/tasks` — [get_tasks](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L27-L53)
* **Seguridad**: Cumple. Tiene `@jwt_required()` y está documentado con `security=[{"bearerAuth": []}]`. El esquema coincide con `bearerAuth` configurado en [config.py](file:///d:/cursos/flask/flask_kanban/config.py#L37).
* **Respuesta exitosa**: Cumple. Documentada con `@bp.response(200, tasks_schema)`.
* **Errores 401 / 404**:
  * `401`: Documentado correctamente con `@bp.alt_response(401, description="Token JWT ausente, inválido o expirado")`.
  * `404`: No aplica (la función devuelve un listado vacío `[]` con `200` si el usuario no tiene tareas activas).
* **Coherencia**: La descripción *"Obtiene las tareas del usuario autenticado"* y el esquema corresponden al comportamiento de la función.

---

#### `POST /api/v1/tasks` — [create_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L82-L131)
* **Seguridad**: Cumple. Protegido con `@jwt_required()` y documentado con `security=[{"bearerAuth": []}]`.
* **Respuesta exitosa**: Cumple. Documentada con `@bp.response(201, task_schema)`.
* **Errores 401 / 404**:
  * `401`: Documentado con `@bp.alt_response(401, description="Token JWT ausente, inválido o expirado")`.
  * `404`: No aplica (creación de recurso).
* **Inconsistencia detectada**:
  * **Descripción errónea**: En la línea 85 ([routes.py:L85](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L85)), `@bp.doc` declara `description="Obtiene las tareas del usuario autenticado."`, texto copiado de `get_tasks`. Debe describir la creación de una nueva tarea para el usuario autenticado.

---

#### `PUT /api/v1/tasks/<int:task_id>` — [update_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L133-L189)
* **Seguridad**: Cumple. Protegido con `@jwt_required()` y documentado con `security=[{"bearerAuth": []}]`.
* **Respuesta exitosa**: **Inconsistencia**.
  * La función retorna `return jsonify(result), 200` ([routes.py:L188](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L188)), pero **no tiene decorador `@bp.response(200, ...)`**. En Swagger UI / OpenAPI no aparece documentada la respuesta `200 OK` ni el esquema devuelto.
* **Errores 401 / 404**:
  * `404`: Cumple. Documentado con `@bp.alt_response(404, description="La tarea no existe o no pertenece al usuario autenticado.")`.
  * `401`: **Falta**. La función está protegida con `@jwt_required()`, por lo que devuelve `401` si el token es inválido o no se envía, pero no está documentado con `@bp.alt_response(401)`.
* **Inconsistencias adicionales**:
  * **Payload / Request Body no documentado**: A diferencia de `create_task` que usa `@bp.arguments(task_schema)`, `update_task` obtiene los datos directamente de `request.get_json()` sin documentar el esquema esperado del cuerpo de la petición.
  * **Errores 400**: La función devuelve `400` si el título o contenido son vacíos o de tipo incorrecto (líneas 169, 175, 178), pero no están reflejados en la documentación.

---

#### `DELETE /api/v1/tasks/<int:task_id>` — [delete_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L191-L226)
* **Seguridad**: Cumple. Protegido con `@jwt_required()` y documentado con `security=[{"bearerAuth": []}]`.
* **Respuesta exitosa**: **Inconsistencia**.
  * La función retorna `jsonify({"message": "Tarea eliminada correctamente"}), 200` ([routes.py:L223-L225](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L223-L225)), pero **carece de `@bp.response(200, ...)`**. En OpenAPI no figura la respuesta `200 OK`.
* **Errores 401 / 404**:
  * `404`: Cumple. Documentado con `@bp.alt_response(404, description="La tarea no existe o no pertenece al usuario autenticado.")`.
  * `401`: **Falta**. Al estar decorada con `@jwt_required()`, devuelve `401` si falla la autenticación, pero no tiene `@bp.alt_response(401)`.

---

#### `POST /api/v1/tasks/<int:task_id>/process` — [process_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L318-L327)
* **Documentación ausente**: Es una ruta perteneciente al prefijo `/tasks`, pero no cuenta con ninguna anotación de OpenAPI:
  * Sin `@bp.doc(...)`.
  * Sin `@bp.response(202, ...)` para la respuesta exitosa asíncrona (`202 Accepted`).
  * Sin documentación de parámetros de ruta (`task_id`).
* **Seguridad**: A diferencia de los otros endpoints de tareas, este endpoint no tiene `@jwt_required()`. En la documentación OpenAPI no figurará seguridad ni descripción.

---

### 3. Resumen de Mejoras de Documentación Sugeridas

1. **Ajustar la descripción en [create_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L84-L87)**:
   Cambiar `"Obtiene las tareas del usuario autenticado."` por `"Crea una nueva tarea para el usuario autenticado."`.

2. **Agregar `@bp.response(200, task_schema)` en [update_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L133)**:
   Permitirá documentar formalmente la respuesta `200 OK` y el esquema del recurso actualizado.

3. **Agregar `@bp.response(200, ...)` en [delete_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L191)**:
   Documentar la respuesta `200 OK` (por ejemplo con un esquema de mensaje o descripción del JSON resultante).

4. **Agregar `@bp.alt_response(401, description="Token JWT ausente, inválido o expirado")`**:
   Tanto en [update_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L133) como en [delete_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L191) para mantener paridad con los otros endpoints protegidos con `@jwt_required()`.

5. **Documentar el endpoint de procesamiento [process_task](file:///d:/cursos/flask/flask_kanban/src/api/routes.py#L318)**:
   Agregar `@bp.doc(description="Encola el procesamiento en segundo plano de una tarea.")` y `@bp.response(202, description="Procesamiento encolado")`.