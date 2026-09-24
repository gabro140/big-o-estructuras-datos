# Resultados del laboratorio — GitHub + Big O + Estructuras de Datos

## Integrante
| Nombre | Carné |
|---|---|
| Gabriel Alessandro Castillo Panilla | 202400786 |

## URL RAW utilizada
<!-- URL_INICIO -->
`https://raw.githubusercontent.com/gabro140/big-o-estructuras-datos/main/data/estudiantes.csv`
<!-- URL_FIN -->

## Hipótesis Big O (antes de medir)

| Estructura | Forma de búsqueda | Complejidad esperada | Idea clave |
|---|---|---|---|
| List | Recorrido elemento a elemento | O(n) | Puede revisar hasta n registros. |
| Set | Hash | O(1) promedio | Comprueba pertenencia sin recorrer la colección. |
| Dictionary | Hash por llave | O(1) promedio | Recupera el registro completo usando el carnet como clave. |
| Lista enlazada | Recorrido nodo a nodo | O(n) | No tiene acceso directo por posición. |
| BST balanceado | Comparación y descarte de ramas | O(log n) | Cada comparación descarta una rama completa. |

## Mediciones

Tiempo **promedio de búsqueda** del último carnet de cada muestra, en microsegundos (µs).
La tabla la escribe automáticamente `python src/main.py`; el detalle completo
(construcción, lista enlazada, BST ordenado vs mezclado y carnet inexistente)
queda en [`mediciones.md`](mediciones.md).

<!-- TABLA_INICIO -->
| n | List O(n) | Set O(1) prom. | Dict O(1) prom. | Lista enlazada O(n) | BST ~O(log n) | Altura BST | log2(n) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 4.382 | 0.048 | 0.044 | 4.817 | 0.352 | 12 | 6.6 |
| 1,000 | 28.187 | 0.037 | 0.048 | 38.842 | 0.356 | 22 | 10.0 |
| 10,000 | 288.706 | 0.038 | 0.056 | 373.777 | 0.870 | 29 | 13.3 |
| 50,000 | 2,130.319 | 0.040 | 0.052 | 2,796.601 | 0.792 | 44 | 15.6 |
| 100,000 | 5,164.197 | 0.041 | 0.052 | 6,454.778 | 0.808 | 43 | 16.6 |
<!-- TABLA_FIN -->

### Lectura de la tabla
- **List y lista enlazada** crecen de forma casi proporcional a n: al multiplicar n por 10, el tiempo también se multiplica aproximadamente por 10. Esa es la huella de O(n).
- **Set y Dict** se mantienen prácticamente constantes (fracciones de microsegundo) aunque n pase de 100 a 100,000: O(1) promedio.
- **BST (datos mezclados)** crece muy lentamente; su altura sigue a log2(n) (con un factor constante, porque un BST aleatorio no queda perfectamente balanceado).
- La lista enlazada suele ser algo más lenta que la List aun teniendo la misma complejidad O(n): cada salto a `siguiente` accede a un objeto distinto en memoria, mientras que la List recorre un arreglo contiguo. Big O no captura esas constantes.

## Separación de costos: construcción vs consulta
Construir un Set o un Dict cuesta O(n) (hay que calcular el hash de cada carnet) y más memoria; construir el BST cuesta O(n log n) en promedio. Esa inversión se paga **una sola vez**. En cambio, cada consulta en una List cuesta O(n) **cada vez**. Si el sistema hace miles de consultas, el costo de construir el Dict se recupera muy rápido.

## Punto de control 7 — ¿Por qué una estructura puede ser O(1) y O(n) a la vez?
Porque la complejidad pertenece a la **operación**, no a la estructura. En la lista enlazada, `insertar_inicio` solo crea un nodo y cambia dos referencias (`nuevo.siguiente = cabeza` y `cabeza = nuevo`); ese trabajo es el mismo con 100 o con 100,000 nodos → O(1). En cambio, `buscar` no tiene forma de saltar a un nodo concreto: debe empezar por la cabeza y seguir `siguiente` uno por uno hasta encontrarlo → O(n). Las mediciones lo confirman: insertar al inicio se mantiene constante mientras que buscar el último crece con n.

