# Correcciones de la Práctica 1 — MEDIATEC «Marismas del Odiel»

**Fecha:** 23/10/2026.
**Referencia:** `Auditoria_Practica1.md` (apartados A–J).

**Método:** todas las correcciones se hicieron **dentro de Microsoft Project** mediante automatización COM, sobre copias del fichero. Después se guardaron, se volvieron a abrir y se verificaron. Ninguna cifra de este documento está calculada fuera de Project sin indicarlo.

**Original:** `Practica1_Base_C1.mpp` no se ha modificado. Su SHA-256 es `7fec3077…f165fe9f`, idéntico antes y después. Hay además una copia de seguridad en `_backup/Practica1_Base_C1_ORIGINAL_20261023_131155.mpp`.

---

## A. Resumen ejecutivo

| Concepto | Valor |
|---|---|
| Estado inicial | PARCIALMENTE CORRECTO. Costes fijos a 1/100, línea base incompleta, vínculos y restricciones sin justificar, sin memoria. |
| Hallazgos de la auditoría (F-1 a F-11) | 11 |
| Corregidos en los `.mpp` o en la documentación | 11 (F-10, a falta de un detalle cosmético) |
| Problemas nuevos detectados al corregir | 3: sobreasignación al modelar el solape (resuelta); unidades del XML (documentado: era la causa raíz); fecha límite del 22/04 ya presente en el hito (se conserva) |
| Criterios de la matriz de 89 | ✅ 87 · ⚠️ 2 · ❌ 0 (ver sección G.2) |
| Coste del proyecto | **32.338,33 € → 74.569,75 €** |
| Fecha de fin del escenario base | **09/04/2026 08:30** (no cambia) |
| Oferta (beneficio del 20 % sobre el coste) | **89.483,70 €** (93.212,19 € si es margen sobre el precio) |
| Cuestión 2 (13 de abril) | **Sí**, sin horas extra y sin coste adicional (escenario A) |
| ¿Listo para entregar? | **Casi.** Faltan los datos del grupo en la memoria (marcados como `[PENDIENTE]`) y montar el ZIP. |

---

## B. Registro completo de modificaciones

### B.1 Escenario A — `Practica1_Base_C1_Corregido.mpp`

Los Id son los de la vista Gantt; entre paréntesis va el UniqueID (UID).

