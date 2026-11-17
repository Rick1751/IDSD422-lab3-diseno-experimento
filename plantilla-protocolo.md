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

**Qué podría invalidarlo si no se controla**

- **Incumplimiento del protocolo:** un gerente que no mueve el producto en la semana asignada, promociones no registradas o quiebres de stock. Todo se registra; si afecta a muchas unidades, el diseño pierde validez y habría que repetirlo.
- **Arrastre entre semanas (carryover):** un cliente que compró el producto en el pasillo principal puede seguir buscándolo ahí o comprándolo por hábito en una semana de ubicación habitual, lo que achica la diferencia. No hay período de lavado entre cambios; solo se puede revisar con un análisis de sensibilidad.
- **Desbalance por azar:** con 40 unidades el sorteo no balancea perfecto las semanas (en la corrida, semana promedio 2,3 contra 2,7). Se registra la semana y se revisa en el análisis.
- **Personal no ciego:** puede influir sin querer en la venta del producto (sección 6).

**Qué no se podrá concluir**

- **Horizonte corto:** 4 semanas no dicen si el efecto dura; puede ser un efecto de novedad que desaparece cuando el cambio es permanente.
- **Rentabilidad total:** se mide el producto estrella, no el resto de la tienda; no se sabe si el producto desplazado o los demás productos venden menos (canibalización). Más unidades del producto no equivalen a más ganancia para la tienda.
- **Generalización:** 10 tiendas elegidas por conveniencia (no una muestra aleatoria de la cadena) y un solo producto; no se puede extender a otros productos, otras tiendas ni otros pasillos.
- **Mecanismo y precisión:** no se sabrá por qué funciona (visibilidad o flujo de clientes) y con 10 tiendas el intervalo de confianza será amplio; la potencia de 0,80 depende de un supuesto de variabilidad no verificado.
- **Datos de este laboratorio:** el registro de 4 filas y la simulación de la sección 9 no son evidencia sobre RetailAndina; la simulación incluye un efecto que fijamos nosotros.

## 9. Comparación en código (Python/R)

Se usó **Python**: `scripts/comparacion_experimento.py` (TODOs completados) carga `plantillas/registro_experimento.csv` y calcula el promedio de `ventas_producto` por `ubicacion`. Se ejecuta desde la raíz del repositorio con `python scripts/comparacion_experimento.py` y su salida es:

```text
Registro cargado:
          tienda  semana         ubicacion  ventas_producto promocion_simultanea  notas
     Quito Norte       1 pasillo_principal             1250                   no    NaN
       Quito Sur       1          habitual              980                   no    NaN
Guayaquil Centro       1 pasillo_principal             1420                   si    NaN
 Guayaquil Norte       1          habitual             1100                   no    NaN

Promedio de ventas_producto por ubicacion:
ubicacion
habitual             1040.0
pasillo_principal    1335.0

Número de registros por grupo:
ubicacion
pasillo_principal    2
habitual             2

Interpretación:
- Con 4 filas (2 por grupo, 4 tiendas distintas, todas en la semana 1) la diferencia
  entre promedios no prueba nada: cada grupo mezcla tiendas distintas y un solo
  registro pesa 50 % del promedio; además una fila tiene promoción simultánea.
- Al análisis le faltarían: más unidades, comparar dentro de cada tienda (pareado),
  incertidumbre (IC 95 % o prueba) y excluir o ajustar las semanas con promoción.
```

- **¿Qué grupo muestra mayor venta promedio en la plantilla?** El pasillo principal: 1335 contra 1040 unidades (295 más). Es solo una descripción de 4 filas.
- **¿Por qué con 4 filas no se puede concluir nada sobre el efecto de la ubicación?** Cada grupo tiene solo 2 registros de tiendas distintas, todas de la semana 1: un solo dato pesa el 50 % del promedio y cada tienda aparece en un solo grupo, así que la diferencia se mezcla con el nivel propio de ventas de cada tienda. Además una de las 4 filas tiene promoción simultánea. Con tan pocos datos no se puede calcular la variabilidad ni saber si la diferencia es mayor que lo esperable por azar.
- **Si el experimento se ejecutara con tu protocolo, ¿qué le faltaría a este análisis para ser justo?**
  - Las 40 unidades asignadas al azar (no 4 filas sin sorteo).
  - Comparar dentro de cada tienda (diferencia pareada), para quitar el efecto de cada tienda.
  - Medir la incertidumbre (desviación estándar de las diferencias, IC 95 % y t pareada) y no solo promedios.
  - Excluir o ajustar las semanas con promoción, quiebre de stock u otros factores registrados, y revisar la semana.

