# Auditoría de la Práctica 1 — MEDIATEC «Marismas del Odiel»

**Fichero auditado:** `Practica1_Base_C1.mpp` (título interno: *Práctica 1 - MEDIATEC - Escenario base (Cuestión 1)*).
**Fuentes:** `Practica1-2026.pdf` (enunciado, 7 págs.), `sueldos.pdf` (Adecco/Infoempleo), `Plantilla-Memoria-Practica1 Alumnos.docx`, y el Decreto 101/2025 del BOJA (calendario de fiestas laborales de Andalucía para 2026).
**Fecha de la auditoría:** 23/10/2026.

## Cómo se ha obtenido la evidencia

- Se copió el `.mpp` a una carpeta temporal y se abrió **esa copia, en solo lectura**, con Microsoft Project mediante COM. El original no se ha modificado.
- De esa copia se exportó un XML (MSPDI) y se leyeron directamente de Project los campos Costo, Costo fijo, Costo previsto, Crítica, Margen total, Sobreasignada y el trabajo diario de cada recurso, con escala de tiempo diaria.
- El coste de personal se **recalculó de forma independiente**, aplicando las tasas derivadas de `sueldos.pdf` a cada hora de trabajo diaria. Resultado: **31.912,03 €**, frente a los **31.911,75 €** de Project. Los 0,28 € de diferencia se deben a que Project usa tasas redondeadas a dos decimales.
- Lo que no se ha podido ver (por ejemplo, el aspecto visual de las vistas o los filtros guardados) figura como ❓ **NO VERIFICABLE**.

---

# A. Diagnóstico general

**Estado global: PARCIALMENTE CORRECTO.**

La estructura, las horas, los roles, las tasas salariales y el calendario son, en su mayoría, correctos y están bien trabajados. Pero hay **un error crítico de costes**: todos los costes fijos están introducidos con un valor 100 veces menor. Por eso el coste total que muestra Project (**32.338,33 €**) está muy por debajo del real (**74.569,75 €**), y la Cuestión 1 calculada con el fichero sería errónea. Además, no hay memoria ni análisis documentado de la Cuestión 2.

### Estimación de nota (sobre 2,5)

| Apartado (peso) | Estado actual (solo el .mpp) | Nota estimada actual | Tras las correcciones y la memoria |
|---|---|---|---|
| Planificación (0,7) | EDT completa, horas y roles exactos, calendario correcto en el periodo. Falta el solape −1 día (2←1), hay vínculos no pedidos (3←2, 4←3, terminales←10) sin justificar, los hitos están «colgados» y la ruta crítica aparece contaminada por restricciones. | 0,45 – 0,55 | 0,60 – 0,70 |
| Costes (0,5) | Coste hora y variaciones salariales impecables, pero **todos los costes fijos están a 1/100** y el total es erróneo. | 0,15 – 0,25 | 0,45 – 0,50 |
| Cuestión 1 (0,3) | Con el fichero, la oferta saldría de 32.338,33 € (incorrecto). | 0 – 0,05 | 0,25 – 0,30 |
| Cuestión 2 (0,5) | El plan termina el 09/04 sin horas extra, lo que **responde «sí»**, pero no hay análisis, ni comprobación documentada, ni justificación de por qué la base ya llega. | 0,05 – 0,15 | 0,30 – 0,45 (*) |
| Justificación (0,3) | No hay memoria. | 0 | 0,20 – 0,30 |
| Memoria y ficheros (0,2) | No hay memoria ni índice de ficheros. | 0 | 0,15 – 0,20 |
| **Total** | | **≈ 0,65 – 1,0** | **≈ 1,95 – 2,45** |

(*) La nota de la Cuestión 2 tiene **mucha incertidumbre**. La plantilla del profesor da por hecho que el escenario base «No llega al 13 de abril» (fila A0, apartado 7.2). Vuestro plan sí llega, gracias a una hipótesis de reparto del trabajo muy agresiva (ver la sección J). Si el profesor no acepta esa hipótesis, la Cuestión 2 y parte de la Planificación podrían bajar bastante. Si la justificáis bien, es defendible.

---

# B. Matriz de cumplimiento

Leyenda: ✅ Correcto · ⚠️ Parcial · ❌ Incorrecto · ❓ No verificable.
Las referencias de página son las del enunciado (`Practica1-2026.pdf`). Los IDs son los del .mpp.

### Bloque I — Puntos de control (pág. 2–3)

| ID | Requisito | Evidencia en el MPP | Estado | Error o diferencia | Corrección |
|---|---|---|---|---|---|
| I.1 | 12 salas × 20 máquinas = 240 puntos | ID 2 «Montaje de soportes metálicos (240 uds.)», ID 11 (240 terminales) | ✅ | — | — |
| I.2 | Soportes: 240 × 8,20 € = 1.968 € | ID 2, Costo fijo = **19,68 €** (la nota de la tarea dice «240 x 8.20 €») | ❌ | Valor 100 veces menor | Costo fijo = 1.968 |
| I.3 | 30 min/soporte ⇒ 120 h | ID 2, Trabajo = 120 h | ✅ | — | — |
| I.4 | 2 operarios disponibles | Recurso «Operarios estructuras metálicas», Capacidad máx. 200 %, asignado al 200 % ⇒ duración 60 h = 7,5 días | ✅ | — | — |
| I.5 | Tarifa normal 34 €/h | Tasa estándar 34 €/h; coste de mano de obra 120 h × 34 = 4.080 € | ✅ | — | — |
| I.6 | Horas extra +30 % | Tasa h. extra 44,20 € = 34 × 1,30 | ✅ | — | — |
| I.7 | Espera de 1 día (soldadura) antes de electricidad y red | ID 4 y ID 7: predecesora 2 FC+1 día | ✅ | Es un retardo en días laborables (sería defendible también «1 día transcurrido»). | Declarar la hipótesis |
| I.8 | Electricidad secuencial: cables 5 d → puntos 2 d | ID 4 (40 h = 5 d) → ID 5 (16 h = 2 d), vínculo 4→5 FC | ✅ | — | — |
| I.9 | Costes eléctricos 920 € y 340 € | ID 4 = **9,20 €**, ID 5 = **3,40 €** | ❌ | 100 veces menor | 920 y 340 |
| I.10 | Red secuencial 2 d / 4 d / 3 d / 2 d | IDs 7→8→9→10, duraciones 16/32/24/16 h | ✅ | — | — |
| I.11 | Costes de red 230/640/580/460 € | IDs 7–10 = **2,30 / 6,40 / 5,80 / 4,60 €** | ❌ | 100 veces menor | 230, 640, 580, 460 |
| I.12 | Red puede solaparse con electricidad | Ambas arrancan el 27/02 13:00 en paralelo | ✅ | — | — |
| I.13 | Terminales: 240 × 44 € = 10.560 € | ID 11, Costo fijo = **105,60 €** | ❌ | 100 veces menor | 10.560 |
| I.14 | 15 min/terminal con personal propio ⇒ 60 h | ID 11, Trabajo = 60 h (Álvaro 30 h + Lucía 30 h) | ✅ | — | — |
| I.15 | Cerrar un punto exige corriente y red | ID 11, predecesoras 5 (puntos de corriente) y 10 (armario/certificación) | ✅ | — | — |
| I.16 | Decidir entre cierre progresivo y esperar | Se espera a que terminen ambas instalaciones (cierre en bloque del 17/03 al 20/03) | ⚠️ | Decisión válida (la tarea tiene 9,06 días de margen) pero no está justificada (decisión D-3). | Justificar en la memoria con el dato del margen |
| I.17 | Montaje del armario dentro de la partida de red | ID 10, predecesora del suministro (ID 18) | ✅ | — | — |
| I.18 | (Implícito) Vínculos solo justificados | ID 11 tiene además como predecesora la **tarea 10 «Verificación del diseño»** (ID 31) | ⚠️ | No lo pide el enunciado. Es un vínculo «de recurso» (Álvaro y Lucía están ocupados hasta el 17/03 10:00). | Justificar o sustituir por redistribución |