| ID | Tarea o elemento | Problema original | Valor anterior | Valor nuevo | Motivo | Estado |
|---|---|---|---|---|---|---|
| A-01 | Id 2 (UID 101) Montaje de soportes — Costo fijo | Importe a 1/100 | 19,68 € | 1.968,00 € | 240 × 8,20 € (pág. 2) | ✅ |
| A-02 | Id 4 (UID 111) Instalar cables eléctricos — Costo fijo | Ídem | 9,20 € | 920,00 € | pág. 2 | ✅ |
| A-03 | Id 5 (UID 112) Instalar puntos de corriente — Costo fijo | Ídem | 3,40 € | 340,00 € | pág. 2 | ✅ |
| A-04 | Id 7 (UID 121) Instalar canaletas — Costo fijo | Ídem | 2,30 € | 230,00 € | pág. 3 | ✅ |
| A-05 | Id 8 (UID 122) Instalar cables de red — Costo fijo | Ídem | 6,40 € | 640,00 € | pág. 3 | ✅ |
| A-06 | Id 9 (UID 123) Tomas de red — Costo fijo | Ídem | 5,80 € | 580,00 € | pág. 3 | ✅ |
| A-07 | Id 10 (UID 124) Armario, pruebas y certificación — Costo fijo | Ídem | 4,60 € | 460,00 € | pág. 3 | ✅ |
| A-08 | Id 11 (UID 130) Terminales táctiles — Costo fijo | Ídem | 105,60 € | 10.560,00 € | 240 × 44 € (pág. 3) | ✅ |
| A-09 | Id 13 (UID 201) Tornos — Costo fijo | Ídem | 55,50 € | 5.550,00 € | 3 × 1.850 € (pág. 3) | ✅ |
| A-10 | Id 14 (UID 202) Barreras — Costo fijo | Ídem | 8,80 € | 880,00 € | pág. 3 | ✅ |
| A-11 | Id 15 (UID 203) Integración NFC — Costo fijo | Ídem | 55,20 € | 5.520,00 € | 6 × 920 € (pág. 4) | ✅ |
| A-12 | Id 17 (UID 301) Servidor — Costo fijo | Ídem | 56,70 € | 5.670,00 € | 4.500 + 870 + 300 € (pág. 4) | ✅ |
| A-13 | Id 18 (UID 302) Armario, switches y patch panels — Costo fijo | Ídem | 82,40 € | 8.240,00 € | 6×1.040 + 6×210 + 740 € (pág. 4) | ✅ |
| A-14 | Id 50 (UID 702) Reunión 1 — Costo fijo | Ídem | 2,75 € | 275,00 € | Catering (pág. 7) | ✅ |
| A-15 | Id 53 (UID 705) Reunión 2 — Costo fijo | Ídem | 2,75 € | 275,00 € | Ídem | ✅ |
| A-16 | Id 56 (UID 708) Reunión 3 — Costo fijo | Ídem | 2,75 € | 275,00 € | Ídem | ✅ |
| A-17 | Id 59 (UID 711) Reunión 4 — Costo fijo | Ídem | 2,75 € | 275,00 € | Ídem | ✅ |
| A-18 | Vínculo 1 → 2 (Id 21 → 22) — Posposición | Faltaba el solape | FC, 0 | FC −1 día (−480 min) | Nota del apdo. IV | ✅ |
| A-19 | Id 22 (UID 2) Requisitos — Retraso por redistribución | El solape sobreasignaba a los 3 analistas (13,33 h el 20/02) | 0 | 1 día transcurrido (1.440 min) | Mismos recursos en 1 y 2; equivale a nivelar | ✅ |
| A-20 | Id 34 (UID 11) Tarea 11 — Predecesoras | El hito «Cierre del diseño» no tenía sucesoras | 31 (tarea 10) | 32 (hito) | Hito dentro de la cadena crítica | ✅ |
| A-21 | Id 40 (UID 15) Tarea 15 — Predecesoras | El hito «Aprobación» no tenía sucesoras | 37 (tarea 14) | 38 (hito) | Ídem | ✅ |
| A-22 | Id 11 (UID 130) Terminales — Predecesoras | Vínculo con la tarea 10 sin justificar | 5; 10; 31 | 5; 10; 32 | Vínculo de recurso con el hito, documentado en las Notas | ✅ |
| A-23 | Id 18 (UID 302) — Tipo de restricción | «Debe comenzar el» lo marcaba como crítico | MSO 17/02 | Lo antes posible | Arranca igualmente el 17/02 | ✅ |
| A-24…A-35 | Id 49 a 60 (UID 701–712), las 12 tareas de reunión — Tipo de restricción | MSO las marcaba como críticas | «Debe comenzar el» (fecha y hora de cada una) | «No comenzar antes del» (misma fecha y hora) | Conservan la fecha y dejan de falsear la ruta crítica | ✅ |
| A-36 | Calendarios «Laboral Huelva 2026» y «Personal MEDIATEC (con reuniones)» — Excepciones | Solo tenían el 02/04 y el 03/04 | 2 festivos | +12 festivos: 01/01, 06/01, 28/02, 01/05, 03/08, 15/08, 08/09, 12/10, 02/11, 07/12, 08/12, 25/12 | Decreto 101/2025 (BOJA nº 93) y Resolución de 6/10/2025 (BOJA nº 197: Huelva, 3/08 y 8/09) | ✅ |
| A-37 | Notas de las tareas Id 22, 23, 24, 11, 32 y 38 | Vínculos adicionales sin justificar | Sin nota (o solo la del coste) | Justificación del vínculo o del hito | Trazabilidad para el profesor | ✅ |
| A-38 | Línea base (Proyecto completo) | Faltaba en el proyecto y en los resúmenes; costes a 1/100 | Fin previsto del proyecto = NOD; costo previsto = 0 | Comienzo 17/02/2026, fin 09/04/2026 08:30, costo 74.569,75 €, trabajo 1.074 h | Guardada al final, con el plan ya corregido | ✅ |

**Sin cambios, por decisión razonada:** las asignaciones del escenario A (reparto en equipo; ver la sección F), los vínculos 2→3 y 3→4 (se mantienen como vínculos de recurso: en serie el análisis dura 7 días frente a 8,25 en paralelo), las tasas y las tablas A/B (eran correctas) y la fecha límite del hito de entrega (22/04/2026 17:00, ya presente y correcta).

