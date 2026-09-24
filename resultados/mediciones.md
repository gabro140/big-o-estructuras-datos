# Mediciones generadas automáticamente por `src/main.py`

- Fecha: 2026-09-23 21:35
- Origen de datos: https://raw.githubusercontent.com/gabro140/big-o-estructuras-datos/main/data/estudiantes.csv
- Registros: 100,000
- Python 3.14.7 · Windows 11 · AMD64 Family 25 Model 120 Stepping 0, AuthenticAMD
- Repeticiones: 100 (búsquedas lineales) / 10,000 (hash y BST)

> Los tiempos dependen del equipo y de la carga del momento. Se deben comparar **tendencias**, no números absolutos.

## Costo de construcción (n = 100,000)

| Estructura | Construcción (µs) |
|---:|---:|
| List (copia) | 809.300 |
| Set | 8,741.900 |
| Dict | 16,534.500 |
| Lista enlazada | 36,625.700 |
| BST (mezclado) | 430,475.800 |

## Búsqueda de `EST099999` con n = 100,000

| Estructura | Big O | Promedio (µs) | Encontrado |
|---:|---:|---:|---:|
| List | O(n) | 5,421.364 | True |
| Set | O(1) prom. | 0.041 | True |
| Dict | O(1) prom. | 0.052 | True |
| Lista enlazada | O(n) | 5,946.603 | True |
| BST (mezclado) | ~O(log n) | 0.792 | True |

## Efecto de n (tiempos promedio en microsegundos, µs)

| n | List O(n) | Set O(1) prom. | Dict O(1) prom. | Lista enlazada O(n) | BST ~O(log n) | Altura BST | log2(n) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 4.382 | 0.048 | 0.044 | 4.817 | 0.352 | 12 | 6.6 |
| 1,000 | 28.187 | 0.037 | 0.048 | 38.842 | 0.356 | 22 | 10.0 |
| 10,000 | 288.706 | 0.038 | 0.056 | 373.777 | 0.870 | 29 | 13.3 |
| 50,000 | 2,130.319 | 0.040 | 0.052 | 2,796.601 | 0.792 | 44 | 15.6 |
| 100,000 | 5,164.197 | 0.041 | 0.052 | 6,454.778 | 0.808 | 43 | 16.6 |

## Lista enlazada: insertar al inicio vs buscar

| n | insertar_inicio O(1) (µs) | buscar último O(n) (µs) |
|---:|---:|---:|
| 100 | 0.256 | 6.366 |
| 1,000 | 0.162 | 36.092 |
| 10,000 | 0.167 | 363.229 |
| 50,000 | 0.170 | 3,479.459 |
| 100,000 | 0.167 | 6,262.165 |

## BST: inserción mezclada vs ordenada (n = 5,000)

| Inserción | Altura | buscar EST004999 (µs) | Comportamiento |
|---:|---:|---:|---:|
| Mezclado (shuffle) | 30 | 0.608 | ~O(log n) |
| Ya ordenado | 5000 | 337.319 | O(n) (degenerado) |

Referencia: log2(5,000) ≈ 12.3 niveles.

## Reto: carnet inexistente `EST999999` (n = 100,000)

| Estructura | Promedio (µs) | Encontrado | Trabajo realizado |
|---:|---:|---:|---:|
| List | 5,042.409 | False | revisa los n elementos |
| Set | 0.059 | False | 1 cálculo de hash |
| Dict | 0.048 | False | 1 cálculo de hash |
| Lista enlazada | 6,079.982 | False | recorre los n nodos |
| BST (mezclado) | 0.844 | False | baja hasta una hoja (altura) |
