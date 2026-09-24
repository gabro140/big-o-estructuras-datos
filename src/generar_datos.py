import csv
import random
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RUTA = BASE / "data" / "estudiantes.csv"
CANTIDAD = 100_000
SEMILLA = 2026  # semilla fija: el dataset es reproducible

random.seed(SEMILLA)

carreras = [
    "Ingeniería en Sistemas",
    "Ingeniería Industrial",
    "Administración",
    "Arquitectura",
    "Contaduría",
]

departamentos = [
    "San Salvador",
    "La Libertad",
    "Santa Ana",
    "San Miguel",
    "Sonsonate",
]

RUTA.parent.mkdir(parents=True, exist_ok=True)

with RUTA.open("w", newline="", encoding="utf-8") as archivo:
    escritor = csv.writer(archivo)
    escritor.writerow(["carnet", "nombre", "carrera", "departamento", "promedio"])

    for i in range(CANTIDAD):
        escritor.writerow([
            f"EST{i:06d}",
            f"Estudiante {i}",
            random.choice(carreras),
            random.choice(departamentos),
            round(random.uniform(5.0, 10.0), 2),
        ])

print(f"OK: archivo generado en {RUTA}")
print(f"OK: registros generados: {CANTIDAD:,}")