### Bloque II — Tornos de acceso (pág. 3–4)

| ID | Requisito | Evidencia | Estado | Error | Corrección |
|---|---|---|---|---|---|
| II.1 | 3 tornos × 1.850 € = 5.550 € | ID 13, Costo fijo = **55,50 €** | ❌ | 100 veces menor | 5.550 |
| II.2 | Barreras 880 € en total | ID 14, Costo fijo = **8,80 €** | ❌ | 100 veces menor | 880 |
| II.3 | 6 lectores NFC × 920 € = 5.520 € | ID 15, Costo fijo = **55,20 €** | ❌ | 100 veces menor | 5.520 |
| II.4 | Montaje de tornos: 2 días, misma empresa y tarifa | ID 13: 16 h de duración, operarios al 200 % ⇒ 32 h × 34 € = 1.088 € | ✅ | Hipótesis: trabajan los 2 operarios los 2 días | Declararla |
| II.5 | Barreras: 1 día | ID 14: 8 h, 16 h de trabajo ⇒ 544 € | ✅ | Ídem | Declararla |
| II.6 | Integración NFC: 1 jornada, personal propio | ID 15: Rubén Ferrer, 8 h | ✅ | — | — |
| II.7 | NFC solo tras instalar el torno | ID 15, predecesora 13 FC | ✅ | (Se integran los 6 a la vez, al acabar los 3 tornos: es conservador y válido.) | — |
| II.8 | Sin electricidad ni red en los tornos | No hay tareas eléctricas ni de red en el bloque II | ✅ | — | — |
| II.9 | Secuenciación con la misma subcontrata | ID 13 sigue a ID 2 (FC): los operarios terminan los soportes y luego montan los tornos | ✅ | Vínculo de recurso: justificarlo (D-5) | Documentar |

### Bloque III — Infraestructura (pág. 4)

| ID | Requisito | Evidencia | Estado | Error | Corrección |
|---|---|---|---|---|---|
| III.1 | Servidor 4.500 € + Windows Server 870 € + transporte 300 € = 5.670 € | ID 17, Costo fijo = **56,70 €** | ❌ | 100 veces menor | 5.670 |
| III.2 | 6 switches (6.240 €) + 6 patch panels (1.260 €) + armario (740 €) = 8.240 € | ID 18 (hito), Costo fijo = **82,40 €** | ❌ | 100 veces menor | 8.240 |
| III.3 | Puesta a punto del servidor: 2 días | ID 17: 16 h, Rubén Ferrer | ✅ | — | — |
| III.4 | Montaje del armario no duplicado | Solo existe en ID 10 (subcontrata de red) | ✅ | — | — |
| III.5 | Material disponible antes del montaje | ID 18 es predecesora de ID 10 | ✅ | ID 18 lleva la restricción «Debe comenzar el» 17/02, que la marca como crítica sin serlo | Cambiar a «Lo antes posible» |

### Bloque IV — Desarrollo (pág. 4–6)

| ID | Requisito | Evidencia | Estado | Error | Corrección |
|---|---|---|---|---|---|
| IV.1–IV.16 | Trabajo exacto de las tareas 1 a 16 | Las 16 coinciden al minuto (ver la sección D) | ✅ | — | — |
| IV.17 | Roles mínimos respetados | Analistas: Álvaro, Lucía, Diego. Programadores: Diego y Rubén. Supervisores: Álvaro y Lucía. Nadie fuera de sus roles. | ✅ | — | — |
| IV.18 | Reparto por rol: 6 A14/S14, 8 A30/P20, 9 A30/P28, 10 A8/P8/S16, 14 P17/S17 | Coincide exactamente (ver la sección D) | ✅ | — | — |
| IV.19 | Predecesoras 2←1 con solape de 1 día | ID 22: predecesora **1 FC sin adelanto** | ⚠️ | El enunciado dice que «admite» solape; la plantilla espera FC−1 día. No está modelado ni justificado. | FC−1d o justificar (sección G-3) |
| IV.20 | 3←1 | ID 23: predecesoras **1 FC y 2 FC** | ⚠️ | Vínculo 2→3 añadido | Justificar como vínculo de recurso |
| IV.21 | 4←1 | ID 24: predecesoras **1 FC y 3 FC** | ⚠️ | Vínculo 3→4 añadido | Ídem |
| IV.22 | 5←2,3,4 · 6←5 · 7←6 · 8,9←7 · 10←8,9 | Correctos | ✅ | — | — |
| IV.23 | 11←10 · 12←11 · 13←11,12 · 14←13 · 15←14 · 16←15 | Correctos | ✅ | — | — |
| IV.24 | Hitos «cierre del diseño» y «aprobación del sistema» | IDs 32 y 38, duración 0, tras las tareas 10 y 14 | ⚠️ | Existen, pero **no tienen sucesoras**: Project les da 14,56 y 7,25 días de margen y no aparecen en la ruta crítica | Hacer que 11 dependa del hito 32 y 15 del hito 38 |
| IV.25 | Reunión quincenal, lunes laborable, 1 h con todo el equipo | IDs 50, 53, 56, 59: 23/02, 09/03, 23/03 y 06/04, 5 personas × 1 h | ✅ | — | — |
| IV.26 | Jefe de proyecto: 4 h por reunión | Preparación 2 h + reunión 1 h + análisis 1 h = 4 h (Marta, tabla A) | ✅ | — | — |
| IV.27 | Hueco de agenda para la reunión | Calendario de tarea «Personal MEDIATEC (con reuniones)» que bloquea 10:00–11:00 esos lunes | ✅ | Buena técnica | — |

### Bloque V — Instalación y pruebas (pág. 6–7)

| ID | Requisito | Evidencia | Estado | Error | Corrección |
|---|---|---|---|---|---|
| V.1 | 17: 16 h; predecesoras 16 y montaje del servidor | ID 43: 16 h; predecesoras 16 FC y 301 (ID 17) FC | ✅ | — | — |
| V.2 | 18: 24 h; predecesora 17 | ID 44 | ✅ | — | — |
| V.3 | 19: 32 h; predecesoras 18, terminales e integración NFC | ID 45: predecesoras 18, 130 (ID 11) y 203 (ID 15) | ✅ | — | — |
| V.4 | 20: 24 h; predecesora 19 | ID 46 | ✅ | — | — |
| V.5 | Cualquier persona de la plantilla | Álvaro, Lucía, Diego y Rubén (Marta no, para evitar el +20 %) | ✅ | Reparto de 4 personas por tarea: justificarlo | Ver la sección J |

### Bloque VI — Condiciones generales (pág. 7)

