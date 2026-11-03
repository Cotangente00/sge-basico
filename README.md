# Sistema de Gestión de Estudiantes (SGE) básico

Aplicación por consola desarrollada en **Python** que permite gestionar una lista de estudiantes.

## Funcionalidades

1. **Agregar estudiante**: ID (único), nombre, programa académico y promedio (0.0 a 5.0).
2. **Mostrar lista de estudiantes**: en orden ascendente o descendente, con el total, los aprobados y el promedio general.
3. **Buscar estudiante por ID**: muestra el estudiante o un mensaje si no existe.
4. **Salir** del sistema.

## Conceptos aplicados

| Concepto | Dónde se aplica |
|---|---|
| Repetición condicionada al comienzo (`while`) | Ciclo del menú principal (`main`) |
| Decisión múltiple (`match-case`, equivalente a `switch`) | Selección de la opción del menú |
| Decisión simple y anidada (`if / elif / else`) | Validaciones, búsqueda, estado aprobado/reprobado |
| Repetición condicionada al final (`while True` + `break`) | Funciones de lectura de datos |
| Iteración ascendente y descendente (`for` + `range`) | Mostrar lista de estudiantes |
| Contador | `total_estudiantes`, `aprobados` |
| Acumulador (sumatoria) | `suma_promedios` |
| Bandera | `bandera_salir`, `encontrado` |
| Estructura de datos | Lista de diccionarios `estudiantes` |
| Manejo de errores | `try-except` en la lectura de datos |

## Requisitos

- Python **3.10 o superior** (por el uso de `match-case`).

## Cómo ejecutarlo

```bash
python sge.py
```

## Estructura del repositorio

```
├── sge.py          # Código fuente del sistema
├── README.md       # Este archivo
├── diagramas/      # Diagramas de flujo (principal y subprocesos)
└── evidencias/     # Capturas de pantalla de la ejecución
```
