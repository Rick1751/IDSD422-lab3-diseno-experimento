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

- **Método:** aleatorización por bloques, con la tienda como bloque. Dentro de cada tienda se sortean sin reemplazo **2 de las 4 semanas** para el pasillo principal (tratamiento); las otras 2 quedan en la ubicación habitual (control). El sorteo lo hace el equipo de BI con código y semilla, antes de empezar, y se guarda en `plantillas/asignacion_aleatoria.csv`; los gerentes de tienda solo ejecutan el calendario.
- **Por qué es necesaria:** si cada gerente eligiera las semanas, el efecto de la ubicación quedaría mezclado con ese criterio (por ejemplo, poner el producto en pasillo principal justo en semanas de quincena). El sorteo reparte al azar, entre los dos grupos, los factores conocidos y también los desconocidos (clima, eventos locales, hábitos de compra, tendencia semanal), de modo que en promedio ambos grupos son comparables y la diferencia se atribuye a la ubicación. El bloque por tienda asegura 2 + 2 en cada una. Siguiendo la regla del curso: quien asigna con código es el investigador, por lo tanto es un experimento y no un estudio observacional.
- **Línea de código de la asignación (Python):**

```python
import numpy as np
rng = np.random.default_rng(1234597)   # semilla fija: el sorteo es reproducible
asignacion = {t: sorted(rng.choice([1, 2, 3, 4], size=2, replace=False).tolist()) for t in tiendas}
```

- **Corrida** (`python scripts/asignacion_aleatoria.py`, semilla 1234597; una segunda corrida da exactamente la misma salida):

```text
Semilla: 1234597

Semanas en pasillo_principal por tienda (las otras 2 quedan en habitual):
  Quito Norte       -> semanas [2, 4]
  Quito Sur         -> semanas [1, 2]
  Guayaquil Centro  -> semanas [3, 4]
  Guayaquil Norte   -> semanas [1, 4]
  Cuenca Centro     -> semanas [2, 3]
  Cuenca Sur        -> semanas [1, 2]
  Ambato Centro     -> semanas [1, 3]
  Manta             -> semanas [2, 3]
  Loja              -> semanas [2, 3]
  Machala           -> semanas [1, 2]

Unidades por grupo (N = 40):
ubicacion
habitual             20
pasillo_principal    20

Control de coherencia: unidades por tienda y grupo
ubicacion         habitual  pasillo_principal
tienda                                       
Ambato Centro            2                  2
Cuenca Centro            2                  2
Cuenca Sur               2                  2
Guayaquil Centro         2                  2
Guayaquil Norte          2                  2
Loja                     2                  2
Machala                  2                  2
Manta                    2                  2
Quito Norte              2                  2
Quito Sur                2                  2

Balance de la semana (1-4) entre grupos: semana promedio por grupo
ubicacion
habitual             2.7
pasillo_principal    2.3

Tiendas en pasillo_principal por semana
semana
1    5
2    7
3    5
4    3
```

- **Lectura:** el sorteo dejó 20 unidades por grupo y 2 + 2 en cada tienda. El azar no balancea perfecto la semana: el pasillo principal quedó con una semana promedio de 2,3 y el control de 2,7. Si las ventas crecen con las semanas, esto juega en contra del tratamiento (lo subestima un poco); por eso la semana se registra y se revisa en el análisis (secciones 7 y 8).

## 6. Respuesta y medición

- **Variable respuesta:** `ventas_producto` = unidades vendidas del producto estrella en la tienda durante la semana (lunes a domingo). Es cuantitativa y se mide una vez por semana-tienda. De forma informativa (no para decidir) se registra también las ventas totales de la tienda, para vigilar el efecto sobre otros productos.
- **Período de medición:** 4 semanas consecutivas, de lunes a domingo, con las mismas fechas de inicio en las 10 tiendas. La gerencia las elige fuera de feriados largos y sin campañas planificadas; si no es posible, se registran como factor (sección 7).
- **Quién registra y cómo (¿ciego?):** las ventas salen automáticamente del sistema de punto de venta (lectura de código de barras del producto) y el analista de BI las vuelca en `plantillas/registro_experimento.csv` (tienda, semana, ubicacion, ventas_producto, promocion_simultanea, notas). Los gerentes de tienda solo mueven el producto según el calendario y no registran ventas.
  - **Ciego:** no es posible cegar al personal de tienda, que ve la góndola. La medición es objetiva y automática, lo que reduce el sesgo del observador, y el analista que calcula la comparación recibe los grupos con códigos («A» y «B») hasta terminar el análisis fijado de antemano. El límite es que el personal podría, sin querer, recomendar más el producto cuando está en el pasillo principal: se le instruye no cambiar su forma de atender y se anota cualquier incidencia en `notas`.

## 7. Factores a controlar (mínimo 4)

| Factor a controlar | Cómo se controla o registra |
|---|---|
| 1. Temporada y feriados (quincena, vacaciones, fechas escolares) | Todas las tiendas corren las mismas 4 semanas calendario y se evita iniciar en feriado largo. La aleatorización dentro de cada tienda reparte las semanas entre grupos y la semana (1 a 4) se registra para revisarla en el análisis. |
| 2. Promociones | Control: no se permiten promociones, descuentos ni publicidad del producto estrella (ni de sus sustitutos directos) durante las 4 semanas. Si ocurre una promoción no planificada, se registra en `promocion_simultanea` (sí/no) y el análisis se repite sin esas filas. |
| 3. Afluencia de clientes | Registro: tickets o visitas por semana-tienda desde el POS o el contador de puerta, para revisar si el tráfico difiere entre grupos. El bloque por tienda mantiene el mismo local y el mismo público en ambos niveles. |
| 4. Stock disponible | Control: reposición garantizada con un inventario mínimo, igual para ambos niveles. Registro: los días con quiebre de stock se anotan en `notas` y esas semanas se analizan aparte. |
| 5. Precio | Control: el precio del producto queda fijo en todas las tiendas durante el experimento, sin cambios de lista. |
| 6. Espacio y presentación (frentes, señalética, altura del estante) | Control: mismo número de frentes y misma señalética en ambos niveles; solo cambia la ubicación. |
| 7. Tienda (tamaño, ciudad, nivel socioeconómico) | Bloqueo: cada tienda recibe los dos niveles (2 + 2) y el análisis compara dentro de cada tienda (pareado). |
| 8. Eventos locales, clima y competencia | Registro: se anotan en `notas` por semana-tienda; la aleatorización los reparte entre grupos. |

## 8. Limitaciones del diseño

*¿Qué podría invalidar el experimento si no se controla? ¿Qué no se podrá concluir?*

## 9. Comparación en código (Python/R)

*Escribe `scripts/comparacion_experimento.py` (o `.R`): debe cargar `plantillas/registro_experimento.csv` y calcular el promedio de `ventas_producto` por `ubicacion`. Incluye la salida y responde:*

- ¿Qué grupo muestra mayor venta promedio en la plantilla?
- ¿Por qué con 4 filas no se puede concluir nada sobre el efecto de la ubicación?
- Si el experimento se ejecutara con tu protocolo, ¿qué le faltaría a este análisis para ser justo?
