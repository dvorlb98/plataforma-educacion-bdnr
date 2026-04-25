# Plataforma de Educación en Línea

Proyecto intermedio de **Bases de Datos No Relacionales** para modelar una plataforma educativa con responsabilidades separadas entre **MongoDB**, **Cassandra** y **Dgraph**.

**Curso:** P2026_ESI3891N  
**Profesor:** Omar Antonio Madriz Almanza  
**Handler de acceso de lectura:** HomerMadriz

## Integrantes

| Nombre | Expediente |
|---|---:|
| Manuel Alfonso Lopez Ponce De Leon | 753353 |
| Carlos Emiliano Olmedo Navarro | 754232 |
| Jorge Alberto Rivera Clemente | 760161 |
| Diego Saúl Castillo Fuentes | 754035 |

## Descripción del proyecto

Este proyecto modela una plataforma educativa donde estudiantes pueden registrarse, inscribirse a cursos, consultar materiales, avanzar por lecciones, presentar quizzes, entregar tareas, obtener certificados y recibir recomendaciones de cursos relacionados.

## Justificación del uso de bases de datos

### MongoDB
Se usa para almacenar documentos principales y relativamente estables: usuarios, perfiles, cursos, lecciones con materiales embebidos, inscripciones, quizzes, certificados y reseñas.

### Cassandra
Se usa para almacenar eventos históricos y temporales orientados a consulta por tiempo: sesiones de estudio, actividad diaria, intentos de quizzes, progreso por lección, eventos de video, entregas y notificaciones.

### Dgraph
Se usa para modelar relaciones entre entidades: alumno-curso, maestro-curso, curso-tarea, curso-prerrequisito, curso-categoría, curso-aula y recomendaciones por recorrido del grafo.

## Flujo de trabajo planeado

1. Se crean esquemas para cada base de datos.
2. Se generan datos de prueba en `data/`.
3. `populate.py` documenta (con comentarios) cómo poblar cada base.
4. `main.py` muestra un menú de consultas planeadas.
5. `connect.py` centraliza conexiones a MongoDB y Cassandra.

## Estructura del proyecto

```text
project-name/
├── Cassandra/
│   └── schema.cql
├── Mongo/
│   └── schema_indexes.js
├── Dgraph/
│   └── schema.graphql
├── data/
│   ├── users.json
│   ├── courses.json
│   ├── enrollments.json
│   ├── quizzes.json
│   ├── certificates.json
│   └── course_reviews.json
├── connect.py
├── populate.py
├── main.py
├── report.md
├── requirements.txt
└── README.md
```

## Requerimientos funcionales (30 corregidos)

| ID | BD | Requerimiento resumido | Resultado esperado |
|---|---|---|---|
| M01 | MongoDB | Crear/publicar curso | Documento `courses` + índices |
| M02 | MongoDB | Buscar/filtrar cursos | Text index + compuesto categoría/idioma |
| M03 | MongoDB | Progreso por lección en inscripción | `enrollments` con progreso |
| M04 | MongoDB | Materiales de apoyo | `lessons.attachments` embebidos |
| M05 | MongoDB | Registro de usuarios | `users` con índices únicos |
| M06 | MongoDB | Gestión de perfil | Subdocumento `profile` |
| M07 | MongoDB | Criterios de aprobación | `quizzes` con `passing_score` |
| M08 | MongoDB | Certificados por usuario | Consulta por `user_id` |
| M09 | MongoDB | Historial de cursos inscritos | Consulta por `user_id/status` |
| M10 | MongoDB | Reseñas/valoraciones | `course_reviews` e índices |
| C01 | Cassandra | Sesiones por estudiante | `sessions_by_student` |
| C02 | Cassandra | Progreso por lección en curso | `lesson_progress_by_student_course` |
| C03 | Cassandra | Intentos de quiz por estudiante | `quiz_attempts_by_student` |
| C04 | Cassandra | Intentos de quiz por curso | `quiz_attempts_by_student_course` |
| C05 | Cassandra | Actividad diaria por estudiante | `activity_by_student_day` |
| C06 | Cassandra | Eventos de video | `video_events_by_student` |
| C07 | Cassandra | Actividad reciente por curso/día | `activity_by_course_day` |
| C08 | Cassandra | Entregas de tareas | `submissions_by_student_course` |
| C09 | Cassandra | Progreso por curso/lección | `lesson_progress_by_course_lesson` |
| C10 | Cassandra | Notificaciones al estudiante | `notifications_by_student` |
| D01 | Dgraph | Alumno inscrito en curso | `inscrito_en` (+ facets) |
| D02 | Dgraph | Maestro imparte curso | `imparte` (+ facets) |
| D03 | Dgraph | Entrega de tareas | `entrega_tarea` (+ facets) |
| D04 | Dgraph | Exámenes realizados | `realiza_examen` (+ facets) |
| D05 | Dgraph | Curso contiene tareas | `contiene_tarea` (+ facets) |
| D06 | Dgraph | Consulta de calificaciones | Vía `entrega_tarea` y `realiza_examen` |
| D07 | Dgraph | Horario de curso | Atributos del nodo `Curso` |
| D08 | Dgraph | Recomendaciones | Traversal Alumno-Curso-Categoría |
| D09 | Dgraph | Prerrequisitos de cursos | `es_prerrequisito_de` |
| D10 | Dgraph | Aula asignada a curso | `se_imparte_en` |

### Correcciones del profesor aplicadas

- Calificaciones en Dgraph se consultan como atributos/facets, no como relación independiente.
- Horario en Dgraph se modela como atributo de `Curso`, no como entidad separada.
- Actividad temporal y asistencia se mueven a Cassandra.
- Recomendaciones se modelan en Dgraph, no en MongoDB.
- En Cassandra se reemplaza último acceso duplicado por actividad reciente por curso.
- En Cassandra se reemplaza monitoreo diario por progreso por curso/lección.
- En Cassandra se reemplazan hitos por notificaciones enviadas al estudiante.

## Consultas planeadas

### MongoDB
1. Buscar cursos por texto, categoría e idioma.
2. Ver perfil de estudiante.
3. Ver progreso de un estudiante en cursos.
4. Listar certificados de un usuario.
5. Ver reseñas de un curso.
6. Calcular promedio de rating por curso.

### Cassandra
1. Ver sesiones recientes de un estudiante.
2. Ver avance de un estudiante dentro de un curso.
3. Ver intentos recientes de quizzes.
4. Ver actividad diaria de un estudiante.
5. Ver actividad reciente de un curso.
6. Ver entregas recientes.
7. Ver notificaciones recientes.

### Dgraph
1. Ver cursos en los que está inscrito un alumno.
2. Ver qué maestro imparte un curso.
3. Ver tareas asociadas a un curso.
4. Ver tareas entregadas por un alumno.
5. Ver exámenes realizados por un alumno.
6. Consultar calificaciones mediante relaciones.
7. Ver prerrequisitos de un curso.
8. Recomendar cursos por relaciones.

## Instrucciones básicas de ejecución

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. (Opcional) Levantar contenedores con Docker Compose si se cuenta con un `docker-compose.yml` en el entorno.

3. Probar conexiones de infraestructura:

```bash
python connect.py
```

4. Ejecutar menú de consultas planeadas:

```bash
python main.py
```

> Nota: `populate.py` en esta entrega es un plan comentado de población y **no inserta datos** todavía.
