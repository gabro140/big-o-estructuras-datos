class NodoArbol:
    def __init__(self, dato):
        self.dato = dato
        self.izquierda = None
        self.derecha = None


class ArbolBST:
    """Árbol binario de búsqueda (BST) básico, ordenado por carnet.

    IMPORTANTE: este BST NO se auto-balancea.
      - Si los datos llegan en orden aleatorio, la altura ~ O(log n) y
        buscar/insertar se aproximan a O(log n).
      - Si los datos llegan ya ordenados, cada nodo se cuelga a la derecha
        del anterior: el árbol degenera en una "lista" y buscar/insertar
        pasan a O(n).
    Un árbol balanceado (AVL, Rojo-Negro) sí garantiza O(log n).

    Nota: insertar y altura se implementan de forma iterativa para evitar
    RecursionError cuando el árbol degenera (Python limita la recursión ~1000).
    """

    def __init__(self):
        self.raiz = None
        self._tamano = 0

    def insertar(self, dato):
        nuevo = NodoArbol(dato)
        if self.raiz is None:
            self.raiz = nuevo
            self._tamano += 1
            return

        actual = self.raiz
        clave = dato["carnet"]
        while True:
            if clave < actual.dato["carnet"]:
                if actual.izquierda is None:
                    actual.izquierda = nuevo
                    self._tamano += 1
                    return
                actual = actual.izquierda
            elif clave > actual.dato["carnet"]:
                if actual.derecha is None:
                    actual.derecha = nuevo
                    self._tamano += 1
                    return
                actual = actual.derecha
            else:
                return  # carnet duplicado: no se inserta

    def buscar(self, carnet):
        actual = self.raiz
        while actual is not None:
            if carnet == actual.dato["carnet"]:
                return actual.dato
            if carnet < actual.dato["carnet"]:
                actual = actual.izquierda
            else:
                actual = actual.derecha
        return None

    def altura(self):
        """Número de niveles del árbol (recorrido por niveles, iterativo)."""
        if self.raiz is None:
            return 0
        nivel = [self.raiz]
        altura = 0
        while nivel:
            altura += 1
            siguiente = []
            for nodo in nivel:
                if nodo.izquierda:
                    siguiente.append(nodo.izquierda)
                if nodo.derecha:
                    siguiente.append(nodo.derecha)
            nivel = siguiente
        return altura

    def tamano(self):
        return self._tamano


if __name__ == "__main__":
    import random

    datos = [{"carnet": f"EST{i:06d}"} for i in range(1000)]

    ordenado = ArbolBST()
    for d in datos:
        ordenado.insertar(d)

    mezclado = ArbolBST()
    copia = datos.copy()
    random.shuffle(copia)
    for d in copia:
        mezclado.insertar(d)

    print("Altura con datos ORDENADOS :", ordenado.altura())
    print("Altura con datos MEZCLADOS :", mezclado.altura())
    print("Buscar EST000500:", mezclado.buscar("EST000500"))
