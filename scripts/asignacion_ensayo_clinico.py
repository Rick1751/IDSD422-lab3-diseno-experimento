# asignacion_ensayo_clinico.py — Bonus: el mismo diseño adaptado a un ensayo clínico (vacuna)
# Ejecutar desde la raíz del repositorio:
#   python scripts/asignacion_ensayo_clinico.py
#
# Diseño ilustrativo: 4 centros (bloques) x 500 participantes = N = 2000.
# En cada centro se sortean 250 a "vacuna" y 250 a "placebo" (aleatorización por bloques).

import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
centros = ["Centro A", "Centro B", "Centro C", "Centro D"]

filas = []
for c in centros:
    # LÍNEA DE ASIGNACIÓN: permutación aleatoria de 250 'vacuna' y 250 'placebo' en el centro
    grupos = rng.permutation(["vacuna"] * 250 + ["placebo"] * 250)
    filas += [{"participante": f"{c[-1]}-{i + 1:03d}", "centro": c, "grupo": g}
              for i, g in enumerate(grupos)]
ensayo = pd.DataFrame(filas)

print("Participantes por centro y grupo (N = 2000):")
print(pd.crosstab(ensayo["centro"], ensayo["grupo"]).to_string())
print("\nPrimeros 6 participantes asignados:")
print(ensayo.head(6).to_string(index=False))