### B.2 Escenario B — `Practica1_EscB_Conservador.mpp` (creado desde A)

| ID | Elemento | Cambio | Motivo |
|---|---|---|---|
| B-01 | Título del proyecto | «Escenario B: reparto conservador (1 persona por rol)» | Identificación |
| B-02 | Asignaciones de las tareas 1–20 | Una persona por cada rol mínimo: 1 Álvaro; 2 Diego; 3 Lucía; 4 Álvaro; 5 Diego; 6 Lucía A 14 h + Álvaro S 14 h; 7 Diego; 8 Álvaro A 30 h + Rubén P 20 h; 9 Lucía A 30 h + Diego P 28 h; 10 Diego A 8 h + Rubén P 8 h + Álvaro S 16 h; 11–13 y 15–16 Rubén; 14 Rubén P 17 h + Álvaro S 17 h; 17–20 Rubén | Sensibilidad frente a la hipótesis D-8 |
| B-03 | Retraso por redistribución de la tarea 2 | 1 día → 0 | Con analistas distintos, el solape FC−1 día se ejecuta realmente |
| B-04 | Vínculos 2→3, 3→4 y hito→terminales | Eliminados | Solo se usa la lógica del enunciado |
| B-05 | Reuniones 5–8 (UID 713–724) | Añadidas el 20/04, 04/05, 18/05 y 01/06 (preparación 2 h, reunión 1 h × 5 personas, análisis 1 h, 275 €) y sus huecos de agenda en el calendario del personal | Quincenales mientras el proyecto está activo |
| B-06 | Línea base | Se conserva la del escenario A | Comparación A frente a B en el Gantt de seguimiento |

### B.3 Escenario C — `Practica1_EscC_Conservador_HorasExtra.mpp` (creado desde B)

| ID | Elemento | Cambio | Motivo |
|---|---|---|---|
| C-01 | Título | «Escenario C: reparto conservador + horas extra (máx. 2,5 h/día)» | Identificación |
| C-02 | Trabajo de horas extra de las 26 asignaciones de las tareas 1–20 | trabajo × 2,5 / 10,5 (redondeado hacia abajo, en minutos) | Así Project reparte 8 h normales + 2,5 h extra por día |
| C-03 | Terminales (Id 11) | Añadida la predecesora «Cierre del diseño» | Sin ella, Álvaro y Lucía quedaban sobreasignados (12,5 h el 20/03) |
| C-04 | Reuniones 7 y 8 (18/05 y 01/06) | Eliminadas, junto con sus excepciones de calendario | Caen después de la nueva entrega (07/05) |
| C-05 | Línea base | Se conserva la del escenario A | Comparación |

---

## C. Correcciones económicas

### C.1 Costes fijos originales y corregidos

| Partida | Antes (en Project) | Ahora | Cálculo |
|---|---|---|---|
| Soportes | 19,68 € | 1.968,00 € | 240 × 8,20 |
| Instalación eléctrica | 12,60 € | 1.260,00 € | 920 + 340 |
| Instalación de red | 19,10 € | 1.910,00 € | 230 + 640 + 580 + 460 |
| Terminales | 105,60 € | 10.560,00 € | 240 × 44 |
| Tornos + barreras | 64,30 € | 6.430,00 € | 3 × 1.850 + 880 |
| NFC tornos | 55,20 € | 5.520,00 € | 6 × 920 |
| Servidor + licencia + transporte | 56,70 € | 5.670,00 € | 4.500 + 870 + 300 |
| Switches + patch panels + armario | 82,40 € | 8.240,00 € | 6.240 + 1.260 + 740 |
| Catering (4 reuniones) | 11,00 € | 1.100,00 € | 4 × 275 |
| **Total de costes fijos** | **426,58 €** | **42.658,00 €** | |

- **Sin doble contabilización.** Cada partida aparece en una sola tarea. El montaje del armario solo está en Id 10, y no hay instalación eléctrica ni de red en los tornos.
- **Ninguna otra tarea** tiene costo fijo. Se revisaron las 60 tareas, incluidas las resumen, que tienen 0.
- **Causa raíz.** En el formato XML de Project (MSPDI), el campo `FixedCost` se guarda **en céntimos**. El original contenía `1968` (= 19,68 €); el corregido contiene `196800` (= 1.968 €). Los importes se escribieron en euros en un campo que va en céntimos.

