# simulacion_experimento.py — Demostración del análisis completo con datos SIMULADOS
# (el experimento no se ejecuta en esta práctica). Requiere haber corrido antes:
#   python scripts/asignacion_aleatoria.py
# Ejecutar desde la raíz del repositorio:
#   python scripts/simulacion_experimento.py
#
# ATENCIÓN: el efecto (+220 unidades) lo fijamos nosotros al simular; por eso el resultado
# NO es evidencia sobre RetailAndina, solo muestra cómo se analizaría un registro real.

import numpy as np
import pandas as pd
from scipy import stats

diseno = pd.read_csv("plantillas/asignacion_aleatoria.csv")
tiendas = list(dict.fromkeys(diseno["tienda"]))

rng = np.random.default_rng(1234598)
efecto_tienda = dict(zip(tiendas, rng.normal(1100, 120, len(tiendas))))  # nivel propio de cada tienda
efecto_semana = {1: 0, 2: 30, 3: 60, 4: 90}                              # tendencia supuesta
diseno["ventas_producto"] = (
    diseno["tienda"].map(efecto_tienda)
    + diseno["semana"].map(efecto_semana)
    + (diseno["ubicacion"] == "pasillo_principal") * 220                 # efecto supuesto
    + rng.normal(0, 90, len(diseno))
).round(0).astype(int)

# Una promoción simultánea registrada (factor a controlar nº 2)
diseno["promocion_simultanea"] = "no"
mask = (diseno["tienda"] == "Guayaquil Centro") & (diseno["semana"] == 1)
diseno.loc[mask, "promocion_simultanea"] = "si"
diseno.loc[mask, "ventas_producto"] += 180
diseno.to_csv("plantillas/resultado_simulacion.csv", index=False)


def analisis(d, etiqueta):
    """Análisis pareado: una diferencia (principal - habitual) por tienda."""
    piv = d.groupby(["tienda", "ubicacion"])["ventas_producto"].mean().unstack()
    dif = piv["pasillo_principal"] - piv["habitual"]
    n, media, dev = len(dif), dif.mean(), dif.std(ddof=1)
    ee = dev / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, df=n - 1)
    p = stats.ttest_rel(piv["pasillo_principal"], piv["habitual"]).pvalue
    print(f"\n[{etiqueta}]  tiendas = {n}")
    print(f"  Promedio de la diferencia (principal - habitual): {media:.1f} unidades/semana")
    print(f"  Desviación estándar de las diferencias:           {dev:.1f}")
    print(f"  IC 95 %: [{media - t_crit * ee:.1f} ; {media + t_crit * ee:.1f}]   p (t pareada) = {p:.6f}")


print("Unidades por grupo:")
print(diseno["ubicacion"].value_counts().to_string())
print("\nPromedio ingenuo por grupo (sin respetar el bloque tienda):")
print(diseno.groupby("ubicacion")["ventas_producto"].mean().round(1).to_string())
analisis(diseno, "Análisis pareado, todas las semanas")
analisis(diseno[diseno["promocion_simultanea"] == "no"], "Sensibilidad: sin la semana con promoción")
