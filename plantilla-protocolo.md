# Plantilla de protocolo — Experimento de ubicación de producto

**Equipo:** <<COMPLETAR>> · **Integrantes:** <<COMPLETAR>> · **Fecha:** 18/11/2026

**Repositorio (fork):** https://github.com/Rick1751/IDSD422-lab3-diseno-experimento

**Caso:** RetailAndina S.A. · IDSD422 · Estadística y Programación para Ciencia de Datos I · 2026-B · Práctica 3 (Tópico 3).
El experimento se diseña, no se ejecuta: los datos de la sección 9 son una plantilla de formato y una simulación.

## 1. Pregunta e hipótesis

**Pregunta:** ¿cambiar la ubicación del producto estrella de RetailAndina al pasillo principal aumenta sus ventas semanales?

**Hipótesis (comparación medible entre los grupos):** durante 4 semanas consecutivas, las ventas semanales del producto estrella son mayores en las semanas-tienda en que se exhibe en el pasillo principal (tratamiento) que en las semanas-tienda en que permanece en su ubicación habitual (control), comparando dentro de cada tienda.

- **Parámetro:** μ_dif = promedio, sobre las 10 tiendas, de [ventas semanales promedio en pasillo principal − ventas semanales promedio en ubicación habitual].
- **H0:** μ_dif = 0 (la ubicación no cambia las ventas). **H1:** μ_dif > 0 (el pasillo principal las aumenta).
- **Respuesta y período:** unidades vendidas del producto estrella por semana-tienda, durante 4 semanas consecutivas.
- **Cómo se confirma o refuta:** se contrasta con una t pareada por tienda, bilateral y con α = 0,05 (más exigente que la unilateral). Se confirma si se rechaza H0 con diferencia positiva; se refuta si el intervalo de confianza del 95 % incluye el 0 o es negativo. Para decidir mover inventario, además, la diferencia debería ser de al menos 110 unidades por semana (≈ 10 % de las ventas habituales).

## 2. Unidad experimental

*¿Qué recibe el tratamiento? ¿Cuántas unidades se incluyen?*

- **Unidad:** la **semana-tienda**: una tienda de RetailAndina durante una semana (lunes a domingo). Es lo que recibe el tratamiento: en esa semana el producto está o no en el pasillo principal. La tienda es el **bloque**: cada tienda aporta 4 unidades.
- **Número de unidades y justificación:** 10 tiendas × 4 semanas = **N = 40 unidades** (20 con tratamiento y 20 de control). Las 10 tiendas se reparten en 7 ciudades (Quito, Guayaquil, Cuenca, Ambato, Manta, Loja y Machala) para cubrir regiones y tamaños distintos.
  - Cada tienda es su propio control, así que se elimina la variación entre tiendas, que es la mayor fuente de ruido.
  - Potencia: con 10 pares de tiendas, una desviación estándar de las diferencias supuesta de 110 unidades por semana (supuesto de planificación, tomado de la simulación; no es un dato real) y α = 0,05 bilateral, la t pareada detecta una diferencia de 110 unidades por semana (≈ 10 %) con potencia ≈ 0,80.
  - Cuatro semanas permiten 2 contra 2 en cada tienda sin tener el producto fuera de su lugar habitual por mucho tiempo, y el costo operativo es bajo (se mueve un solo producto).

## 3. Factor, niveles y tratamiento

- **Factor** (variable manipulada): ubicación del producto estrella dentro de la tienda.
- **Niveles** (valores del factor): 2 niveles: `pasillo_principal` y `habitual` (el estante donde ya está hoy).
- **Tratamiento** (combinación asignada): cada semana-tienda recibe exactamente un nivel. El tratamiento es **exhibir el producto estrella en el pasillo principal durante esa semana** (nivel `pasillo_principal`) con todo lo demás fijo: mismo precio, mismo número de frentes de góndola, misma señalética y sin promoción especial. El pasillo no es el tratamiento sino un nivel del factor; el tratamiento es lo que recibe la unidad: el nivel más las condiciones fijas.
- **Coherencia con la hipótesis:** el investigador manipula un solo factor y solo cambia la ubicación; la respuesta (ventas) se compara entre sus dos niveles.

## 4. Grupo de control

*¿Cuál es la referencia sin tratamiento y qué rol cumple?*

- **Control:** las semanas-tienda en que el producto estrella permanece en su **ubicación habitual**, sin ningún cambio (20 de las 40 unidades). Es la misma tienda que otras 2 semanas recibe el tratamiento.
- **Rol:** es la referencia de lo que vende cada tienda cuando no se mueve el producto. Sin ella no se podría separar el efecto de la ubicación de la tendencia, la temporada o el nivel propio de cada tienda (un simple «antes y después» lo mezclaría todo). Como cada semana hay tiendas en ambos grupos a la vez, el control también absorbe lo que le pase a toda la cadena en esa semana.
- **Igual atención:** en las semanas de control el equipo de la tienda también revisa el producto y su stock, sin moverlo, para que ambos grupos reciban el mismo contacto.

## 5. Aleatorización

*¿Cómo se asignan las unidades a los grupos? ¿Por qué es necesaria?*

- **Línea de código de la asignación (Python o R):** escribe el comando que asigna al azar tus N unidades a los dos grupos (tratamiento y control) y ejecútalo con semilla. Incluye el resultado de una corrida y explica por qué el sorteo reparte los factores desconocidos entre los grupos.

## 6. Respuesta y medición

- Variable respuesta:
- Período de medición:
- Quién registra y cómo (¿ciego?):

## 7. Factores a controlar (mínimo 4)

| Factor a controlar | Cómo se controla o registra |
|---|---|
| 1. | |
| 2. | |
| 3. | |
| 4. | |

## 8. Limitaciones del diseño

*¿Qué podría invalidar el experimento si no se controla? ¿Qué no se podrá concluir?*

## 9. Comparación en código (Python/R)

*Escribe `scripts/comparacion_experimento.py` (o `.R`): debe cargar `plantillas/registro_experimento.csv` y calcular el promedio de `ventas_producto` por `ubicacion`. Incluye la salida y responde:*

- ¿Qué grupo muestra mayor venta promedio en la plantilla?
- ¿Por qué con 4 filas no se puede concluir nada sobre el efecto de la ubicación?
- Si el experimento se ejecutara con tu protocolo, ¿qué le faltaría a este análisis para ser justo?
