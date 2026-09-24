class Nodo:
    """Nodo simple: guarda un registro (dict) y la referencia al siguiente nodo."""

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    """Lista simplemente enlazada.

    Complejidad por operación:
      - insertar_inicio: O(1)  -> solo se cambian dos referencias, sin importar n.
      - buscar:          O(n)  -> no hay acceso directo; se recorre nodo a nodo.
      - tamano:          O(1)  -> se lleva un contador.
    """

    def __init__(self):
        self.cabeza = None
        self._tamano = 0

    def insertar_inicio(self, dato):
        nuevo = Nodo(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self._tamano += 1

    def buscar(self, carnet):
        actual = self.cabeza
        while actual is not None:
            if actual.dato["carnet"] == carnet:
                return actual.dato
            actual = actual.siguiente
        return None

    def tamano(self):
        return self._tamano


if __name__ == "__main__":
    # Prueba rápida independiente
    lista = ListaEnlazada()
    for i in range(5):
        lista.insertar_inicio({"carnet": f"EST{i:06d}", "nombre": f"Estudiante {i}"})
    print("Tamaño:", lista.tamano())
    print("Buscar EST000001:", lista.buscar("EST000001"))
    print("Buscar EST999999:", lista.buscar("EST999999"))