## Punto de control 8 — BST vs árbol balanceado
Un **árbol binario de búsqueda (BST)** solo garantiza el orden (izquierda < nodo < derecha); **no** garantiza su forma. Un **árbol balanceado** (AVL, Rojo-Negro) además se reorganiza con rotaciones para que su altura sea siempre O(log n). Nuestro BST es básico: con los carnets mezclados obtuvo una altura cercana a log2(n) y búsquedas de ~1 µs; con los mismos 5,000 carnets insertados en orden, la altura fue 5,000 (una "lista" colgando a la derecha) y la búsqueda se volvió cientos de veces más lenta. Por eso **no todo BST garantiza O(log n)**.

## Punto de control 9 — Carnet inexistente (EST999999)
Para concluir que un valor **no existe**, una búsqueda lineal debe descartar todos los elementos: List y lista enlazada revisan los n registros, y ese es exactamente su peor caso, **O(n)**. En las mediciones, la búsqueda fallida de EST999999 tardó prácticamente lo mismo que buscar el último carnet (≈5,042 µs en List y ≈6,080 µs en la lista enlazada), porque en ambos casos se recorren los 100,000 registros; en cambio Set y Dict respondieron en ≈0.05 µs y el BST en ≈0.8 µs. Set y Dict calculan el hash, van a la posición correspondiente y al no encontrar la clave responden de inmediato: O(1) promedio. El BST baja por una sola rama hasta una hoja: el costo es su altura.

## Preguntas obligatorias de análisis

**1. ¿Por qué una búsqueda secuencial sobre List se clasifica como O(n)?**
Porque en el peor caso (carnet al final o inexistente) compara el carnet buscado con cada uno de los n registros. El número de comparaciones crece en proporción directa a n; en la tabla, multiplicar n por 10 multiplicó el tiempo aproximadamente por 10.

**2. ¿Por qué Set y Dictionary tienen búsqueda O(1) en promedio?**
Son tablas hash: la función hash convierte el carnet en la posición donde debería estar guardado, así que se va directo a esa posición sin recorrer la colección. Es "en promedio" porque pueden existir colisiones (dos claves en la misma posición); Python las mantiene pocas redimensionando la tabla, pero en el peor caso teórico la búsqueda podría degradarse a O(n).

**3. ¿Por qué O(1) no significa "cero tiempo" ni "exactamente el mismo tiempo siempre"?**
O(1) significa que el trabajo **no crece** con n, no que no exista. Calcular el hash y comparar la clave toma decenas de nanosegundos. Además el tiempo real varía por la caché del procesador, el recolector de basura, otros procesos del sistema operativo y la resolución del reloj; por eso en la tabla Set y Dict tienen pequeñas variaciones aunque sean O(1).

**4. ¿Cuál es la diferencia entre medir segundos y analizar Big O?**
Medir segundos es una observación empírica que depende del hardware, del lenguaje y de la carga del momento (por eso los resultados cambian entre computadoras). Big O es un análisis teórico que describe cómo **crece** el trabajo cuando n tiende a infinito, ignorando constantes. Medir sirve para **verificar la tendencia**; Big O sirve para **predecirla** y justificar decisiones antes de tener millones de datos.

**5. ¿Por qué una lista enlazada puede insertar al inicio en O(1) pero buscar en O(n)?**
Insertar al inicio solo modifica la referencia `cabeza` y el `siguiente` del nuevo nodo: un número fijo de pasos. Buscar requiere recorrer los nodos desde la cabeza porque no hay índice ni acceso directo; en el peor caso se visitan los n nodos.