**Demostración con datos simulados.** Para mostrar cómo se analizaría un registro completo, `scripts/simulacion_experimento.py` toma la asignación de la sección 5 y simula las 40 ventas (nivel propio por tienda, tendencia semanal, ruido y una promoción registrada). **El efecto de +220 unidades lo fijamos nosotros al simular**, así que este resultado no es evidencia sobre RetailAndina: solo comprueba que el análisis pareado recupera un efecto conocido y entrega su intervalo (se guarda en `plantillas/resultado_simulacion.csv`).

```text
Unidades por grupo:
ubicacion
habitual             20
pasillo_principal    20

Promedio ingenuo por grupo (sin respetar el bloque tienda):
ubicacion
habitual             1118.6
pasillo_principal    1335.4

[Análisis pareado, todas las semanas]  tiendas = 10
  Promedio de la diferencia (principal - habitual): 216.8 unidades/semana
  Desviación estándar de las diferencias:           109.1
  IC 95 %: [138.8 ; 294.8]   p (t pareada) = 0.000144

[Sensibilidad: sin la semana con promoción]  tiendas = 10
  Promedio de la diferencia (principal - habitual): 219.7 unidades/semana
  Desviación estándar de las diferencias:           109.8
  IC 95 %: [141.1 ; 298.3]   p (t pareada) = 0.000137
```

La diferencia estimada (≈ 217) queda cerca del efecto fijado (220), el IC 95 % no incluye el 0 y el resultado casi no cambia al excluir la semana con promoción. Con datos reales no sabríamos la respuesta de antemano; por eso importan la aleatorización y los controles de las secciones anteriores. (El archivo `scripts/comparacion_experimento.R` quedó sin completar porque se eligió Python.)

## Bonus: adaptación a un ensayo clínico (vacuna)

El mismo diseño (unidad, factor, control, aleatorización, respuesta, controles y limitaciones) aplicado a una **vacuna candidata**. Los números son ilustrativos: en un ensayo real el tamaño se calcula con la incidencia esperada y la eficacia mínima que se quiere detectar.

| Elemento | Ubicación de producto (RetailAndina) | Ensayo clínico de una vacuna |
|---|---|---|
| Hipótesis | Las ventas semanales son mayores con el producto en el pasillo principal que en su ubicación habitual. | La incidencia de enfermedad confirmada a 6 meses es menor en vacunados que en el grupo placebo. |
| Unidad experimental | Semana-tienda (N = 40). | Participante adulto voluntario con consentimiento informado (N = 2000, ilustrativo). |
| Factor y niveles | Ubicación: `pasillo_principal` / `habitual`. | Intervención: `vacuna` / `placebo`. |
| Tratamiento | Producto en pasillo principal durante una semana, resto fijo. | 2 dosis (días 0 y 28) del nivel asignado, mismo esquema y volumen. |
| Grupo de control | Ubicación habitual en la misma tienda. | Placebo (solución salina): controla el efecto placebo y la evolución natural de la enfermedad. |
| Aleatorización | 2 de 4 semanas por tienda, con semilla. | 250 vacuna y 250 placebo por centro (bloque), con semilla (código abajo). |
| Respuesta y medición | Unidades vendidas por semana, desde el POS; no hay ciego pleno. | Casos confirmados por PCR en 6 meses, juzgados por un comité independiente; **doble ciego**: participantes y evaluadores no conocen el grupo. |
| Factores a controlar | Temporada, promociones, afluencia, stock, precio. | Edad, comorbilidades, centro, exposición al virus, vacunación previa (estratificación por centro y registro de las demás). |
| Limitaciones | Arrastre, 4 semanas, un producto, 10 tiendas. | Seguimiento de 6 meses, voluntarios que no representan a niños o embarazadas, pérdidas de seguimiento. |

Diferencias clave: en el ensayo sí es posible el doble ciego (con el placebo) y la unidad es una persona, por lo que hay requisitos éticos: consentimiento informado, aprobación de un comité de ética y monitoreo independiente de seguridad que puede detener el ensayo.

Asignación aleatoria del ensayo (`python scripts/asignacion_ensayo_clinico.py`, semilla 2026):

```python
rng = np.random.default_rng(2026)
grupos = rng.permutation(["vacuna"] * 250 + ["placebo"] * 250)   # una vez por centro
```

```text
Participantes por centro y grupo (N = 2000):
grupo     placebo  vacuna
centro                   
Centro A      250     250
Centro B      250     250
Centro C      250     250
Centro D      250     250

Primeros 6 participantes asignados:
participante   centro   grupo
       A-001 Centro A placebo
       A-002 Centro A  vacuna
       A-003 Centro A placebo
       A-004 Centro A  vacuna
       A-005 Centro A  vacuna
       A-006 Centro A placebo
```
