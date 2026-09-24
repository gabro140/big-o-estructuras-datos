"""
Laboratorio: GitHub + Big O + Estructuras de Datos
--------------------------------------------------
Descarga el CSV de estudiantes desde la URL RAW de GitHub y compara la
MISMA operación (buscar un carnet) en: List, Set, Dict, Lista enlazada y BST.

Uso:
    python src/main.py            -> descarga desde la URL RAW (modo oficial)
    python src/main.py --local    -> usa data/estudiantes.csv (solo para pruebas sin Internet)

Al terminar actualiza automáticamente:
    resultados/mediciones.md      -> todas las tablas de esta ejecución
    resultados/resultados.md      -> la tabla principal (entre las marcas TABLA)
"""
import csv
import io
import platform
import random
import sys
import time
import urllib.request
from datetime import datetime
from math import log2
from pathlib import Path

from arbol_bst import ArbolBST
from lista_enlazada import ListaEnlazada

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
# Pegue aquí la URL RAW del CSV alojado en GitHub.
URL = "https://raw.githubusercontent.com/gabro140/big-o-estructuras-datos/main/data/estudiantes.csv"

CARNET_BUSCAR = "EST099999"        # último carnet del dataset (peor caso para búsqueda lineal)
CARNET_INEXISTENTE = "EST999999"   # reto del paso 9
TAMANOS = [100, 1_000, 10_000, 50_000, 100_000]
SEMILLA = 2026                     # para que el shuffle del BST sea reproducible

# Repeticiones: las operaciones O(1) son tan rápidas que se necesitan muchas
# repeticiones para que el reloj pueda medirlas; las O(n) son más lentas.
REP_LINEAL = 100
REP_RAPIDA = 10_000

BASE = Path(__file__).resolve().parent.parent
CSV_LOCAL = BASE / "data" / "estudiantes.csv"
RESULTADOS = BASE / "resultados" / "resultados.md"
MEDICIONES = BASE / "resultados" / "mediciones.md"


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------
def descargar_datos(url):
    if "PEGAR_AQUI" in url:
        raise ValueError("Debe reemplazar URL por la dirección RAW de GitHub.")

    with urllib.request.urlopen(url) as respuesta:
        contenido = respuesta.read().decode("utf-8")

    return list(csv.DictReader(io.StringIO(contenido)))


def leer_local(ruta):
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


# ---------------------------------------------------------------------------
# Búsqueda y medición
# ---------------------------------------------------------------------------
def buscar_lista(estudiantes, carnet):
    """Búsqueda secuencial: O(n)."""
    for estudiante in estudiantes:
        if estudiante["carnet"] == carnet:
            return estudiante
    return None


def medir(funcion, repeticiones=100):
    """Tiempo PROMEDIO (segundos) de una llamada a `funcion`.

    Se mide el bloque completo de repeticiones con time.perf_counter() y se
    divide entre la cantidad; así el costo del propio reloj no domina en las
    operaciones O(1).
    """
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        funcion()
    return (time.perf_counter() - inicio) / repeticiones


def medir_una_vez(funcion):
    inicio = time.perf_counter()
    resultado = funcion()
    return time.perf_counter() - inicio, resultado


def construir_lista_enlazada(registros):
    """Inserta al inicio recorriendo al revés, para que la lista enlazada quede
    en el MISMO orden que la List (el último carnet queda al final). Así ambas
    estructuras resuelven exactamente la misma consulta en igualdad de condiciones."""
    lista = ListaEnlazada()
    for estudiante in reversed(registros):
        lista.insertar_inicio(estudiante)
    return lista


def construir_bst(registros, mezclar=True):
    datos = list(registros)
    if mezclar:
        random.Random(SEMILLA).shuffle(datos)
    arbol = ArbolBST()
    for estudiante in datos:
        arbol.insertar(estudiante)
    return arbol


def us(segundos):
    """Segundos -> microsegundos con formato."""
    return f"{segundos * 1_000_000:,.3f}"


def tabla_md(encabezados, filas, alinear_derecha=True):
    sep = "|" + "|".join(("---:" if alinear_derecha else "---") for _ in encabezados) + "|"
    lineas = ["| " + " | ".join(encabezados) + " |", sep]
    lineas += ["| " + " | ".join(str(c) for c in fila) + " |" for fila in filas]
    return "\n".join(lineas)