### C.2 Costes laborales verificados

| Recurso | Horas | Coste | Comprobación |
|---|---|---|---|
| Álvaro Nieto | 226,5 h | 6.629,39 € | |
| Marta Salas | 16 h | 471,20 € | Solo reuniones (tabla A) |
| Lucía Prieto | 226,5 h | 6.668,26 € | Tabla B en las tareas 10 y 14 |
| Diego Manzano | 264,5 h | 8.448,34 € | Tasas con fecha 01/03 y 20/03 |
| Rubén Ferrer | 172,5 h | 3.982,57 € | Tabla A siempre |
| Operarios (subcontrata) | 168 h | 5.712,00 € | 168 × 34 € |
| **Total** | **1.074 h** | **31.911,75 €** | Recálculo independiente: 31.912,03 € (+0,28 € por el redondeo de tasas) |

Las tasas y sus cambios con fecha se verificaron una a una: 29,16 / 29,74; 32,65 / 33,31 para Diego; tablas B 34,99 · 31,49 · 34,25; horas extra 33,24 · 35,57 · 34,40 · 26,71 · 44,20. Coinciden con 39.741 × 1,3 / 1.772 y 31.122 × 1,3 / 1.772.

### C.3 Totales

| Concepto | Importe |
|---|---|
| Coste total anterior (Project) | 32.338,33 € |
| **Coste total corregido (Project)** | **74.569,75 €** |
| Diferencia | +42.231,42 € (= 42.658 − 426,58) |

**Por bloques:**

| Bloque | Coste |
|---|---|
| I | 21.536,88 € |
| II | 13.764,64 € |
| III | 14.275,28 € |
| IV (tareas 1–16) | 20.179,56 € |
| V (tareas 17–20) | 2.785,92 € |
| Reuniones | 2.027,47 € |

### C.4 Oferta definitiva

| Interpretación | Oferta | Beneficio |
|---|---|---|
| **20 % sobre el coste (adoptada, D-7)** | **89.483,70 €** | 14.913,95 € |
| 20 % de margen sobre el precio | 93.212,19 € | 18.642,44 € |

---

## D. Correcciones temporales

| Aspecto | Antes | Después |
|---|---|---|
| Solape 2 ← 1 | FC sin adelanto | FC −1 día + retraso por redistribución de 1 día (sin sobreasignación) |
| Hitos | Sin sucesoras (márgenes de 14,56 y 7,25 días; no críticos) | Predecesores de 11, 15 y terminales; margen 0, críticos |
| Restricciones | 13 «Debe comenzar el» | 0 MSO: 12 «No comenzar antes del» y 1 «Lo antes posible» |
| Calendario | 2 excepciones | 14 excepciones oficiales (en los dos calendarios base) |
| Asignaciones (escenario A) | — | Sin cambios (decisión documentada) |
| Ruta crítica | Ruido: 12 reuniones e Id 18 marcados como críticos | Solo 1→…→20 y la Entrega (más sus resúmenes) |
| Duración | 35,06 días laborables | 35,06 días laborables |
| **Fecha de fin** | **09/04/2026 08:30** | **09/04/2026 08:30** |

**Por qué la fecha no cambia.** Durante la corrección, el solape −1 día adelantó la fecha al 08/04, pero solo porque sobreasignaba a los tres analistas (13,33 h el 20/02). Ese adelanto era **ficticio** y no se aceptó: el retraso por redistribución devuelve la fecha real del 09/04. Ninguna de las demás correcciones afecta a la lógica de la ruta crítica.

---

## E. Comparación de escenarios (valores leídos de Project)

