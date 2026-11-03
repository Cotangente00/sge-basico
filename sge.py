# -*- coding: utf-8 -*-
"""
Sistema de Gestión de Estudiantes (SGE) básico
------------------------------------------------
Aplicación por consola que permite:
    1. Agregar estudiantes
    2. Mostrar la lista completa de estudiantes
    3. Buscar un estudiante por su ID
    4. Salir del sistema

Conceptos aplicados:
    - Sentencias de decisión simples, anidadas y múltiples (if / elif / match-case)
    - Sentencias de repetición (while, for) ascendentes y descendentes
    - Variables especiales: contador, acumulador (sumatoria) y bandera
    - Estructura de datos simple: lista de diccionarios
    - Funciones (unidades de código reutilizables)
    - Validación de entradas con try-except

Requiere Python 3.10 o superior (por el uso de match-case).
"""

# ---------------------------------------------------------------
# Constantes del sistema
# ---------------------------------------------------------------
# Aunque las listas de Python crecen solas, se pone un límite para
# controlar el tamaño del registro, como se haría con un arreglo.
MAX_ESTUDIANTES = 50
NOTA_MINIMA = 0.0
NOTA_MAXIMA = 5.0   # Escala de calificación usada en Colombia


# ---------------------------------------------------------------
# Funciones de lectura y validación de datos
# ---------------------------------------------------------------
def leer_entero(mensaje, minimo=None, maximo=None):
    """Pide un número entero y repite la pregunta hasta que sea válido.

    Se usa 'while True' + 'break' para simular una repetición
    condicionada al final (do-while): la pregunta se hace al menos
    una vez y se repite solo si el dato es incorrecto.
    """
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            # Si el usuario escribe letras o deja vacío, int() falla
            print("   [!] Debe ingresar un número entero. Intente de nuevo.")
            continue

        # Decisiones simples para revisar el rango permitido
        if minimo is not None and numero < minimo:
            print(f"   [!] El número debe ser mayor o igual a {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"   [!] El número debe ser menor o igual a {maximo}.")
        else:
            break   # Dato correcto: termina el ciclo
    return numero


def leer_decimal(mensaje, minimo, maximo):
    """Pide un número decimal dentro de un rango (por ejemplo una nota)."""
    while True:
        # Se acepta coma o punto como separador decimal (ej. 4,5 o 4.5)
        texto = input(mensaje).strip().replace(",", ".")
        try:
            numero = float(texto)
        except ValueError:
            print("   [!] Debe ingresar un número (ejemplo: 4.2). Intente de nuevo.")
            continue

        if numero < minimo or numero > maximo:
            print(f"   [!] El valor debe estar entre {minimo} y {maximo}.")
        else:
            break
    return numero


def leer_texto(mensaje):
    """Pide un texto que no esté vacío ni sea solo números."""
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("   [!] Este campo no puede quedar vacío.")
        elif texto.replace(" ", "").isdigit():
            print("   [!] Este campo no puede contener solo números.")
        else:
            break
    return texto


def formatear_texto(texto):
    """Pone en mayúscula la primera letra de cada palabra, excepto
    conectores cortos (de, del, la, y...). Ej: 'ingeniería de software'
    -> 'Ingeniería de Software'."""
    conectores = ["de", "del", "la", "las", "los", "y", "en", "e"]
    palabras = texto.lower().split()
    resultado = []
    for i in range(len(palabras)):
        # La primera palabra siempre va en mayúscula
        if i > 0 and palabras[i] in conectores:
            resultado.append(palabras[i])
        else:
            resultado.append(palabras[i].capitalize())
    return " ".join(resultado)


# ---------------------------------------------------------------
# Funciones de búsqueda y presentación
# ---------------------------------------------------------------
def buscar_posicion(estudiantes, id_buscado):
    """Búsqueda lineal: recorre la lista y devuelve la posición del
    estudiante con ese ID, o -1 si no existe.

    Se usa una bandera ('encontrado') para detener el ciclo apenas
    se encuentra el estudiante y no seguir recorriendo sin necesidad.
    """
    encontrado = False      # Bandera
    posicion = -1
    i = 0
    while i < len(estudiantes) and not encontrado:
        if estudiantes[i]["id"] == id_buscado:
            encontrado = True
            posicion = i
        i += 1
    return posicion


def mostrar_estudiante(estudiante):
    """Imprime los datos de UN estudiante en una sola línea con formato."""
    # Decisión simple para indicar si el promedio es aprobatorio
    if estudiante["promedio"] >= 3.0:
        estado = "Aprobado"
    else:
        estado = "Reprobado"
    # Se recortan los textos largos para que la tabla no se desalinee
    nombre = estudiante["nombre"][:22]
    programa = estudiante["programa"][:26]
    print(f"   {estudiante['id']:<8} {nombre:<22} "
          f"{programa:<26} {estudiante['promedio']:>4.1f}   {estado}")


def imprimir_encabezado_tabla():
    print(f"   {'ID':<8} {'NOMBRE':<22} {'PROGRAMA':<26} {'PROM.':>5}  ESTADO")
    print("   " + "-" * 75)


# ---------------------------------------------------------------
# Funciones de cada opción del menú
# ---------------------------------------------------------------
def agregar_estudiante(estudiantes, total_estudiantes):
    """Agrega un estudiante nuevo a la lista y devuelve el contador
    actualizado."""
    print("\n--- AGREGAR ESTUDIANTE ---")

    # Decisión simple: no superar el tamaño máximo definido
    if total_estudiantes >= MAX_ESTUDIANTES:
        print(f"   [!] No se pueden registrar más de {MAX_ESTUDIANTES} estudiantes.")
        return total_estudiantes

    # El ID debe ser único: se repite la pregunta mientras ya exista
    id_estudiante = leer_entero("   ID del estudiante (número): ", minimo=1)
    while buscar_posicion(estudiantes, id_estudiante) != -1:
        print(f"   [!] Ya existe un estudiante con el ID {id_estudiante}.")
        id_estudiante = leer_entero("   Ingrese otro ID: ", minimo=1)

    nombre = leer_texto("   Nombre completo: ")
    programa = leer_texto("   Programa académico: ")
    promedio = leer_decimal(f"   Promedio ({NOTA_MINIMA} a {NOTA_MAXIMA}): ",
                            NOTA_MINIMA, NOTA_MAXIMA)

    # Cada estudiante se guarda como un diccionario dentro de la lista
    estudiante = {
        "id": id_estudiante,
        "nombre": formatear_texto(nombre),
        "programa": formatear_texto(programa),
        "promedio": promedio,
    }
    estudiantes.append(estudiante)

    total_estudiantes += 1      # Contador: un estudiante más
    print(f"\n   Estudiante agregado correctamente. "
          f"Total registrados: {total_estudiantes}")
    return total_estudiantes


def mostrar_estudiantes(estudiantes, total_estudiantes):
    """Muestra todos los estudiantes en el orden que el usuario elija
    y calcula el promedio general del grupo."""
    print("\n--- LISTA DE ESTUDIANTES ---")

    # Decisión simple: si la lista está vacía no hay nada que mostrar
    if total_estudiantes == 0:
        print("   No hay estudiantes registrados todavía.")
        return

    print("   1. Del primero al último registrado")
    print("   2. Del último al primero registrado")
    orden = leer_entero("   Seleccione el orden: ", minimo=1, maximo=2)
    print()
    imprimir_encabezado_tabla()

    suma_promedios = 0.0    # Acumulador (sumatoria)
    aprobados = 0           # Contador de aprobados

    if orden == 1:
        # Iteración ASCENDENTE: posiciones 0, 1, 2, ..., n-1
        for i in range(0, total_estudiantes):
            mostrar_estudiante(estudiantes[i])
            suma_promedios += estudiantes[i]["promedio"]
            if estudiantes[i]["promedio"] >= 3.0:
                aprobados += 1
    else:
        # Iteración DESCENDENTE: posiciones n-1, n-2, ..., 0
        for i in range(total_estudiantes - 1, -1, -1):
            mostrar_estudiante(estudiantes[i])
            suma_promedios += estudiantes[i]["promedio"]
            if estudiantes[i]["promedio"] >= 3.0:
                aprobados += 1

    promedio_general = suma_promedios / total_estudiantes
    print("   " + "-" * 75)
    print(f"   Total de estudiantes: {total_estudiantes}   |   "
          f"Aprobados: {aprobados}   |   Promedio general: {promedio_general:.2f}")


def buscar_estudiante(estudiantes, total_estudiantes):
    """Pide un ID y muestra el estudiante si existe."""
    print("\n--- BUSCAR ESTUDIANTE POR ID ---")

    if total_estudiantes == 0:
        print("   No hay estudiantes registrados para buscar.")
        return

    id_buscado = leer_entero("   Ingrese el ID a buscar: ", minimo=1)
    posicion = buscar_posicion(estudiantes, id_buscado)

    # Decisión simple: ¿se encontró o no el estudiante?
    if posicion != -1:
        print("\n   Estudiante encontrado:\n")
        imprimir_encabezado_tabla()
        mostrar_estudiante(estudiantes[posicion])
    else:
        print(f"   [!] No existe ningún estudiante con el ID {id_buscado}.")


def mostrar_menu():
    print("\n==============================================")
    print("   SISTEMA DE GESTIÓN DE ESTUDIANTES (SGE)")
    print("==============================================")
    print("   1. Agregar estudiante")
    print("   2. Mostrar lista de estudiantes")
    print("   3. Buscar estudiante por ID")
    print("   4. Salir")
    print("----------------------------------------------")


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------
def main():
    estudiantes = []            # Lista donde se guardan los estudiantes
    total_estudiantes = 0       # Contador de estudiantes registrados
    bandera_salir = False       # Bandera que controla el ciclo del menú

    # Repetición condicionada al comienzo: el menú se repite
    # mientras el usuario NO haya elegido salir.
    while not bandera_salir:
        mostrar_menu()
        opcion = leer_entero("   Seleccione una opción (1-4): ")

        # Decisión múltiple: dirige el programa a la opción elegida
        match opcion:
            case 1:
                total_estudiantes = agregar_estudiante(estudiantes, total_estudiantes)
            case 2:
                mostrar_estudiantes(estudiantes, total_estudiantes)
            case 3:
                buscar_estudiante(estudiantes, total_estudiantes)
            case 4:
                bandera_salir = True    # Se activa la bandera: termina el ciclo
            case _:
                print("   [!] Opción no válida. Elija un número del 1 al 4.")

    print(f"\n   Saliendo del sistema... Se registraron {total_estudiantes} "
          f"estudiante(s) en esta sesión. ¡Hasta pronto!\n")


# Punto de entrada del programa
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Si el usuario cierra con Ctrl+C o se acaba la entrada,
        # el programa termina sin mostrar un error feo.
        print("\n\n   Programa interrumpido por el usuario. ¡Hasta pronto!\n")