| ID | Requisito | Evidencia | Estado | Error | Corrección |
|---|---|---|---|---|---|
| VI.1 | Inicio el 17/02/2026 | Comienzo del proyecto: 17/02/2026 08:00 | ✅ | — | — |
| VI.2 | Calendario de Huelva capital | «Laboral Huelva 2026»: solo 02/04 y 03/04 | ⚠️ | **Correcto dentro del periodo** (el 28/02 cae en sábado y el Decreto 101/2025 no lo traslada; los festivos locales caen fuera del periodo). Pero el calendario anual está incompleto. | Añadir los demás festivos de 2026 |
| VI.3 | Jornada y días no laborables | L–V, 8–12 y 13–17 (8 h); 480 min/día | ✅ | — | — |
| VI.4 | Catering de 275 € por reunión | IDs 50, 53, 56, 59: Costo fijo = **2,75 €** | ❌ | 100 veces menor | 275 |
| VI.5 | +2 % desde el 20/03 | Cambio de tasa con fecha 20/03/2026 en todos los recursos propios (no en los operarios: correcto) | ✅ | — | — |
| VI.6 | +20 % a la JP fuera de su rol | Tabla B de Marta: 34,99 €/h (no usada; correcto, porque Marta solo hace de JP) | ✅ | — | — |
| VI.7 | Fecha límite 22/04 | Fin del plan: 09/04/2026 08:30 | ✅ | — | — |
| VI.8 | Penalización de 560 €/día | No aplica (no hay retraso) | ✅ | Indicarlo en la memoria | — |
| VI.9 | Sergio Ballesteros solo si se justifica | No contratado (no es necesario) | ✅ | Justificar D-2 | — |

### Recursos y tasas (pág. 4–5, 7 y `sueldos.pdf`)

| ID | Requisito | Evidencia | Estado | Observación |
|---|---|---|---|---|
| R.1 | Coste hora = bruto × 1,30 / 1.772 | A: 39.741 × 1,3 / 1.772 = 29,155 → **29,16** ✓. P: 31.122 × 1,3 / 1.772 = 22,832 → **22,83** ✓ | ✅ | Categoría «Analista Programador» y «Programador» de **empresa pequeña**: hay que justificarlo (hipótesis) |
| R.2 | Horas extra individuales | Álvaro 33,24 (+14 %), Marta 35,57 (+22 %), Lucía 34,40 (+18 %), Diego 33,24 (+14 %), Rubén 26,71 (+17 %) | ✅ | — |
| R.3 | Diego +12 % desde el 01/03 | Tasa 32,65 €/h desde el 01/03 y 33,31 €/h desde el 20/03 (1,12 × 1,02, compuesto) | ✅ | Declarar que la subida se aplica de forma compuesta |
| R.4 | Lucía +8 % como supervisora | Tabla B 31,49 €/h, usada en las tareas 10 y 14 | ✅ | En la tarea 6 el supervisor es Álvaro (Lucía, tabla A, hace de analista): coherente, pero el fichero no lo dice en ningún sitio |
| R.5 | Rubén como analista al 150 % | Tabla B 34,25 €/h (no usada: Rubén nunca hace de analista) | ✅ | — |
| R.6 | Marta +20 % fuera de su rol | Tabla B 34,99 €/h (no usada) | ✅ | — |
| R.7 | +2 % el 20/03 | En todas las tablas A y B | ✅ | — |
| R.8 | Sin sobreasignaciones | Sobreasignada = No en los 6 recursos; máximo diario 8 h (operarios: 16 h = 2 × 8) | ✅ | Verificado día a día por COM |
| R.9 | Horas extra ≤ 2,5 h/día | Horas extra = 0 en todo el proyecto | ✅ | Verificado día a día |

### Aspectos técnicos de Project y entregables

| ID | Requisito | Evidencia | Estado | Observación |
|---|---|---|---|---|
| T.1 | Línea base guardada | Hay comienzo y fin previstos por tarea, pero **las tareas resumen y el proyecto no tienen línea base** (Fin previsto = «NOD») y los **costes previstos son 1/100** de los costes de las tareas | ❌ | Volver a guardar la línea base del proyecto completo tras corregir los costes |
| T.2 | Ruta crítica | Calculada, pero «contaminada»: las 12 tareas de reunión y el hito ID 18 aparecen como críticos por su restricción «Debe comenzar el» | ⚠️ | Cambiar las restricciones |
| T.3 | Tipos de tarea | Desarrollo: Trabajo fijo, condicionada por el esfuerzo. Subcontratas: Duración fija sin recursos. | ✅ | Coherente |
| T.4 | Calendario sobrante | Existe «Estándar» (9–13, 15–19), sin uso | ⚠️ | Eliminar o no citar |
| T.5 | Fichero de la Cuestión 2 | No existe | ⚠️ | Si la base ya llega, explicarlo; si no, crearlo |
| T.6 | Memoria PDF | No existe | ❌ | Redactarla con la plantilla |
| T.7 | Capturas | No existen | ❌ | Ver el checklist (sección I) |

### Recuento

- **Filas evaluadas:** 89 (contando IV.1–IV.16 como 16).
- ✅ **66** · ⚠️ **10** · ❌ **13**.
- **Cumplimiento estricto (solo ✅): ≈ 74 %.** Contando cada ⚠️ como medio cumplimiento: **≈ 80 %**.
- Ojo: el peso no es proporcional al número de filas. Un solo ❌ (los costes fijos) invalida el presupuesto entero y la Cuestión 1.

---

# C. Explicación de lo que hace realmente vuestro fichero

## C.1 Qué es MEDIATEC y cuál es el alcance

MEDIATEC debe entregar llave en mano un sistema de control de acceso, aforo y uso de máquinas para un complejo deportivo:

- **Hardware de salas:** 240 puntos de control, cada uno con un soporte, corriente, red y un terminal táctil NFC.
- **Accesos:** 3 tornos con 6 lectores NFC.
- **Infraestructura común:** servidor, armario, switches y patch panels.
- **Software:** una aplicación de escritorio con módulo web, desarrollada por el personal propio.
- **Puesta en marcha:** instalación, carga de datos, pruebas y formación.

## C.2 Estructura (EDT) del fichero: 60 tareas

| WBS | Bloque | Contenido |
|---|---|---|
| 1 | I. Puntos de control | 1.1 Soportes (ID 2) · 1.2 Electricidad (IDs 4–5) · 1.3 Red (IDs 7–10) · 1.4 Terminales (ID 11) |
| 2 | II. Tornos | 2.1 Tornos (ID 13) · 2.2 Barreras (ID 14) · 2.3 NFC (ID 15) |
| 3 | III. Infraestructura | 3.1 Servidor (ID 17) · 3.2 Suministro de armario, switches y patch panels (hito ID 18) |
| 4 | IV. Desarrollo | Análisis (1–6) · Diseño (7–10 + hito «Cierre del diseño») · Construcción (11–14 + hito «Aprobación del sistema») · Pruebas (15–16) |
| 5 | V. Instalación y pruebas | Tareas 17–20 (IDs 43–46) |
| 6 | Hito «Entrega del proyecto» (ID 47) | |
| 7 | Reuniones (IDs 49–60) | 4 reuniones × (preparación JP 2 h + reunión 1 h + análisis JP 1 h) |

## C.3 Cómo calcula Project duraciones y fechas en vuestro fichero

Casi todas las tareas con recursos son de tipo **Trabajo fijo** y **condicionadas por el esfuerzo**. Esto significa:

> **Duración = Trabajo / (número de personas × unidades) / 8 h**

Ejemplo, **tarea 1 «Definición del sistema» (ID 21)**: 88 h repartidas entre Álvaro, Lucía y Diego al 100 % → 29,33 h cada uno → **3,67 días** (17/02 08:00 → 20/02 14:20). Si la hiciera un solo analista, serían **11 días**.

Las tareas de subcontrata (electricidad y red) son de **Duración fija**, sin recursos, y solo llevan un coste fijo.

Los soportes: 240 × 0,5 h = 120 h de trabajo; con los 2 operarios (200 %) salen 60 h = **7,5 días** (17/02 → 26/02 12:00).

## C.4 Recorrido cronológico real del plan