| Escenario | Fichero | Entrega | Días lab. | Coste Project | Horas extra | Personas en desarrollo | Penalización | Ruta crítica |
|---|---|---|---|---|---|---|---|---|
| **A** (recomendado) | Practica1_Base_C1_Corregido.mpp | **09/04/2026 08:30** | 35,06 | **74.569,75 €** | 0 | 4 (+ Marta solo en reuniones) | 0 € | 1→2→3→4→5→6→7→8/9→10→Hito→11→…→14→Hito→15→16→17→18→19→20→Entrega |
| B | Practica1_EscB_Conservador.mpp | 01/06/2026 10:00 | 71,5 | 75.510,86 € | 0 | 4, uno por rol | 22.400 € (40 días naturales) / 15.120 € (27 laborables) | 1→3→5→6→7→8/9→10→Hito→11→…→20→Entrega (2 y 4 con margen) |
| C | Practica1_EscC_Conservador_HorasExtra.mpp | 07/05/2026 11:06 | 54,39 | 75.226,21 € (horas extra valoradas en 5.984,26 €; recargo neto 806,83 €) | 187,88 h, máx. 2,50 h/día | 4, uno por rol | 8.400 € (15 días naturales) / 5.600 € (10 laborables) | Igual que B |

**Recomendación: entregar A como plan ofertado y respuesta a las dos cuestiones.** Cumple todas las restricciones verificadas, termina antes del 13/04 sin horas extra y es el más barato. B y C acompañan como **análisis de sensibilidad**: demuestran que la conclusión depende de la hipótesis de reparto y cuantifican el riesgo.

**Sergio Ballesteros** no se modeló en un `.mpp` porque no aporta nada en ninguna hipótesis. En A el plazo ya se cumple. En B y C, la cadena crítica (tareas 11–20) la forman tareas secuenciales de una sola persona, y un programador más no la acorta sin dividir las tareas, que es justo la hipótesis de A. Esta conclusión es razonada, no calculada en Project, y así figura en la memoria (A2: «No calculado en Project»).

---

## F. Explicación del 13 de abril

**¿Por qué terminábamos el 9 de abril sin horas extra?**
Porque cada tarea de desarrollo la hacen **a la vez** todas las personas con el rol exigido. Por ejemplo, la tarea 1 (88 h) la hacen tres analistas: 29,33 h cada uno, 3,67 días. Las tareas en Project son de «Trabajo fijo» condicionado por el esfuerzo, así que la duración se divide entre el número de personas.

**¿Era correcto?**
Sí, **con esa hipótesis**, y se ha vuelto a verificar después de las correcciones:
- Las horas de las 20 tareas coinciden con el enunciado.
- Los roles son válidos.
- Ningún día supera las 8 h normales por persona.
- No hay trabajo en festivos ni fines de semana.
- Se respetan todas las dependencias del enunciado.

No había ningún error oculto que adelantara la fecha. El único «adelanto» que apareció (al 08/04 con el solape) era artificial y se descartó.

**¿Se mantiene esa fecha después de corregir?**
Sí: **09/04/2026 08:30**. Lo que cambia es el coste.

**¿Qué pasa con una asignación más conservadora?**
Con una persona por rol (B), la entrega pasa al **01/06/2026**, con 40 días naturales de retraso. Incluso con el máximo legal de horas extra (C), la entrega queda en el **07/05/2026**. Con esa hipótesis no se llega al 13/04 ni al 22/04.

**¿Qué interpretación es más defendible?**
**La A.** Hay cuatro argumentos:
1. El enunciado da «trabajo total» y «roles **mínimos** que deben intervenir», y no limita las personas por tarea.
2. Con la hipótesis B, el proyecto incumpliría el contrato en más de un mes incluso con todas las horas extra posibles. Un enunciado que fija el 22/04 como plazo difícilmente pretende un escenario base imposible de cumplir.
3. Las notas «A(14h), S(14h)» de las tareas 6, 8, 9, 10 y 14 indican cómo se reparte el trabajo entre roles, no que cada rol lo haga una persona.
4. El enunciado subraya que el equipo tiene «amplia experiencia», lo que «permite ajustar con holgura las estimaciones».

Aun así, es una **hipótesis**, no un hecho demostrable desde el enunciado. La plantilla da por hecho que el escenario base «No llega al 13 de abril», así que **conviene confirmarlo con el profesor**. Mientras tanto, la memoria la declara, la justifica (D-8) y la contrasta con B y C.

---

## G. Validaciones realizadas

### G.1 Comprobaciones

