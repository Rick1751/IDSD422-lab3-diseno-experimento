# asignacion_aleatoria.py — Sección 5 del protocolo: aleatorización por bloques
# Ejecutar desde la raíz del repositorio:
#   python scripts/asignacion_aleatoria.py
#
# Diseño: 10 tiendas (bloques) x 4 semanas = 40 unidades experimentales (semana-tienda).
# Dentro de cada tienda se sortean al azar 2 de las 4 semanas para el pasillo principal
# (tratamiento); las otras 2 quedan en la ubicación habitual (control). Resultado: 20 y 20.

import numpy as np
import pandas as pd

SEMILLA = 1234597
tiendas = ["Quito Norte", "Quito Sur", "Guayaquil Centro", "Guayaquil Norte",
           "Cuenca Centro", "Cuenca Sur", "Ambato Centro", "Manta", "Loja", "Machala"]
semanas = [1, 2, 3, 4]

rng = np.random.default_rng(SEMILLA)

# LÍNEA DE ASIGNACIÓN: por tienda, qué 2 de las 4 semanas van al pasillo principal
asignacion = {t: sorted(rng.choice(semanas, size=2, replace=False).tolist()) for t in tiendas}

# Tabla completa de las 40 unidades (semana-tienda) con su grupo
filas = [{"tienda": t, "semana": s,
          "ubicacion": "pasillo_principal" if s in asignacion[t] else "habitual"}
         for t in tiendas for s in semanas]
diseno = pd.DataFrame(filas)
diseno.to_csv("plantillas/asignacion_aleatoria.csv", index=False)

print(f"Semilla: {SEMILLA}")
print("\nSemanas en pasillo_principal por tienda (las otras 2 quedan en habitual):")
for t, sem in asignacion.items():
    print(f"  {t:<17} -> semanas {sem}")
print("\nUnidades por grupo (N = 40):")
print(diseno["ubicacion"].value_counts().to_string())
print("\nControl de coherencia: unidades por tienda y grupo")
print(pd.crosstab(diseno["tienda"], diseno["ubicacion"]).to_string())
print("\nBalance de la semana (1-4) entre grupos: semana promedio por grupo")
print(diseno.groupby("ubicacion")["semana"].mean().round(2).to_string())
print("\nTiendas en pasillo_principal por semana")
print(diseno[diseno["ubicacion"] == "pasillo_principal"]["semana"].value_counts().sort_index().to_string())