| Fecha | Qué ocurre |
|---|---|
| 17–18/02 | Rubén monta el servidor (ID 17). Los operarios empiezan los soportes. Álvaro, Lucía y Diego empiezan la definición del sistema (ID 21). |
| 20/02 14:20 | Termina la definición y empieza Requisitos (sin solape). |
| 23/02 | Reunión 1 (de 10 a 11). Marta prepara de 8 a 10 y analiza de 11 a 12. |
| 26/02 12:00 | Terminan los soportes. Los operarios pasan a los tornos (26/02 13:00 → 02/03 12:00) y a las barreras (02/03 → 03/03). |
| 27/02 13:00 | Pasado el día de soldadura, arrancan **en paralelo** la electricidad (→ 10/03) y la red (→ 16/03). |
| 02–03/03 | Rubén integra los 6 NFC de los tornos. |
| 06/03 16:40 | Termina el análisis (aprobación, tarea 6). |
| 17/03 10:00 | Termina la verificación del diseño → hito «Cierre del diseño». Arrancan la codificación (Diego + Rubén) y el montaje de terminales (Álvaro + Lucía, 17–20/03). |
| 26/03 14:30 | Hito «Aprobación del sistema». |
| 01/04 16:30 | Terminan las pruebas de integración (16). |
| 02–03/04 | Jueves y Viernes Santo (festivos). |
| 06/04 | Reunión 4; tareas 17 y 18. |
| 07–08/04 | Tarea 19 (pruebas en el cliente). |
| **09/04 08:30** | **Termina la tarea 20 → Entrega del proyecto.** |

## C.5 Qué se ejecuta en paralelo

- **Hardware y software avanzan en paralelo** desde el primer día. Todo el hardware (bloques I–III) termina el 20/03, con un margen de entre 9 y 30 días sobre la entrega.
- Electricidad y red van en paralelo entre sí.
- Las tareas 8 y 9 (diseño de clases y de datos) van en paralelo.
- En las tareas 1–7 y 17–20 trabajan varias personas **a la vez sobre la misma tarea**, que se acorta en proporción.

## C.6 Ruta crítica real

La cadena que determina la fecha de fin (margen total 0) es:

**1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 y 9 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → Entrega.**

Es decir, **todo el desarrollo de software más la instalación final**. El hardware no es crítico.

Matices:

- 3 y 4 están en la ruta crítica solo porque habéis añadido los vínculos 2→3 y 3→4. Según el enunciado, 2, 3 y 4 podrían ir en paralelo.
- Las reuniones y el hito «Suministro…» (ID 18) aparecen como críticos **por sus restricciones «Debe comenzar el»**, no porque condicionen la fecha. Es ruido visual.
- Los hitos «Cierre del diseño» y «Aprobación del sistema» **no aparecen como críticos** porque nada depende de ellos.

## C.7 Recursos y por qué está asignado cada uno

| Recurso | Qué hace en el plan | Lógica |
|---|---|---|
| Álvaro Nieto (A, S) | Análisis 1–7, diseño 8 (A), supervisión en 6, 10 y 14, terminales, 17–20 | Analista y supervisor sin recargo de rol |
| Lucía Prieto (A, S) | Análisis 1–7, diseño 9 (A), supervisión en 10 y 14 (tabla B, +8 %), terminales, 17–20 | Hace de supervisora solo en 10 y 14 (en 6 lo hace Álvaro) |
| Diego Manzano (A, P) | Análisis 1–5 y 7, programador en 9, analista en 10, programador en 11–16, 17–20 | Es el «comodín» y el **recurso cuello de botella**: está al 100 % casi todos los días |
| Rubén Ferrer (P, A) | Servidor, NFC, P en 8 y 10, programación 11–16, 17–20 | Nunca hace de analista (evita el 150 %) |
| Marta Salas (JP, A) | Solo reuniones (16 h) | Evita el +20 % fuera de su rol |
| Operarios (subcontrata) | Soportes, tornos, barreras | 2 operarios al 200 % |

## C.8 Cómo se calculan los costes en el fichero

- **Personal:** horas × tasa vigente en la fecha y en la tabla de la asignación. Ejemplo: en la tarea 4, el coste de Diego (574,90 €) mezcla su tasa anterior y la posterior al 01/03.
- **Materiales, subcontratas y catering:** como **Costo fijo** de la tarea, acumulado al final. Es un método válido, pero **todos los importes están a 1/100**.

## C.9 Diagrama de Gantt, hitos y línea base

- El **Gantt** muestra cada tarea como una barra en el tiempo. Las flechas son los vínculos y las barras rojas (con el formato de ruta crítica activado), las tareas con margen 0.
- Un **hito** es una tarea de duración 0 que marca un evento (cierre del diseño, aprobación, entrega).
- La **línea base** es una «foto» del plan aprobado, que sirve para comparar después (Gantt de seguimiento). En vuestro fichero está **incompleta**: solo existe por tarea, con costes erróneos, y no hay línea base del proyecto.

---

# D. Auditoría de tareas

## D.1 Las 20 tareas de desarrollo, instalación y pruebas

Duración en días de 8 h. Coste tal como lo calcula Project (en estas tareas no hay costes fijos, así que el coste es correcto).

| # | ID | Trabajo enunciado / MPP | Predecesoras enunciado → MPP | Roles exigidos → asignación en el MPP | Duración | Fechas | Coste | Resultado |
|---|---|---|---|---|---|---|---|---|
| 1 | 21 | 88 / 88 | — → — | A → Álvaro, Lucía, Diego (29,33 h c/u) | 3,67 d | 17/02–20/02 | 2.566,08 € | ✅ |
| 2 | 22 | 48 / 48 | 1 (solape 1 d) → **1 FC** | A → 3 analistas, 16 h c/u | 2 d | 20/02–24/02 | 1.399,68 € | ⚠️ falta el solape o su justificación |
| 3 | 23 | 66 / 66 | 1 → **1, 2** | A → 3 analistas, 22 h c/u | 2,75 d | 24/02–27/02 | 1.924,56 € | ⚠️ vínculo añadido |
| 4 | 24 | 54 / 54 | 1 → **1, 3** | A → 3 analistas, 18 h c/u | 2,25 d | 27/02–03/03 | 1.624,66 € | ⚠️ vínculo añadido |
| 5 | 25 | 34 / 34 | 2,3,4 → 2,3,4 | A → 3 analistas, 11,33 h c/u | 1,42 d | 03/03–05/03 | 1.030,99 € | ✅ |
| 6 | 26 | 28 / 28 | 5 → 5 | A14 + S14 → Lucía 14 (A) + Álvaro 14 (S) | 1,75 d | 05/03–06/03 | 816,48 € | ✅ (documentad quién es S) |
| 7 | 28 | 34 / 34 | 6 → 6 | A → 3 analistas, 11,33 h c/u | 1,42 d | 06/03–10/03 | 1.030,99 € | ✅ |
| 8 | 29 | 50 / 50 | 7 → 7 | A30 + P20 → Álvaro 30 + Rubén 20 | 3,75 d | 10/03–16/03 | 1.331,40 € | ✅ |
| 9 | 30 | 58 / 58 | 7 → 7 | A30 + P28 → Lucía 30 + Diego 28 | 3,75 d | 10/03–16/03 | 1.789,00 € | ✅ |
| 10 | 31 | 32 / 32 | 8,9 → 8,9 | A8 + P8 + S16 → Diego 8 (A), Rubén 8 (P), Álvaro 8 + Lucía 8 (S, tabla B) | 1 d | 16/03–17/03 | 929,04 € | ✅ |
| 11 | 34 | 44 / 44 | 10 → 10 | P → Diego + Rubén, 22 h c/u | 2,75 d | 17/03–19/03 | 1.220,56 € | ✅ |
| 12 | 35 | 26 / 26 | 11 → 11 | P → Diego + Rubén, 13 h c/u | 1,63 d | 20/03–23/03 | 735,80 € | ✅ |
| 13 | 36 | 30 / 30 | 11,12 → 11,12 | P → Diego + Rubén, 15 h c/u | 1,88 d | 23/03–25/03 | 849,00 € | ✅ |
| 14 | 37 | 34 / 34 | 13 → 13 | P17 + S17 → Diego 8,5 + Rubén 8,5 (P), Álvaro 8,5 + Lucía 8,5 (S, B) | 1,06 d | 25/03–26/03 | 1.006,91 € | ✅ |
| 15 | 40 | 40 / 40 | 14 → 14 | P → Diego + Rubén, 20 h c/u | 2,5 d | 26/03–31/03 | 1.132,00 € | ✅ |
| 16 | 41 | 28 / 28 | 15 → 15 | P → Diego + Rubén, 14 h c/u | 1,75 d | 31/03–01/04 | 792,40 € | ✅ |
| 17 | 43 | 16 / 16 | 16 + servidor → 16, ID 17 | Cualquiera → 4 personas × 4 h | 0,5 d (se extiende por los festivos) | 01/04–06/04 | 464,32 € | ✅ |
| 18 | 44 | 24 / 24 | 17 → 17 | Cualquiera → 4 × 6 h | 0,75 d | 06/04–07/04 | 696,48 € | ✅ |
| 19 | 45 | 32 / 32 | 18 + terminales + NFC → 18, ID 11, ID 15 | Cualquiera → 4 × 8 h | 1 d | 07/04–08/04 | 928,64 € | ✅ |
| 20 | 46 | 24 / 24 | 19 → 19 | Cualquiera → 4 × 6 h | 0,75 d | 08/04–09/04 | 696,48 € | ✅ |