def imprimir_tabla(encabezados, filas):
    anchos = [max(len(str(x)) for x in [h] + [f[i] for f in filas]) for i, h in enumerate(encabezados)]
    print("  " + "  ".join(str(h).rjust(a) for h, a in zip(encabezados, anchos)))
    print("  " + "  ".join("-" * a for a in anchos))
    for f in filas:
        print("  " + "  ".join(str(c).rjust(a) for c, a in zip(f, anchos)))


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main():
    modo_local = "--local" in sys.argv
    secciones_md = []

    # 1) Descarga ----------------------------------------------------------
    if modo_local:
        print(f"1) MODO LOCAL (solo pruebas): leyendo {CSV_LOCAL}")
        estudiantes = leer_local(CSV_LOCAL)
        origen = f"archivo local {CSV_LOCAL.name} (modo prueba)"
    else:
        print("1) Descargando datos desde GitHub...")
        estudiantes = descargar_datos(URL)
        origen = URL
    print(f"   OK: {len(estudiantes):,} registros recibidos")

    # 2) Construcción (costo de construcción, separado del de consulta) -----
    print("\n2) Construyendo estructuras (costo de CONSTRUCCIÓN)...")
    t_c_list, _ = medir_una_vez(lambda: list(estudiantes))
    t_c_set, carnets_set = medir_una_vez(lambda: {e["carnet"] for e in estudiantes})
    t_c_dict, estudiantes_dict = medir_una_vez(lambda: {e["carnet"]: e for e in estudiantes})
    t_c_le, lista_enlazada = medir_una_vez(lambda: construir_lista_enlazada(estudiantes))
    t_c_bst, arbol = medir_una_vez(lambda: construir_bst(estudiantes))
    filas_const = [
        ["List (copia)", us(t_c_list)],
        ["Set", us(t_c_set)],
        ["Dict", us(t_c_dict)],
        ["Lista enlazada", us(t_c_le)],
        ["BST (mezclado)", us(t_c_bst)],
    ]
    imprimir_tabla(["Estructura", "Construcción (µs)"], filas_const)
    secciones_md.append("## Costo de construcción (n = {:,})\n\n".format(len(estudiantes))
                        + tabla_md(["Estructura", "Construcción (µs)"], filas_const))

    # 3) Búsqueda del carnet con n completo (paso 5) ----------------------
    print(f"\n3) Midiendo búsquedas de {CARNET_BUSCAR} (costo de CONSULTA)...")
    t_lista = medir(lambda: buscar_lista(estudiantes, CARNET_BUSCAR), REP_LINEAL)
    t_set = medir(lambda: CARNET_BUSCAR in carnets_set, REP_RAPIDA)
    t_dict = medir(lambda: estudiantes_dict.get(CARNET_BUSCAR), REP_RAPIDA)
    t_le = medir(lambda: lista_enlazada.buscar(CARNET_BUSCAR), REP_LINEAL)
    t_bst = medir(lambda: arbol.buscar(CARNET_BUSCAR), REP_RAPIDA)

    print("\nRESULTADOS PROMEDIO")
    print(f"LIST           : {t_lista:.10f} s   -> O(n)")
    print(f"SET            : {t_set:.10f} s   -> O(1) promedio")
    print(f"DICT           : {t_dict:.10f} s   -> O(1) promedio")
    print(f"LISTA ENLAZADA : {t_le:.10f} s   -> O(n)")
    print(f"BST (mezclado) : {t_bst:.10f} s   -> ~O(log n)")

    print("\n4) Validación funcional")
    v_list = buscar_lista(estudiantes, CARNET_BUSCAR) is not None
    v_set = CARNET_BUSCAR in carnets_set
    v_dict = estudiantes_dict.get(CARNET_BUSCAR) is not None
    v_le = lista_enlazada.buscar(CARNET_BUSCAR) is not None
    v_bst = arbol.buscar(CARNET_BUSCAR) is not None
    print("LIST encontrado          :", v_list)
    print("SET encontrado           :", v_set)
    print("DICT encontrado          :", v_dict)
    print("LISTA ENLAZADA encontrado:", v_le)
    print("BST encontrado           :", v_bst)
    print("Registro recuperado (DICT):", estudiantes_dict.get(CARNET_BUSCAR))

    filas_busq = [
        ["List", "O(n)", us(t_lista), v_list],
        ["Set", "O(1) prom.", us(t_set), v_set],
        ["Dict", "O(1) prom.", us(t_dict), v_dict],
        ["Lista enlazada", "O(n)", us(t_le), v_le],
        ["BST (mezclado)", "~O(log n)", us(t_bst), v_bst],
    ]
    secciones_md.append(f"## Búsqueda de `{CARNET_BUSCAR}` con n = {len(estudiantes):,}\n\n"
                        + tabla_md(["Estructura", "Big O", "Promedio (µs)", "Encontrado"], filas_busq))

    # 5) Efecto de n (paso 6) --------------------------------------------
    print("\n5) Efecto de n (búsqueda del ÚLTIMO carnet de cada muestra, en µs)")
    filas_n = []
    for n in TAMANOS:
        muestra = estudiantes[:n]
        set_n = {e["carnet"] for e in muestra}
        dict_n = {e["carnet"]: e for e in muestra}
        le_n = construir_lista_enlazada(muestra)
        bst_n = construir_bst(muestra)
        carnet = muestra[-1]["carnet"]

        tl = medir(lambda: buscar_lista(muestra, carnet), REP_LINEAL)
        ts = medir(lambda: carnet in set_n, REP_RAPIDA)
        td = medir(lambda: dict_n.get(carnet), REP_RAPIDA)
        tle = medir(lambda: le_n.buscar(carnet), REP_LINEAL)
        tb = medir(lambda: bst_n.buscar(carnet), REP_RAPIDA)
        assert buscar_lista(muestra, carnet) and carnet in set_n and dict_n.get(carnet) \
            and le_n.buscar(carnet) and bst_n.buscar(carnet), "Validación fallida"

        filas_n.append([f"{n:,}", us(tl), us(ts), us(td), us(tle), us(tb),
                        bst_n.altura(), f"{log2(n):.1f}"])

    enc_n = ["n", "List O(n)", "Set O(1) prom.", "Dict O(1) prom.",
             "Lista enlazada O(n)", "BST ~O(log n)", "Altura BST", "log2(n)"]
    imprimir_tabla(enc_n, filas_n)
    tabla_principal = tabla_md(enc_n, filas_n)
    secciones_md.append("## Efecto de n (tiempos promedio en microsegundos, µs)\n\n" + tabla_principal)

    # 6) Lista enlazada: dos operaciones distintas (paso 7) ---------------
    print("\n6) Lista enlazada: insertar al inicio vs buscar")
    filas_le = []
    for n in TAMANOS:
        le = construir_lista_enlazada(estudiantes[:n])
        nuevo = {"carnet": "EST_NUEVO", "nombre": "Prueba"}

        def insertar_y_deshacer():
            le.insertar_inicio(nuevo)
            le.cabeza = le.cabeza.siguiente  # se deshace para no alterar n

        ti = medir(insertar_y_deshacer, REP_RAPIDA)
        tb = medir(lambda: le.buscar(estudiantes[n - 1]["carnet"]), REP_LINEAL)
        filas_le.append([f"{n:,}", us(ti), us(tb)])
    enc_le = ["n", "insertar_inicio O(1) (µs)", "buscar último O(n) (µs)"]
    imprimir_tabla(enc_le, filas_le)
    secciones_md.append("## Lista enlazada: insertar al inicio vs buscar\n\n" + tabla_md(enc_le, filas_le))

    # Ejemplo literal de la guía (10,000 insertados al inicio)
    ejemplo = ListaEnlazada()
    for estudiante in estudiantes[:10_000]:
        ejemplo.insertar_inicio(estudiante)
    print("   Ejemplo guía -> buscar('EST000001'):", ejemplo.buscar("EST000001"))

    # 7) BST mezclado vs ordenado (paso 8) --------------------------------
    print("\n7) BST: datos mezclados vs datos ya ordenados (n = 5,000)")
    muestra = estudiantes[:5_000]
    bst_mezclado = construir_bst(muestra, mezclar=True)
    bst_ordenado = construir_bst(muestra, mezclar=False)
    objetivo = muestra[-1]["carnet"]
    t_mez = medir(lambda: bst_mezclado.buscar(objetivo), REP_RAPIDA)
    t_ord = medir(lambda: bst_ordenado.buscar(objetivo), REP_LINEAL)
    filas_bst = [
        ["Mezclado (shuffle)", bst_mezclado.altura(), us(t_mez), "~O(log n)"],
        ["Ya ordenado", bst_ordenado.altura(), us(t_ord), "O(n) (degenerado)"],
    ]
    enc_bst = ["Inserción", "Altura", f"buscar {objetivo} (µs)", "Comportamiento"]
    imprimir_tabla(enc_bst, filas_bst)
    print(f"   log2(5000) = {log2(5000):.1f}")
    print("   Ejemplo guía -> buscar(muestra[-1]):", bst_mezclado.buscar(objetivo))
    secciones_md.append("## BST: inserción mezclada vs ordenada (n = 5,000)\n\n"
                        + tabla_md(enc_bst, filas_bst)
                        + f"\n\nReferencia: log2(5,000) ≈ {log2(5000):.1f} niveles.")

    # 8) Carnet inexistente (paso 9) --------------------------------------
    print(f"\n8) Reto: buscar carnet inexistente {CARNET_INEXISTENTE}")
    ci = CARNET_INEXISTENTE
    ti_l = medir(lambda: buscar_lista(estudiantes, ci), REP_LINEAL)
    ti_s = medir(lambda: ci in carnets_set, REP_RAPIDA)
    ti_d = medir(lambda: estudiantes_dict.get(ci), REP_RAPIDA)
    ti_le = medir(lambda: lista_enlazada.buscar(ci), REP_LINEAL)
    ti_b = medir(lambda: arbol.buscar(ci), REP_RAPIDA)
    filas_inex = [
        ["List", us(ti_l), buscar_lista(estudiantes, ci) is not None, "revisa los n elementos"],
        ["Set", us(ti_s), ci in carnets_set, "1 cálculo de hash"],
        ["Dict", us(ti_d), estudiantes_dict.get(ci) is not None, "1 cálculo de hash"],
        ["Lista enlazada", us(ti_le), lista_enlazada.buscar(ci) is not None, "recorre los n nodos"],
        ["BST (mezclado)", us(ti_b), arbol.buscar(ci) is not None, "baja hasta una hoja (altura)"],
    ]
    enc_inex = ["Estructura", "Promedio (µs)", "Encontrado", "Trabajo realizado"]
    imprimir_tabla(enc_inex, filas_inex)
    secciones_md.append(f"## Reto: carnet inexistente `{ci}` (n = {len(estudiantes):,})\n\n"
                        + tabla_md(enc_inex, filas_inex))

    # 9) Guardar evidencia ------------------------------------------------
    encabezado = (
        "# Mediciones generadas automáticamente por `src/main.py`\n\n"
        f"- Fecha: {datetime.now():%Y-%m-%d %H:%M}\n"
        f"- Origen de datos: {origen}\n"
        f"- Registros: {len(estudiantes):,}\n"
        f"- Python {platform.python_version()} · {platform.system()} {platform.release()} · {platform.processor() or platform.machine()}\n"
        f"- Repeticiones: {REP_LINEAL} (búsquedas lineales) / {REP_RAPIDA:,} (hash y BST)\n\n"
        "> Los tiempos dependen del equipo y de la carga del momento. "
        "Se deben comparar **tendencias**, no números absolutos.\n"
    )
    MEDICIONES.write_text(encabezado + "\n" + "\n\n".join(secciones_md) + "\n", encoding="utf-8")
    actualizar_resultados(tabla_principal, origen)
    print(f"\nOK: evidencia guardada en {MEDICIONES.relative_to(BASE)} y tabla actualizada en {RESULTADOS.relative_to(BASE)}")


def actualizar_resultados(tabla, origen):
    """Reemplaza la tabla entre las marcas de resultados.md con la de esta ejecución."""
    if not RESULTADOS.exists():
        return
    texto = RESULTADOS.read_text(encoding="utf-8")
    ini, fin = "<!-- TABLA_INICIO -->", "<!-- TABLA_FIN -->"
    if ini in texto and fin in texto:
        antes = texto.split(ini)[0]
        despues = texto.split(fin)[1]
        texto = f"{antes}{ini}\n{tabla}\n{fin}{despues}"
    ini_u, fin_u = "<!-- URL_INICIO -->", "<!-- URL_FIN -->"
    if ini_u in texto and fin_u in texto and not origen.startswith("archivo local"):
        antes = texto.split(ini_u)[0]
        despues = texto.split(fin_u)[1]
        texto = f"{antes}{ini_u}\n`{origen}`\n{fin_u}{despues}"
    RESULTADOS.write_text(texto, encoding="utf-8")


if __name__ == "__main__":
    main()
