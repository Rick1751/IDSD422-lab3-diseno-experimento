# comparacion_experimento.py — Comparación de grupos (Python)
# Ejecuta desde la raíz del repositorio:
#   python scripts/comparacion_experimento.py

import pandas as pd

# TODO 1 (hecho): carga plantillas/registro_experimento.csv con pandas
df = pd.read_csv("plantillas/registro_experimento.csv")
print("Registro cargado:")
print(df.to_string(index=False))

# TODO 2 (hecho): calcula e imprime el promedio de ventas_producto por ubicacion
print("\nPromedio de ventas_producto por ubicacion:")
print(df.groupby("ubicacion")["ventas_producto"].mean().to_string())

# TODO 3 (hecho): imprime el número de registros por grupo (value_counts)
print("\nNúmero de registros por grupo:")
print(df["ubicacion"].value_counts().to_string())

# TODO 4 (hecho): interpretación (sección 9 de la plantilla)
print("\nInterpretación:")
print("- Con 4 filas (2 por grupo, 4 tiendas distintas, todas en la semana 1) la diferencia")
print("  entre promedios no prueba nada: cada grupo mezcla tiendas distintas y un solo")
print("  registro pesa 50 % del promedio; además una fila tiene promoción simultánea.")
print("- Al análisis le faltarían: más unidades, comparar dentro de cada tienda (pareado),")
print("  incertidumbre (IC 95 % o prueba) y excluir o ajustar las semanas con promoción.")