Las horas suman **694 h** en las tareas 1–16 y **96 h** en las 17–20, exactamente lo que pide el enunciado.

## D.2 Instalaciones y equipamiento

| ID | Tarea | Duración | Recursos | Predecesoras | Costo fijo en el MPP → correcto | Margen total | Resultado |
|---|---|---|---|---|---|---|---|
| 2 | Soportes 240 uds. | 7,5 d | Operarios 200 % (120 h) | — | 19,68 → **1.968** | 9,94 d | ❌ coste |
| 4 | Cables eléctricos | 5 d | — | 2 FC+1 d | 9,20 → **920** | 13,94 d | ❌ coste |
| 5 | Puntos de corriente | 2 d | — | 4 | 3,40 → **340** | 13,94 d | ❌ coste |
| 7 | Canaletas | 2 d | — | 2 FC+1 d | 2,30 → **230** | 9,94 d | ❌ coste |
| 8 | Cables de red | 4 d | — | 7 | 6,40 → **640** | 9,94 d | ❌ coste |
| 9 | Tomas de red | 3 d | — | 8 | 5,80 → **580** | 9,94 d | ❌ coste |
| 10 | Armario, pruebas y certificación | 2 d | — | 9, 18 | 4,60 → **460** | 9,94 d | ❌ coste |
| 11 | Terminales y cierre | 3,75 d | Álvaro + Lucía (60 h) | 5, 10 y **tarea 10 de desarrollo** | 105,60 → **10.560** | 9,06 d | ❌ coste · ⚠️ vínculo |
| 13 | Tornos | 2 d | Operarios 200 % | 2 | 55,50 → **5.550** | 22,69 d | ❌ coste |
| 14 | Barreras | 1 d | Operarios 200 % | 13 | 8,80 → **880** | 24,56 d | ❌ coste |
| 15 | NFC tornos | 1 d | Rubén | 13 | 55,20 → **5.520** | 22,44 d | ❌ coste |
| 17 | Servidor | 2 d | Rubén | — | 56,70 → **5.670** | 29,56 d | ❌ coste |
| 18 | Suministro de armario, switches y PP | hito | — | restricción «Debe comenzar el» 17/02 | 82,40 → **8.240** | 0 (artificial) | ❌ coste · ⚠️ restricción |

---

# E. Auditoría de costes

## E.1 Coste hora (recalculado)

Fórmula: **Coste hora = Bruto anual × 1,30 / 1.772**. Fuente: `sueldos.pdf`, pág. 3, tabla «Niveles retributivos», columna **Pequeña**.

| Categoría | Bruto (pequeña) | × 1,30 | ÷ 1.772 | En el MPP |
|---|---|---|---|---|
| A (Analista Programador) | 39.741 € | 51.663,30 € | **29,1554 €/h** | 29,16 ✅ |
| P (Programador) | 31.122 € | 40.458,60 € | **22,8322 €/h** | 22,83 ✅ |

**Supuesto que debéis declarar:** se ha usado la columna de empresa **pequeña** (facturación inferior a 6 M€, según la nota 2 del PDF). Si MEDIATEC fuera **mediana**, A = 42.244 € → 30,99 €/h y P = 41.615 € → 30,53 €/h. Eso cambia todo el coste de personal (en torno a un +14 % para A y un +34 % para P). No es un error, pero **es una hipótesis que la plantilla obliga a declarar** (apartado 3).

## E.2 Tasas aplicadas (antes del 20/03 → desde el 20/03)

| Persona y tabla | Estándar | H. extra | Cálculo |
|---|---|---|---|
| Álvaro A | 29,16 → 29,74 | 33,24 → 33,90 | ×1,14 |
| Marta A (JP) | 29,16 → 29,74 | 35,57 → 36,28 | ×1,22 |
| Marta B (fuera de su rol) | 34,99 → 35,69 | 42,68 → 43,54 | ×1,20, luego ×1,22 |
| Lucía A | 29,16 → 29,74 | 34,40 → 35,09 | ×1,18 |
| Lucía B (supervisora) | 31,49 → 32,12 | 37,16 → 37,90 | ×1,08, luego ×1,18 |
| Diego | 29,16 → (01/03) 32,65 → (20/03) 33,31 | 33,24 → 37,23 → 37,97 | ×1,12, luego ×1,02 (compuesto) |
| Rubén A (programador) | 22,83 → 23,29 | 26,71 → 27,25 | ×1,17 |
| Rubén B (analista) | 34,25 → 34,93 | 40,07 → 40,87 | ×1,5, luego ×1,17 |
| Operarios | 34,00 | 44,20 | ×1,30 (sin subida del 2 %) |

Todas son correctas.

- **Bases aplicadas:** los recargos se aplican sobre la tasa ya modificada por el rol, nunca sumando porcentajes. Por ejemplo, Lucía como supervisora en hora extra: 29,16 × 1,08 × 1,18. Es la interpretación más defendible; declaradla.
- **Diego:** 1,12 × 1,02 = 1,1424, no 1,14. Declaradlo también.

## E.3 Presupuesto recalculado desde cero

| # | Partida | Cálculo | Importe correcto | En el MPP |
|---|---|---|---|---|
| 1 | Personal propio, jornada normal | Álvaro 6.629,39 + Marta 471,20 + Lucía 6.668,26 + Diego 8.448,34 + Rubén 3.982,57 (independiente: 26.200,03) | **26.199,75 €** | 26.199,75 ✅ |
| | ↳ de ello, en reuniones | 4 reuniones (personal) | 927,47 € | ✅ |
| 2 | Horas extra | 0 h | **0,00 €** | 0 ✅ |
| 3 | Subcontrata de estructuras metálicas | 120 h + 32 h + 16 h = 168 h × 34 € | **5.712,00 €** | 5.712 ✅ |
| 4 | Materiales y equipos | Soportes 1.968 + terminales 10.560 + tornos 5.550 + barreras 880 + NFC 5.520 + servidor 4.500 + Windows Server 870 + switches 6.240 + patch panels 1.260 + armario 740 | **38.088,00 €** | 380,88 ❌ |
| 5 | Instalaciones eléctrica y de red | 920 + 340 + 230 + 640 + 580 + 460 | **3.170,00 €** | 31,70 ❌ |
| 6 | Catering de reuniones | 4 × 275 | **1.100,00 €** | 11,00 ❌ |
| 7 | Transporte especial del servidor | 300 | **300,00 €** | 3,00 ❌ |
| 8 | Penalizaciones | 0 días de retraso | **0,00 €** | — |
| | **COSTE TOTAL** | | **74.569,75 €** | **32.338,33 €** ❌ |