| # | Qué se verificó | Cómo | Resultado | Evidencia |
|---|---|---|---|---|
| 1 | Guardado y persistencia | Cada `.mpp` se cerró y se reabrió en una instancia nueva de Project (solo lectura) | Abren sin errores; los cambios persisten | Lecturas por COM tras reabrir |
| 2 | Original intacto | SHA-256 antes y después | Idéntico | `7fec3077…f165fe9f` |
| 3 | EDT | Listado de las tareas, sus niveles y resúmenes | 60 tareas en A, 72 en B y 66 en C; jerarquía coherente | Gantt (Capturas/*_gantt_completo.png) |
| 4 | Trabajo de las 20 tareas | Script frente a la tabla del enunciado (XML exportado de cada `.mpp`) | 0 diferencias en A, B y C | 694 h + 96 h |
| 5 | Roles | Cada asignación frente a los roles del enunciado | 0 incumplimientos; Marta sin tareas de desarrollo | Tabla B solo para Lucía S (A) |
| 6 | Dependencias | Predecesoras frente al enunciado | Todas presentes; adicionales solo 2→3 y 3→4 (A, justificadas) | Notas de las tareas |
| 7 | Costes fijos | Valor del campo frente al importe del enunciado | 13 tareas + 4 caterings correctos | Tabla Costo |
| 8 | Coste de personal | Recálculo independiente (horas diarias × tasa) | 31.912,03 € frente a 31.911,75 € | Anexo C de la memoria |
| 9 | Tasas | Tablas A/B y cambios con fecha | Correctas | Hoja de recursos |
| 10 | Sobreasignaciones | Campo «Sobreasignado» + trabajo normal diario (trabajo − horas extra) | Ninguna en A, B y C; máx. 8 h/día (operarios 16 h/día) | Calculos_Practica1.xlsx |
| 11 | Horas extra ≤ 2,5 h por persona y día | Serie diaria de horas extra por recurso | A y B: 0. C: máximo 2,50 (Álvaro 2,4996; Lucía 2,497; Diego 2,50; Rubén 2,50) | Capturas/C_uso_recursos_horas_extra_1…6.png |
| 12 | Días laborables | Trabajo diario frente a fines de semana y festivos | 0 horas en sábados, domingos, 02/04, 03/04 o 01/05 | xlsx |
| 13 | Línea base | Campos previstos de proyecto, resúmenes y tareas | Proyecto: 17/02 → 09/04 08:30, 74.569,75 €, 1.074 h | Gantt de seguimiento |
| 14 | Calendario | Excepciones exportadas en XML: no laborables | 14 festivos en ambos calendarios base; los recursos heredan de «Laboral Huelva 2026» | Anexo B de la memoria |
| 15 | Fecha de fin y fecha límite | Fin del proyecto y hito con fecha límite | A 09/04 (margen positivo); B y C con margen negativo | Gantt (flecha verde del 22/04) |
| 16 | Oferta | 74.569,75 × 1,2 y ÷ 0,8 | 89.483,70 € / 93.212,19 € | — |
| 17 | Memoria frente a los `.mpp` | Las cifras de la memoria se tomaron de las lecturas de Project | Coinciden | Memoria_Practica1.pdf |

**Incidencias de verificación detectadas y corregidas durante el proceso:**
- Un código de serie temporal mal identificado devolvía el **trabajo previsto** en lugar del normal, y hacía que B pareciera igual que A. Se detectó, se corrigió (trabajo normal = trabajo − horas extra) y se repitieron todas las comprobaciones.
- Al construir B, las tareas con varios roles perdían horas por el esfuerzo condicionado (por ejemplo, la tarea 6 quedaba con 21 h en lugar de 28). Se rehízo B desde A, añadiendo primero todas las asignaciones y fijando después las horas.
- Las reuniones nuevas repartían 1 h entre 5 personas. Se desactivó el esfuerzo condicionado en esas tareas, que son de duración fija.

### G.2 Matriz de cumplimiento actualizada (89 criterios de la auditoría)

| Grupo | Antes ✅ / ⚠️ / ❌ | Ahora ✅ / ⚠️ / ❌ | Cambios |
|---|---|---|---|
| Bloque I (18) | 12 / 2 / 4 | **18 / 0 / 0** | I.2, I.9, I.11 e I.13: costes; I.16: D-3 documentada; I.18: vínculo al hito, justificado |
| Bloque II (9) | 6 / 0 / 3 | **9 / 0 / 0** | II.1–II.3: costes |
| Bloque III (5) | 3 / 0 / 2 | **5 / 0 / 0** | III.1 y III.2: costes; III.5: restricción eliminada |
| Bloque IV (27) | 23 / 4 / 0 | **27 / 0 / 0** | IV.19 solape modelado; IV.20/21 vínculos justificados; IV.24 hitos en la cadena |
| Bloque V (5) | 5 / 0 / 0 | **5 / 0 / 0** | — |
| Bloque VI (9) | 7 / 1 / 1 | **9 / 0 / 0** | VI.2 calendario completo; VI.4 catering |
| Recursos (9) | 9 / 0 / 0 | **9 / 0 / 0** | Hipótesis salariales declaradas en la memoria |
| Técnicos y entregables (7) | 1 / 3 / 3 | **5 / 2 / 0** | T.1 línea base ✅; T.2 ruta crítica ✅; T.5 escenarios ✅; T.7 capturas ✅. **T.4** ⚠️: el calendario «Estándar» sigue existiendo (sin uso). **T.6** ⚠️: memoria hecha, con los datos del grupo `[PENDIENTE]`. |
| **Total** | **66 / 10 / 13** | **87 / 2 / 0** | Cumplimiento estricto del **97,8 %**; no es el 100 % |

---

## H. Problemas pendientes (reales)

| Problema | Por qué no se resolvió | Procedimiento exacto |
|---|---|---|
| ~~Correos UHU y reparto del trabajo~~ | **Resuelto:** la portada tiene los tres nombres y correos, y el apartado 10 tiene el reparto en parte inicial (Jhon), central (Santiago) y final (Juanfrancisco). | — |
| Índice de la memoria con números de página | python-docx no calcula la paginación; no hay Word instalado en este equipo | Abrir el .docx en Word. El documento pide actualizar los campos al abrir (`updateFields`); aceptar, o pulsar F9 sobre el índice. Después, Archivo → Exportar → PDF para un PDF con la maquetación exacta de Word |
| PDF generado sin Word | Se generó con mammoth (docx → HTML) y Microsoft Edge (HTML → PDF): el contenido es el mismo, pero la maquetación es aproximada | Opcional: volver a exportar desde Word, como en la fila anterior |
| ZIP de entrega | Depende de los dos puntos anteriores | Comprimir: Memoria_Practica1.pdf, Practica1_Base_C1_Corregido.mpp, Practica1_EscB_Conservador.mpp, Practica1_EscC_Conservador_HorasExtra.mpp y, opcionalmente, Calculos_Practica1.xlsx. **No incluir** el `Practica1_Base_C1.mpp` original. |
| Calendario «Estándar» sin uso (cosmético) | Borrarlo exige el Organizador; no afecta a ninguna fecha | Archivo → Información → Organizador → pestaña Calendarios → seleccionar «Estándar» en el proyecto → Eliminar |
| Formato de duración de las reuniones nuevas en B/C (se ven como «0,25 días» en lugar de «2 horas») | Cosmético; trabajo, horas y fechas son correctos | En cada tarea, escribir la duración como «2 h» o «1 h» |
| ~~Aceptación de la hipótesis D-8 por el profesor~~ | **Resuelto:** el grupo la ha confirmado con el profesor | — |

---

## I. Archivos finales (carpeta `Practica1/`)

| Archivo | Función |
|---|---|
| `Practica1_Base_C1.mpp` | **Original, sin modificar.** No va en el ZIP. |
| `_backup/Practica1_Base_C1_ORIGINAL_20261023_131155.mpp` | Copia de seguridad del original |
| `Practica1_Base_C1_Corregido.mpp` | **Escenario A**: plan corregido con línea base completa. Cuestiones 1 y 2. |
| `Practica1_EscB_Conservador.mpp` | Escenario B: una persona por rol (sensibilidad), con la línea base de A |
| `Practica1_EscC_Conservador_HorasExtra.mpp` | Escenario C: B + horas extra ≤ 2,5 h/día, con la línea base de A |
| `Memoria_Practica1.docx` | Memoria editable sobre la plantilla oficial (10 apartados, 8 fichas de decisión, anexos A–C y 13 figuras) |
| `Memoria_Practica1.pdf` | Memoria en PDF (23 páginas) |
| `Calculos_Practica1.xlsx` | Coste hora con fórmulas, partidas fijas, comparativa de escenarios y horas diarias (normales y extra) por persona de A, B y C |
| `Capturas/` (18 PNG) | Gantt, Gantt de seguimiento, hoja de recursos y tabla de costos de A, B y C; Uso de recursos con horas extra diarias de C (6 tramos) |
| `Auditoria_Practica1.md` | Auditoría previa |
| `Correcciones_Practica1.md` | Este documento |

---

## J. Explicación de los cambios para el estudiante

### 1. Costes fijos a 1/100 (el error grave)

- **Qué estaba mal.** El campo *Costo fijo* de 17 tareas valía 100 veces menos de lo debido. Por ejemplo, 19,68 € en lugar de 1.968 € en los soportes.
- **Por qué.** Los importes se escribieron en euros en un campo que, en el formato XML de Project, va en céntimos. Project no avisa de nada: el número es «válido».
- **Cómo lo corregí.** Escribí el importe real del enunciado en cada tarea.
- **Qué cambia.** El coste total pasa de 32.338 € a 74.570 €. Con el dato antiguo habríais ofertado 38.806 € y el proyecto habría perdido unos 35.800 €.
- **Qué aprender.** Compara siempre el total de Project con una suma independiente de las partidas, aunque sea aproximada.

### 2. Solape de requisitos

- **Qué estaba mal.** El enunciado permite empezar Requisitos un día antes, y no estaba modelado.
- **Cómo lo corregí.** Puse el vínculo FC−1 día. Al hacerlo, Project adelantó la entrega un día, pero a costa de que los tres analistas trabajaran 13,33 h el 20/02. Eso es imposible, así que añadí un retraso por redistribución.
- **Qué aprender.** Un solape solo sirve si hay **personas libres** para aprovecharlo. Una fecha que mejora porque alguien trabaja 13 h no es una mejora: es una sobreasignación.

### 3. Hitos sin sucesoras

- **Qué estaba mal.** Los hitos estaban «colgando»: nada dependía de ellos, así que Project los mostraba con margen y fuera de la ruta crítica.
- **Cómo lo corregí.** Ahora la tarea 11 y la 15 dependen de los hitos.
- **Qué aprender.** Un hito debe formar parte de la cadena lógica para que tenga sentido en la ruta crítica.

### 4. «Debe comenzar el» en las reuniones

- **Qué estaba mal.** Esa restricción da margen 0 y Project pinta la tarea como crítica aunque no retrase nada.
- **Cómo lo corregí.** La cambié por «No comenzar antes del»: la reunión sigue el mismo lunes y la ruta crítica queda limpia.
- **Qué aprender.** Usa las restricciones más débiles que resuelvan el problema.

### 5. Calendario

- **Qué estaba mal.** Solo tenía la Semana Santa. Ahora tiene todos los festivos oficiales de 2026 en Huelva.
- **Qué cambia.** Dentro del plan base, nada. En los escenarios largos, el 1 de mayo sí cuenta.

### 6. Línea base

- **Qué estaba mal.** Estaba incompleta y con costes a 1/100.
- **Cómo lo corregí.** Se guardó al final, cuando el plan ya era correcto.
- **Qué aprender.** La línea base es la «foto» del plan aprobado. Si se guarda antes de corregir, compara contra un plan erróneo.

### 7. El 13 de abril

Vuestro resultado era correcto con vuestra hipótesis: trabajar en equipo dentro de cada tarea. Lo que faltaba era **declararla y demostrar su impacto**. Ahora podéis decirle al profesor:

> «Con el reparto en equipo terminamos el 09/04 sin horas extra. Si cada rol lo cubriera una sola persona, acabaríamos el 01/06, y ni con 2,5 h extra diarias llegaríamos al 22/04 (07/05). Por eso consideramos que el enunciado, que habla de roles mínimos y fija el 22/04 como plazo, admite el trabajo en equipo.»

**Fuentes oficiales del calendario:**
- [Decreto 101/2025, BOJA nº 93 (19/05/2025)](https://cdn.juntadeandalucia.es/boja/2025/93/BOJA25-093-00002-6889-01_00320489.pdf)
- [Resolución de 6/10/2025, fiestas locales de 2026, BOJA nº 197 (14/10/2025)](https://www.sspa.juntadeandalucia.es/servicioandaluzdesalud/sites/default/files/sincfiles/wsas-media-sas_normativa_mediafile/2025/BOJA251014_fiestas_locales_2026.pdf)
