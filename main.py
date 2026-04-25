"""Menú de consultas planeadas para la plataforma de educación en línea.

Este archivo NO ejecuta conexiones ni queries reales aún.
Solo muestra las consultas planeadas por base de datos.
"""


def show_menu() -> None:
    print("\n=== Plataforma de Educación en Línea ===")
    print("Seleccione una consulta planeada:\n")

    print("--- MongoDB ---")
    print(" 1. Buscar cursos por texto, categoría e idioma")
    print(" 2. Ver perfil de estudiante")
    print(" 3. Ver progreso de un estudiante en cursos")
    print(" 4. Listar certificados de un usuario")
    print(" 5. Ver reseñas de un curso")
    print(" 6. Calcular promedio de rating por curso")

    print("\n--- Cassandra ---")
    print(" 7. Ver sesiones recientes de un estudiante")
    print(" 8. Ver avance de un estudiante dentro de un curso")
    print(" 9. Ver intentos recientes de quizzes")
    print("10. Ver actividad diaria de un estudiante")
    print("11. Ver actividad reciente de un curso")
    print("12. Ver entregas recientes")
    print("13. Ver notificaciones recientes")

    print("\n--- Dgraph ---")
    print("14. Ver cursos en los que está inscrito un alumno")
    print("15. Ver qué maestro imparte un curso")
    print("16. Ver tareas asociadas a un curso")
    print("17. Ver tareas entregadas por un alumno")
    print("18. Ver exámenes realizados por un alumno")
    print("19. Consultar calificaciones mediante relaciones")
    print("20. Ver prerrequisitos de un curso")
    print("21. Recomendar cursos por relaciones")

    print("\n 0. Salir")


PLANNED_QUERIES = {
    "1": "Consulta planeada: Buscar cursos por texto, categoría e idioma (MongoDB).",
    "2": "Consulta planeada: Ver perfil de estudiante (MongoDB).",
    "3": "Consulta planeada: Ver progreso de un estudiante en cursos (MongoDB).",
    "4": "Consulta planeada: Listar certificados de un usuario (MongoDB).",
    "5": "Consulta planeada: Ver reseñas de un curso (MongoDB).",
    "6": "Consulta planeada: Calcular promedio de rating por curso (MongoDB).",
    "7": "Consulta planeada: Ver sesiones recientes de un estudiante (Cassandra).",
    "8": "Consulta planeada: Ver avance de un estudiante dentro de un curso (Cassandra).",
    "9": "Consulta planeada: Ver intentos recientes de quizzes (Cassandra).",
    "10": "Consulta planeada: Ver actividad diaria de un estudiante (Cassandra).",
    "11": "Consulta planeada: Ver actividad reciente de un curso (Cassandra).",
    "12": "Consulta planeada: Ver entregas recientes (Cassandra).",
    "13": "Consulta planeada: Ver notificaciones recientes (Cassandra).",
    "14": "Consulta planeada: Ver cursos en los que está inscrito un alumno (Dgraph).",
    "15": "Consulta planeada: Ver qué maestro imparte un curso (Dgraph).",
    "16": "Consulta planeada: Ver tareas asociadas a un curso (Dgraph).",
    "17": "Consulta planeada: Ver tareas entregadas por un alumno (Dgraph).",
    "18": "Consulta planeada: Ver exámenes realizados por un alumno (Dgraph).",
    "19": "Consulta planeada: Consultar calificaciones mediante relaciones (Dgraph).",
    "20": "Consulta planeada: Ver prerrequisitos de un curso (Dgraph).",
    "21": "Consulta planeada: Recomendar cursos por relaciones (Dgraph).",
}


def run_menu() -> None:
    while True:
        show_menu()
        option = input("\nIngresa una opción: ").strip()

        if option == "0":
            print("Saliendo del menú de consultas planeadas.")
            break

        message = PLANNED_QUERIES.get(option)
        if message:
            print(f"\n{message}")
        else:
            print("\nOpción inválida. Intenta nuevamente.")


if __name__ == "__main__":
    run_menu()