**Diferencia: 42.231,42 €.** Equivale exactamente a los 42.658 € de costes fijos menos los 426,58 € que Project sí cuenta: todos los costes fijos están divididos entre 100. Las notas de cada tarea («Coste fijo = Soporte metálico 240 x 8.20 €») muestran que la intención era correcta. El valor introducido en el campo *Costo fijo* no lo es.

### Desglose por bloques (corregido)

| Bloque | Coste correcto |
|---|---|
| I. Puntos de control | 21.536,88 € |
| II. Tornos | 13.764,64 € |
| III. Infraestructura | 14.275,28 € |
| IV. Desarrollo (1–16) | 20.179,56 € |
| V. Instalación y pruebas (17–20) | 2.785,92 € |
| Reuniones (personal + catering) | 2.027,47 € |
| **Total** | **74.569,75 €** |

## E.4 Beneficio del 20 % (decisión D-7)

| Interpretación | Fórmula | Con el coste correcto | Con el coste erróneo del MPP |
|---|---|---|---|
| Sobre el coste (mark-up) | Coste × 1,20 | **89.483,70 €** (beneficio 14.913,95 €) | 38.806,00 € |
| Sobre el precio (margen) | Coste ÷ 0,80 | **93.212,19 €** (beneficio 18.642,44 €) | 40.422,91 € |

- La diferencia entre ambas interpretaciones es de **3.728,49 €**. El fichero no indica cuál se adopta (no le corresponde: va en la memoria).
- **Consecuencia del error:** si ofertarais 38.806 € a partir del MPP actual, el proyecto tendría una **pérdida de 35.763,75 €**, en lugar de un beneficio.

---

# F. Lista priorizada de errores

| Prioridad | Código | Hallazgo |
|---|---|---|
| **CRÍTICO** | F-1 | Los 14 costes fijos (materiales, subcontratas, transporte y catering) están introducidos a 1/100. Coste total 32.338,33 € en lugar de 74.569,75 €. Invalida el presupuesto y la Cuestión 1. |
| **CRÍTICO** | F-2 | No hay memoria ni respuesta documentada a las Cuestiones 1 y 2 (el enunciado exige el ZIP con memoria PDF, pág. 7). |
| **ALTO** | F-3 | Línea base incompleta: no existe a nivel de proyecto ni de tareas resumen, y los costes previstos están a 1/100. La «Gantt de seguimiento» y las estadísticas no sirven. |
| **ALTO** | F-4 | La hipótesis de reparto del trabajo (3 analistas por tarea, 2 programadores, 4 personas en 17–20) es la que hace que el plan llegue al 09/04. No está declarada ni justificada, y contradice lo que la plantilla da por hecho (A0 «No llega al 13 de abril»). Ver la sección J. |
| **MEDIO** | F-5 | Solape de requisitos (2 ← 1 FC−1 d) no modelado ni justificado. |
| **MEDIO** | F-6 | Vínculos que no están en el enunciado: 2→3, 3→4 y tarea 10 → terminales. Son vínculos «de recurso» sin justificar. |
| **MEDIO** | F-7 | Los hitos «Cierre del diseño» y «Aprobación del sistema» no tienen sucesoras: quedan fuera de la ruta crítica (margen de 14,56 y 7,25 días). |
| **MEDIO** | F-8 | Restricciones «Debe comenzar el» en las reuniones y en ID 18: aparecen como falsas tareas críticas. |
| **MEDIO** | F-9 | Hipótesis salariales sin declarar: empresa pequeña, «Analista Programador» como categoría A, subida compuesta en Diego, quién supervisa en la tarea 6. |
| **BAJO** | F-10 | El calendario de Huelva 2026 solo contiene los festivos del periodo; faltan los del resto del año (incluidos los locales). Sobra el calendario «Estándar». |
| **BAJO** | F-11 | Decisiones D-3 (cierre en bloque de terminales) y D-5 (orden de las subcontratas) correctas, pero sin justificar. |

---

# G. Correcciones paso a paso

> Haced todas las correcciones en una **copia** (por ejemplo `Practica1_Base.mpp`) y conservad el original.

### G-1 (CRÍTICO) Costes fijos ×100

1. **Situación actual:** el campo *Costo fijo* contiene, por ejemplo, 19,68 € en los soportes.
2. **Por qué está mal:** el enunciado dice 8,20 €/ud × 240 = 1.968 € (pág. 2). Lo mismo ocurre con todas las demás partidas.
3. **Qué exige el enunciado:** los importes de las págs. 2, 3, 4 y 7.
4. **Qué cambiar:** los 14 valores de la tabla.
5. **Cómo hacerlo en Project:** *Vista → Diagrama de Gantt → Vista → Tablas → Costo*. En la columna **Costo fijo**, escribid:

   | ID | Valor |
   |---|---|
   | 2 | 1968 |
   | 4 | 920 |
   | 5 | 340 |
   | 7 | 230 |
   | 8 | 640 |
   | 9 | 580 |
   | 10 | 460 |
   | 11 | 10560 |
   | 13 | 5550 |
   | 14 | 880 |
   | 15 | 5520 |
   | 17 | 5670 |
   | 18 | 8240 |
   | 50, 53, 56, 59 | 275 cada una |

6. **Resultado esperado:** la columna **Costo total** de la tarea resumen del proyecto (ID 0; activadla en *Formato → Tarea de resumen del proyecto*) debe mostrar **74.569,75 €**.
7. **Cómo comprobarlo:** *Proyecto → Información del proyecto → Estadísticas* → Costo actual = 74.569,75 €. Las fechas no deben cambiar (el coste no afecta a la programación).

### G-2 (ALTO) Línea base

1. **Situación actual:** línea base parcial, con costes a 1/100 y sin línea base de proyecto.
2. **Corrección:** después de G-1 y del resto de cambios de planificación, *Proyecto → Establecer línea base → Establecer línea base… → Línea base → **Proyecto completo***. Aceptad sobrescribir.
3. **Cómo comprobarlo:** en *Estadísticas*, la fila «Previsto» debe mostrar comienzo 17/02, fin igual al plan y costo igual al actual. En *Gantt de seguimiento*, las barras grises deben coincidir con las azules o rojas.

### G-3 (MEDIO) Solape 2 ← 1

1. **Situación actual:** 2 ← 1 FC, sin adelanto.
2. **Qué dice el enunciado:** «puede arrancar un día antes» (pág. 6). Es un permiso, no una obligación, pero la plantilla lo da por modelado.
3. **Opción A (modelar):** doble clic en el ID 22 → *Predecesoras* → en la fila 1, *Posposición* = **−1d**.

   Al hacerlo, Álvaro, Lucía y Diego quedan sobreasignados el último día de la tarea 1. Hay que resolverlo:
   - con *Redistribuir → Redistribuir todo*, o
   - cambiando el reparto: por ejemplo, la tarea 1 la hacen dos analistas y uno entra antes en Requisitos.

   Comprobad que *Sobreasignada = No* en la Hoja de recursos.
4. **Opción B (no modelar):** dejar FC y escribir en el apartado 3 de la memoria que, como las tareas 1 y 2 las hacen las mismas tres personas, el solape no acorta nada sin sobreasignarlas.
5. **Cómo comprobarlo:** la fecha de fin se adelanta como mucho unas horas. Documentad el resultado.

