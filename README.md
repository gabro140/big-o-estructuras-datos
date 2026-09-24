# big-o-estructuras-datos

Laboratorio **GitHub + Big O + Estructuras de Datos** — Proyecto Integrador.

## Problema
Una universidad administra miles de estudiantes (carnet, nombre, carrera, departamento, promedio).
El sistema consulta constantemente si un estudiante existe y recupera sus datos a partir del carnet.
Se evalúa qué estructura de datos se comporta mejor cuando crece la cantidad de registros, comparando
la **misma operación de búsqueda** en:

| Estructura | Búsqueda por carnet |
|---|---|
| List | O(n) |
| Set | O(1) promedio |
| Dictionary | O(1) promedio |
| Lista enlazada (`src/lista_enlazada.py`) | O(n) — insertar al inicio O(1) |
| Árbol binario de búsqueda (`src/arbol_bst.py`) | ~O(log n) si está balanceado; O(n) si degenera |

Los datos (100,000 estudiantes) se publican en este repositorio y Python los consume desde la **URL RAW** de GitHub.

## Integrantes
| Nombre | Carné |
|---|---|
| Gabriel Alessandro Castillo Panilla | 202400786 |
| _(agregar integrante)_ | |

## Estructura
```
big-o-estructuras-datos/
├── data/estudiantes.csv        # dataset generado (100,000 registros)
├── src/
│   ├── generar_datos.py        # genera el CSV (semilla fija, reproducible)
│   ├── main.py                 # descarga desde GitHub RAW, mide y documenta
│   ├── lista_enlazada.py       # lista simplemente enlazada
│   └── arbol_bst.py            # árbol binario de búsqueda
├── resultados/
│   ├── resultados.md           # tabla, respuestas de análisis y conclusión
│   └── mediciones.md           # evidencia completa generada por main.py
├── README.md
└── .gitignore
```

## Cómo ejecutar desde cero
Requisitos: Python 3 (sin librerías externas) y conexión a Internet.

```bash
git clone https://github.com/gabro140/big-o-estructuras-datos.git
cd big-o-estructuras-datos

# 1. (Opcional) regenerar el dataset — ya viene publicado en data/
python src/generar_datos.py

# 2. Ejecutar el análisis (descarga el CSV desde la URL RAW configurada en src/main.py)
python src/main.py
```
En Windows, si `python` no se reconoce, use `py` en su lugar.

`main.py`:
1. Descarga el CSV desde GitHub y verifica que lleguen **100,000 registros**.
2. Construye List, Set, Dict, lista enlazada y BST (y mide su costo de construcción por separado).
3. Mide la búsqueda de `EST099999` con `time.perf_counter()` y valida que todas devuelvan `True`.
4. Repite la búsqueda para n = 100, 1,000, 10,000, 50,000 y 100,000.
5. Compara en la lista enlazada `insertar_inicio` (O(1)) vs `buscar` (O(n)).
6. Compara el BST con datos mezclados vs ya ordenados (árbol degenerado).
7. Busca un carnet inexistente (`EST999999`).
8. Guarda la evidencia en `resultados/mediciones.md` y actualiza la tabla de `resultados/resultados.md`.

> Para probar sin Internet: `python src/main.py --local` (lee `data/estudiantes.csv`). La entrega oficial usa la URL RAW.

> Los tiempos cambian según el equipo; se comparan **tendencias**, no números absolutos.

## Resultados
Ver [`resultados/resultados.md`](resultados/resultados.md).
