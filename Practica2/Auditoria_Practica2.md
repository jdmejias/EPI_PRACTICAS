# Auditoría final de la Práctica 2 — CURASIERRA (grupo 16)

**Fecha de la revisión:** 14/11/2026.

**Material revisado:**
- `CURASIERRA_contratacion_y_horas_extra.mpp`
- `Memoria_Practica2 (1).docx`
- `CURASIERRA – Punto 2 análisis de alternativas y decisión.pdf`
- `Informe de corrección Práctica 1 - Grupo 16 (1).pdf`

**Enunciado oficial de la Práctica 2:** no está en el equipo. Precio, beneficio, penalizaciones, recargos, sueldos X/Y/Z/R, contingencia y precedencias solo se han podido contrastar con lo que citan la memoria y el PDF de apoyo. No se han verificado contra el enunciado.

## Método

- **Fichero de Project:** se abrió en Microsoft Project **2016** (versión 16.0.4266), por COM, sobre una copia idéntica en solo lectura. Abre sin errores.
- **Datos del modelo:** se exportó el XML de la copia y se leyeron tareas, asignaciones, línea base y la serie diaria de trabajo y horas extra por recurso.
- **Cálculos:** las tasas, los costes y los resultados económicos se recalcularon de forma independiente.
- **Capturas:** las imágenes nuevas se sacaron con «Copiar imagen» de Project 2016 sobre ese mismo fichero. No se ha recreado ningún dato.
- **Originales:** no se han modificado. Su SHA-256 es el mismo antes y después:
  - `.mpp`: `1903f4c1…`
  - `.docx`: `6f1e88ff…`
  - `.pdf`: `6b2d894b…`

## 1. Datos verificados en el `.mpp`

| Dato | Memoria | Project | Estado |
|---|---|---|---|
| Inicio / fin | 05/11/2026 / 18/01/2027 | Igual | ✅ |
| Fecha de estado | 20/11/2026 | 20/11/2026 17:00 | ✅ |
| Línea base | 28.883,20 €; 1.112 h; fin 18/01/2027 | Igual, y por recurso: BD 8.113,76; App 7.303,20; Jr 4.578,00; RespArea 4.399,20; Adm 2.389,20; Web 2.099,84 | ✅ conservada |
| Coste actual | 31.717,82 € | 31.717,82 € | ✅ |
| Coste real hasta el 20/11 | 9.471,92 € | 9.471,92 € | ✅ |
| Desviación de 4.150 € | 3.744,08 + 405,92 | 2.3: trabajo 176 h frente a 24 h previstas; costo fijo 405,92 € | ✅ cuadra |
| Horas extra | 80 h: Jr 34, Jr2 30, BD 14, RespArea 2 | Igual | ✅ |
| Máximo de horas extra por persona y día | 2 h | 2,00 h (RespArea 0,67) | ✅ |
| Sobreasignaciones | 0 | 0, comprobado día a día con el trabajo normal ≤ 8 h | ✅ |
| Trabajo en días no laborables | — | 0 h | ✅ |
| Calendario | 7 y 8/12; del 23/12 al 06/01 | Igual. La Navidad coincide con el calendario oficial de Grado UHU 2026/27. | ✅ |
| N1 / N2 / N3 / N4 | CC+5 ed / FC−2 ed / FF / FC+3 ed | Igual | ✅ |
| Restricciones «No comenzar antes del» | 4.2, 5.1, 5.2.3, 5.2.4, 7.2, 13 | Igual | ✅ |
| Tareas terminadas | 8 al 100 % con las fechas de la línea base | Igual. La 2.3 está al 75 % y la 2.4 al 0 %. | ✅ |
| Camino crítico | 2.3 → 2.4 → 4.1 → 7.3 → 8.x → 9.x, más 10.2 y 5.2.4 | Igual | ✅ |
| Fechas replanificadas (tabla 7.3) | 22 filas | Coinciden todas | ✅ |

**Recálculos independientes:**

- **Tasas.** Bruto × 1,33 ÷ 1.772: RespArea 42,30; Web 32,81; BD 29,83; App 26,85; Adm 19,91; Jr 22,83 × 0,7 = 16,35. Las horas extra también cuadran. La columna de empresa mediana da 32.546,72 €, como dice la memoria.
- **Escenarios.**
  - A4: 35.900 − 31.717,82 = 4.182,18 €.
  - A3: 3.619,52 €.
  - A2: 2.329,22 €.
  - A1: 1.738,56 €.
  - A0: −18.283,20 €, con penalización de 10.700 + 11 × 950 = 21.150 €.
  - A5: −14.671,92 €.
- **Anexo C.** 9.471,92 + 1.168,48 + 21.077,42 = 31.717,82 €; el trabajo pendiente se ha comprobado en el fichero.

## 2. Errores y riesgos