### G-4 (MEDIO) Vínculos que no están en el enunciado

1. **Situación actual:** 2→3, 3→4 y 10 (desarrollo) → ID 11.
2. **Por qué es un problema:** el enunciado solo pide 3←1 y 4←1, y la tarea 11 de hardware no depende del diseño. Un vínculo sin explicar se corrige como error de dependencias.
3. **Corrección:** mantenedlos, pero **justificados** como vínculos de recurso. El mismo equipo de 3 analistas hace 2, 3 y 4 de forma consecutiva: 168 h / 3 = 7 días, frente a 8,25 días si cada analista hiciera una tarea en paralelo (la de 66 h marca el ritmo). Es decir, vuestro orden es **más rápido**.

   Escribidlo en *Información de la tarea → Notas* y en el apartado 5.2 de la memoria. La alternativa es borrarlos y usar *Redistribuir*.
4. **Cómo comprobarlo:** cada vínculo de la columna Predecesoras está en el enunciado o en la tabla 5.2 de la memoria.

### G-5 (MEDIO) Hitos en la cadena

1. En la tarea 11 de desarrollo (ID 34), cambiad la predecesora «31» (tarea 10) por «32» (hito Cierre del diseño).
2. En la tarea 15 (ID 40), cambiad «37» por «38» (hito Aprobación del sistema).
3. **Resultado esperado:** ambos hitos aparecen en rojo (críticos), con margen 0, y las fechas no cambian.

### G-6 (MEDIO) Restricciones que ensucian la ruta crítica

1. **ID 18:** *Información de la tarea → Avanzado → Tipo de restricción* = **Lo antes posible**.
2. **Reuniones (IDs 49–60):** cambiad «Debe comenzar el» por **«No comenzar antes del»** con la misma fecha. Como no tienen predecesoras, se quedan en la misma fecha pero dejan de ser críticas.
3. **Cómo comprobarlo:** *Formato → Tareas críticas* resalta solo la cadena 1…20 y la Entrega.

### G-7 (BAJO) Calendario

En *Proyecto → Cambiar tiempo de trabajo → «Laboral Huelva 2026» → Excepciones*, añadid los festivos que faltan:

- 01/01, 06/01, 28/02 (sábado), 01/05, 15/08 (sábado), 12/10, 02/11, 07/12, 08/12 y 25/12 (Decreto 101/2025, BOJA nº 93).
- Los dos festivos locales de Huelva capital, una vez confirmados en la resolución oficial de fiestas locales de 2026 (las fuentes no oficiales indican el 03/08 y el 08/09).

Copiad las mismas excepciones al calendario «Personal MEDIATEC (con reuniones)» y eliminad «Estándar». Dentro del periodo del proyecto no cambia nada, pero queda completo.

### G-8 (ALTO) Declarar y justificar la hipótesis de reparto

Ver la sección J. Debe ir en el apartado 3 (hipótesis) y en la decisión D-4 de la memoria.

### G-9 (CRÍTICO) Memoria y Cuestiones

Redactad la memoria con la plantilla, usando las cifras **corregidas**. Ver las secciones H e I.

---

# H. Guion para defender el proyecto (10–15 min)

## 1. Contexto (1 min)

MEDIATEC debe entregar llave en mano el sistema: hardware de 240 puntos, 3 tornos, servidor y red, y una aplicación a medida. El plazo contractual es el 22/04/2026, con una penalización de 560 € por día de retraso.

## 2. Idea central de la planificación (2 min)

- El hardware lo ejecutan sobre todo subcontratas, con duraciones y costes cerrados.
- El software lo hace el equipo propio a partir de **horas de trabajo**, no de días.
- Por eso el proyecto tiene dos caminos en paralelo, y el que manda es el del **software**: 790 h de trabajo frente a unos 22 días laborables de hardware.

## 3. Hardware (3 min)

- **Soportes:** 240 × 30 min = 120 h; con 2 operarios, 7,5 días.
- **Soldadura:** vínculo FC + 1 día hacia electricidad y red.
- **Electricidad y red** van en paralelo; cada una es secuencial por dentro.
- **Terminales:** 60 h con 2 personas, cuando hay corriente y red.
- **Tornos:** los mismos operarios, al terminar los soportes.
- Todo el hardware tiene más de 9 días de margen, así que **no es crítico**. Por eso no adelantamos el cierre progresivo de terminales: complicaría coordinar tres empresas sin ganar ni un día.

## 4. Software (4 min)

- Tareas de Trabajo fijo: la duración resulta de las horas y del número de personas.
- **Reparto:**
  - Análisis con los 3 analistas sin recargo (Álvaro, Lucía, Diego).
  - Construcción con los 2 programadores (Diego y Rubén, que es el más barato).
  - Supervisión de Álvaro (sin plus) en la tarea 6 y de Lucía (+8 %) en las 10 y 14, porque S16 y S17 necesitan dos supervisores para no alargar la tarea.
  - Marta solo como JP, para evitar su +20 %. Rubén nunca como analista, para evitar su 150 %.
- **Ruta crítica:** de la tarea 1 a la 20, todo el desarrollo y la instalación.

## 5. Costes (2 min)

- Coste hora = bruto × 1,3 / 1.772. Hemos tomado la categoría de empresa pequeña.
- Cambios de tasa con fecha: Diego el 01/03 y todos el 20/03. Tablas B para los cambios de rol.
- Total: **74.569,75 €**. Materiales y equipos suponen el 51 %, el personal propio el 35 %, y las subcontratas, el catering y el transporte, el resto.

## 6. Cuestiones (2 min)

- **Cuestión 1:** fin el 09/04, sin penalización. Oferta de 89.483,70 € (coste × 1,2) o 93.212,19 € (coste / 0,8), según la interpretación declarada. La fecha comprometida se elige entre el 09/04 y el 22/04, con colchón justificado.
- **Cuestión 2:** sí, el 13/04 se cumple sin horas extra, con unos 2,9 días laborables de margen, gracias al reparto del trabajo entre varias personas.

## Preguntas probables del profesor

| Pregunta | Respuesta fundamentada |
|---|---|
| «¿Por qué tu escenario base ya llega al 13 de abril? ¿No es sospechoso?» | Porque el enunciado da trabajo total y roles **mínimos**, así que asignamos a todas las personas compatibles. Sin horas extra ni sobreasignaciones (comprobado día a día). Si cada tarea la hiciera una sola persona por rol, el plan acabaría hacia el 28/05 (estimación manual). Esa es la sensibilidad clave. |
| «¿Tres personas hacen 88 h en un tercio del tiempo? ¿Y la comunicación?» | Es una simplificación (ley de Brooks). La mitigamos porque son tareas de análisis repartibles y el equipo es pequeño y con experiencia (pág. 5: «permite ajustar con holgura las estimaciones»). Además, hay 9 días laborables de colchón hasta el 22/04. |
| «¿Por qué Requisitos no arranca un día antes?» | (Según la opción elegida en G-3.) |
| «¿Por qué 3 depende de 2 si el enunciado no lo dice?» | Es un vínculo de recurso: el mismo equipo hace 2, 3 y 4 en serie, y eso tarda 7 días frente a 8,25 en paralelo. |
| «¿Quién es supervisor en la tarea 6 y por qué?» | Álvaro, porque no tiene plus. Lucía cobraría un 8 % más. |
| «¿Cómo modelas los materiales?» | Como costo fijo de la tarea donde se consumen, acumulado al final. |
| «¿Qué pasa si el electricista se retrasa 5 días?» | La red tiene 9,9 días de margen y la electricidad 13,9, así que la entrega no se mueve. |
| «¿Cuánto cuesta un día de retraso frente a acelerar?» | 560 € por día de penalización, frente al coste de horas extra (por ejemplo, Diego y Rubén 2,5 h × 37,97 + 2,5 h × 27,25 ≈ 163 €/día). |
| «¿Por qué no contratáis a Sergio?» | El plan ya llega al 13/04; contratarlo solo añadiría coste. |
| «¿Qué representa la línea base?» | La foto del plan aprobado: sirve para medir desviaciones en el seguimiento. |

