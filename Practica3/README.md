# Práctica 3 - Proyecto ICT (Infraestructura Común de Telecomunicaciones)

Este directorio contiene todo el material, esquemas, planos 2D/3D y documentación de la **Práctica 3 (Sesión 1: Esquemas y Proyecto ICT)**.

---

## 📁 Estructura de Contenidos

### 1. Documentación y Guías Base
* **`Sesión 1. Proyecto ICT.docx`**: Documento de trabajo / guía de la Sesión 1.
* **`GuiaReferenciaMemoriaICT.doc`**: Guía oficial y estructura de referencia para la redacción de la memoria del proyecto ICT.
* **`Ejemplos Planos 2D plantas-20261113.zip`**: Planos 2D de las plantas del edificio en formato CAD/imagen.

---

### 2. Carpeta `Sesion1_Esquemas/`

Contiene todos los diagramas, planos y esquemas técnicos generados para el proyecto ICT en múltiples formatos:

* **Documento Consolidado:**
  * `ICT_Sesion1_Esquemas_3D_2D.pdf`: Documento completo con portada, índice y todos los esquemas técnicos explicados listos para entrega o consulta.

* **Formatos Editables e Intercambio:**
  * **`Visio/`**: Archivos `.vsdx` editables directamente con Microsoft Visio para cada plano/esquema.
  * **`DXF/`**: Archivos de intercambio CAD (`.dxf`) compatibles con AutoCAD y LibreCAD.
  * **`3D/`**: Modelo 3D de la infraestructura (`.obj` + `.mtl`) del conjunto del edificio.
  * **`previsualizacion_png/`**: Renderizados e imágenes en alta resolución (`.png`) para consultar rápidamente o pegar en memorias.
  * **Archivos `.svg`**: Gráficos vectoriales escalables de cada esquema:
    * `ICT_01_Conjunto_3D.svg`: Esquema general de distribución vertical y registros en 3D.
    * `ICT_02_Plano_General_2D.svg`: Esquema unifilar general 2D de la red de ICT.
    * `ICT_03_Vivienda_Planta_Baja.svg`: Esquema de red interior de usuario para vivienda en planta baja.
    * `ICT_04_Vivienda_Planta_Primera.svg`: Esquema de red interior de usuario para vivienda en planta primera.
    * `ICT_05_Local_y_Zonas_Comunes.svg`: Esquema de servicios en local comercial y zonas comunes.

* **Herramientas y Scripts (`fuentes/`):**
  * `generar_planos.py`: Script generador de los diagramas y esquemas.
  * `exportar_pdf.py`: Script para compilación y exportación automática a PDF.
  * `portada.html`: Plantilla de diseño para la portada del informe técnico.