| Gravedad | Problema | Estado |
|---|---|---|
| Moderado | Faltaba la Figura 6, con el marcador «INSERTAR CAPTURA» | **Corregido** con una captura real de Project |
| Moderado | La Figura 1 decía «línea base del Punto 1», pero la imagen era el Gantt de seguimiento del Punto 2 (75 %, 0 %), casi igual que la Figura 2 | **Corregido** con una captura real de los campos de línea base del fichero |
| Moderado | A0, A1, A2, A3 y A5 salen de un modelo de optimización externo; solo A4 está en Project. En la Práctica 1 el corrector pedía alternativas calculadas en Project o en una hoja de cálculo. | **No corregido** (decisión del grupo). Si existen los XML que cita el PDF, conviene entregarlos. |
| Moderado | El PDF de apoyo contradice a la memoria: indexa 4 ficheros XML que no están en la carpeta y dice que se probaron «los seis perfiles», mientras la memoria (D-8) habla de tres | **No corregido.** Recomendación: no entregar el PDF o alinearlo con la memoria. |
| Menor | En el apartado 3 aparecía «590,92 €», cuando D-9 y el Anexo C dan 591,02 €, que es lo correcto (31.717,82 − 31.126,80) | **Corregido** |
| Menor | El apartado 7.4 decía que se llega a 2 h extra al día en «7.3 y 4.1»; también se llega en la 8.3 y la 5.2.4 | **Corregido** |
| Menor | El pie de la Figura 6 limitaba el periodo al 30/11–22/12, pero hay horas extra del 26/11 al 18/01 | **Corregido** |
| Menor | Las tablas de figuras tenían resaltado amarillo | **Corregido** |
| Observación | El hito 11 «Entrega del diseño» cae el 18/01, después de construcción y pruebas, porque la 5.2.4 se coloca al final por coste. Está documentado en D-4, pero el profesor podría verlo como incoherente. | Sin cambio |
| Observación | La fecha de A0 (29/01) no se puede reproducir con el fichero entregado. Desplazar 6 días laborables la cadena final daría el 26/01; los días restantes dependen de los desfases y recursos del modelo del grupo. | Sin verificar |

## 3. Cambios en `Memoria_Practica2_final.docx`

- **Figura 1:** captura de Project con duración, comienzo, fin, trabajo y costo previstos de las 43 tareas. Pie ajustado.
- **Figura 6:** 4 capturas de Uso de recursos con detalle diario de Trabajo y Trabajo extra, del 23/11/2026 al 18/01/2027. Pie ajustado.
- **Correcciones de texto:** «590,92 €» → «591,02 €»; en la tabla 7.4, «(7.3 y 4.1)» → «(4.1, 7.3, 8.3 y 5.2.4)».
- **Formato:** quitado el resaltado de las 7 tablas de figuras.
- **Portada:** correos de Santiago y Jhon, los que facilitó el grupo.
- **Lista de comprobación:** marcado ☑ en «Las capturas del Anexo A y las figuras 1 y 2 están insertadas».
- **Índice:** activado `updateFields` para que Word lo actualice al abrir, porque la paginación cambia con las imágenes nuevas.

El `.mpp` no se ha modificado: no hacía falta.

## 4. Pendiente antes de entregar

1. **Reparto del trabajo:** parte de la que se ocupó cada integrante (portada) y tareas y horas (apartado 10). Están resaltados como «completar» y no se han inventado.
2. **Versión final en Word:** abrir `Memoria_Practica2_final.docx` en Word, aceptar actualizar el índice, revisar que las tablas e imágenes no queden cortadas en la paginación y **exportar a PDF**. En este equipo no hay Word, así que no he podido generar el PDF con la maquetación real ni ver la paginación.
3. **Lista de comprobación:** después de lo anterior, marcar en Word los tres puntos que quedan sin marcar (entrega del PDF y del `.mpp`, datos del grupo y ausencia de resaltado amarillo).
4. **PDF de apoyo:** decidir si se entrega. Si se entrega, quitar o explicar el índice de ficheros XML.

## 5. Cierre (14/11/2026) — contraste con el enunciado oficial `Practica2-2027.pdf`

- **Enunciado frente al fichero:**
  - Las 29 tareas suman 1.112 h.
  - Las precedencias, los roles por tarea, N1–N4, el calendario de la ETSI con el 22/12 laborable, el 33 % de Seguridad Social, las 1.772 h, los recargos, el precio de 35.900 €, el beneficio de 3.820 €, las penalizaciones (10.700 € + 950 €/día y 5.200 € por cancelación), el 30 % de contingencia incluido y los 5 días de preparación coinciden con el modelo.
- **Hito «Entrega del diseño» el 18/01:** compatible con el enunciado. El hito se exige «tras finalizar todas las actividades de diseño», y la construcción solo depende de la 4.1 (N1, N2) y de la 6.2. Se mantiene.
- **Alternativas:** el enunciado pide analizarlas y documentarlas, y entregar «el índice de ficheros Project que entrega». No exige un fichero por alternativa. No se generan ficheros nuevos.
- **Reparto del grupo:** completado en la portada y en el apartado 10. Las horas están marcadas como **estimadas**: JF 18 h, Santiago 20 h y Jhon 18 h.
- **Formato:** salto de página antes de la lista de comprobación para que la tabla no se parta. Índice actualizado con la paginación del PDF.
- **PDF:** exportado con LibreOffice, instalado con winget porque el equipo no tiene Word. La Figura 6 se lee bien al ampliar; a tamaño de página el texto es pequeño, con la misma densidad que la Figura 2 original.
- **Entrega:** carpeta `ENTREGA/` con `Memoria_Practica2.pdf` (el nombre que figura en el índice de ficheros) y `CURASIERRA_contratacion_y_horas_extra.mpp`, sin modificar.