---

# I. Checklist final de entrega (ZIP)

| Elemento | Estado | Qué falta |
|---|---|---|
| `Practica1_Base.mpp` corregido (costes, vínculos, hitos, restricciones, calendario, línea base) | ⚠️ | Correcciones G-1 a G-7 |
| `Practica1_C1_Oferta.mpp` | Opcional | Solo si la fecha comprometida o el plan ofertado difieren de la base |
| `Practica1_C2_Acelerado.mpp` | ⚠️ | Si la base ya llega al 13/04, no hace falta acelerar: explicadlo. Si cambiáis la hipótesis de reparto y la base deja de llegar, este fichero es **obligatorio** (A1–A4). |
| `Calculos_Practica1.xlsx` (opcional) | ❌ | Coste hora, materiales, comparativa de alternativas |
| Memoria PDF (apartados 1–10) | ❌ | Toda |
| Capturas: Gantt con ruta crítica, Hoja de recursos, Tablas de tasas A/B, Uso de recursos diario (horas extra), Estadísticas, Costos, Calendario | ❌ | Todas, numeradas y legibles |
| Grupo (3–4 miembros) y reparto del trabajo | ❌ | Apartado 10 |

---

# J. La duda sobre el 13 de abril

## J.1 ¿Es matemáticamente posible terminar antes del 13/04 sin horas extra?

**Sí, con vuestra hipótesis de asignación, y lo he verificado:**

- Las horas de las 20 tareas coinciden al minuto con el enunciado.
- No hay sobreasignaciones. El trabajo diario de cada persona se ha leído día a día de Project: máximo 8 h por persona y 16 h para los 2 operarios.
- Las horas extra son 0 en todo el proyecto.
- El calendario es correcto en el periodo (Decreto 101/2025: el 28/02 cae en sábado y no se traslada; el 02/04 y el 03/04 son festivos).
- Las dependencias del enunciado se respetan todas. Las diferencias que hay (sin solape en 2←1, vínculos 2→3 y 3→4, terminales←10) **retrasan** el plan, no lo adelantan.
- El error de costes ×1/100 **no afecta** a las fechas.

**No he encontrado ningún error oculto que adelante artificialmente la fecha.** Días laborables disponibles: del 17/02 al 13/04 hay 38, y del 17/02 al 22/04 hay 45. El plan usa 35,06.

## J.2 ¿Por qué entonces termina tan pronto?

Por **una sola decisión de modelado**: cada tarea la hacen **todas** las personas compatibles a la vez, y Project divide la duración entre ellas.

| Tramo | Horas | Personas en el MPP | Días en el MPP | Con 1 persona por rol (estimación) |
|---|---|---|---|---|
| Análisis (1–6) | 318 | 3 analistas | 13,96 | ≈ 26 |
| Diseño (7–10) | 174 | 2–4 | 6,3 | ≈ 10 |
| Construcción (11–14) | 134 | 2–4 | 7,4 | ≈ 14,6 |
| Pruebas (15–16) | 68 | 2 | 4,25 | 8,5 |
| Instalación (17–20) | 96 | 4 | ≈ 3 | 12 |

Con «una persona por rol mínimo» (paralelizando solo lo que el enunciado permite), la cadena crítica sale de unos **70,4 días laborables**, lo que llevaría el fin hacia el **28/05/2026**. Es un cálculo manual que **no incluye las reuniones**, así que tomadlo solo como orden de magnitud. Esa fecha está más allá del 22/04 incluso con 2,5 h extra al día.

La «verdad» depende de la hipótesis. El enunciado no prohíbe asignar a más personas: habla de «roles **mínimos** que deben intervenir». Pero la plantilla da dos pistas de que el profesor podría esperar algo intermedio:

1. La fila **A0 del apartado 7.2** está rellenada de antemano con «No llega al 13 de abril».
2. En **D-2** dice: «Las tareas secuenciales de una sola persona no se dividen por tener dos».

Son pistas, no reglas. No puedo afirmar cuál es la solución de referencia del profesor.

## J.3 ¿Es razonable vuestro resultado?

**Es válido y defendible, pero optimista.** Además, ni siquiera es el máximo posible: Rubén está libre muchos días (del 19/02 al 09/03) y Marta casi siempre. El fin depende casi por completo de cuántas personas se asignan por tarea.

## J.4 Recomendación

1. **Mantened el plan** si lo podéis defender, pero **declarad la hipótesis** en el apartado 3: «el trabajo de cada tarea es divisible entre todas las personas con rol compatible, sin pérdida por coordinación». Justificadla en D-4 con cifras: sin el reparto, el fin sería hacia finales de mayo.
2. Añadid un **análisis de sensibilidad** en la memoria, o mejor un segundo `.mpp`, con una hipótesis más conservadora (por ejemplo, como máximo 2 personas por tarea). Así demostráis que habéis evaluado el riesgo, y si ese escenario no llega al 13/04, tenéis un caso real donde aplicar A1–A4.
3. **Preguntad al profesor** qué hipótesis espera. Es una ambigüedad legítima del enunciado.

---

## Respuestas directas

1. **¿Está bien realizado?** Parcialmente. La planificación y las tasas son de buen nivel; los costes fijos son erróneos y falta toda la documentación.
2. **¿Qué porcentaje de requisitos cumple?** Un 74 % estricto (66 de 89), o un 80 % contando los parciales como medio cumplimiento.
3. **¿Qué está completamente correcto?** Horas y roles de las 20 tareas, tasas y tablas A/B, variaciones salariales con fecha, calendario dentro del periodo, reuniones (horas), dependencias del hardware y de las tareas 5–20, ausencia de sobreasignaciones y de horas extra.
4. **¿Qué está mal?** Los 14 costes fijos (÷100), la línea base, los vínculos y el solape sin justificar, los hitos sin sucesoras y las restricciones que ensucian la ruta crítica.
5. **¿Qué falta?** La memoria, las capturas, la justificación de las decisiones D-1 a D-7, la declaración de hipótesis y el análisis de la Cuestión 2.
6. **¿Son correctos el presupuesto y la fecha?** El presupuesto **no**: es 74.569,75 €, no 32.338,33 €. La fecha (09/04) sí es coherente con vuestra hipótesis.
7. **¿Se pueden resolver las dos cuestiones con este archivo?** Solo tras corregir los costes. La Cuestión 2 sale «sí, sin horas extra», pero hay que argumentarla.
8. **¿Qué corregir y en qué orden?** G-1 → G-5 → G-6 → G-3 → G-4 → G-7 → G-2 (línea base, la última) → G-8 → G-9.
9. **¿Qué nota estimo hoy?** Entre 0,65 y 1,0 sobre 2,5. Corregido y bien documentado, entre 1,95 y 2,45.
10. **¿Está listo para entregar?** **No.**

---

**Fuentes externas:**

- [Decreto 101/2025, BOJA nº 93 de 19/05/2025 (fiestas laborales de Andalucía 2026)](https://cdn.juntadeandalucia.es/boja/2025/93/BOJA25-093-00002-6889-01_00320489.pdf)
- [Calendario laboral de Huelva 2026 (fuente no oficial; festivos locales)](https://www.diainternacionalde.com/calendario-laboral/huelva/2026)