**6. ¿Qué condición permite que un árbol de búsqueda se acerque a O(log n)?**
Que esté **balanceado** (o razonablemente balanceado): que la altura sea proporcional a log n. Así cada comparación descarta aproximadamente la mitad de los nodos restantes. Se logra insertando datos en orden aleatorio (como hicimos con `shuffle`) o, de forma garantizada, usando un árbol auto-balanceado (AVL, Rojo-Negro).

**7. ¿Qué ocurre con el BST si se inserta información ya ordenada?**
Cada nuevo carnet es mayor que todos los anteriores y se inserta siempre a la derecha: el árbol degenera en una cadena (altura = n) y se comporta como una lista enlazada, con búsqueda e inserción O(n). En nuestra prueba con 5,000 carnets la altura pasó de ~30 (mezclado) a 5,000 (ordenado). Con una implementación recursiva además se produce `RecursionError`, por eso usamos inserción iterativa.

**8. ¿Qué estructura elegiría para recuperar un estudiante completo por carnet? Justifique.**
**Dictionary** con el carnet como clave y el registro como valor. Recupera el registro completo en O(1) promedio con `dict.get(carnet)`, y el carnet es un identificador único, que es justo lo que se necesita como clave. Fue la opción más rápida para recuperar datos en todas las mediciones.

**9. ¿Qué estructura elegiría si solamente necesita saber si un carnet existe? Justifique.**
**Set**. La prueba de pertenencia `carnet in carnets_set` es O(1) promedio y el Set solo almacena los carnets (no los registros completos), por lo que usa menos memoria que un Dict. Si además se necesitaran los datos, convendría el Dict.

**10. Si el sistema realiza 70% búsquedas, 20% inserciones y 10% reportes, ¿qué decisión de diseño tomaría y por qué?**
Usaría un **Dictionary indexado por carnet** como estructura principal: cubre el 70% de búsquedas en O(1) promedio y el 20% de inserciones también en O(1) amortizado (`dict[carnet] = registro`). Para el 10% de reportes, que normalmente requieren recorrer todo u ordenar (por carrera, promedio, etc.), basta recorrer los valores en O(n) u ordenarlos en O(n log n) solo cuando se pide el reporte. Si los reportes necesitaran estar **siempre ordenados** o por rangos de carnet, agregaría un árbol balanceado como índice secundario (búsqueda, inserción y recorrido en orden con O(log n)). Descartaría la List y la lista enlazada como estructura de búsqueda, porque su O(n) por consulta se vuelve inaceptable con millones de estudiantes.

## Respuesta a la pregunta guía
Si el sistema pasara de 100 a 5,000,000 de estudiantes, buscar uno por uno en una List **no** sería conveniente: n crece 50,000 veces y el tiempo de cada búsqueda crecería en la misma proporción (de microsegundos a cientos de milisegundos por consulta), mientras que en un Dict o Set seguiría en fracciones de microsegundo.

## Conclusión
Este laboratorio mostró que, con los mismos 100,000 registros descargados desde GitHub,
la estructura elegida cambia por completo el costo de responder la misma pregunta.
La List y la lista enlazada tuvieron un crecimiento casi lineal: cada vez que n se
multiplicó por 10, el tiempo de búsqueda también lo hizo, confirmando O(n); además,
una búsqueda fallida las obliga a revisar los n elementos. Set y Dict mantuvieron
tiempos casi constantes gracias al hashing, lo que confirma O(1) en promedio, aunque
no "cero tiempo". El BST con datos mezclados logró búsquedas del orden de O(log n),
pero con datos ordenados degeneró a una cadena de altura n: un BST básico no es lo
mismo que un árbol balanceado. También comprobamos que la complejidad depende de la
operación: la lista enlazada inserta en O(1) pero busca en O(n). Para consultar
estudiantes por carnet la mejor decisión es un Dictionary, y un Set si solo importa la
existencia. Big O nos permite justificar esa elección antes de que el volumen de datos
convierta un diseño funcional en un sistema lento.
