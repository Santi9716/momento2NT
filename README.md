# Proyecto de Análisis de Datos Educativos

Este proyecto es una práctica de **análisis de datos en Python** basada en un sistema académico simulado.  
El objetivo es aprender a **cargar, limpiar, transformar y analizar datos** a partir de archivos CSV que contienen información de **usuarios (estudiantes y profesores)** y **notas**.

## 📂 Estructura del Proyecto
proyecto-analisis/
│
├── data/
│ ├── usuarios.csv # 100 registros (80 estudiantes y 20 profesores)
│ ├── notas.csv # +300 registros de calificaciones
│
├── preprocesamiento.py # Funciones de limpieza y preparación de datos
├── analisis.py # Script principal de análisis
├── README.md # Documentación del proyecto

## ⚙️ Requisitos

- Python 3.8 o superior  
- Librerías necesarias:
  - pandas

//Ejecución

Clonar este repositorio o descargarlo.

Asegurarse de que los archivos usuarios.csv y notas.csv estén en la carpeta data/.

Ejecutar el script de análisis:
python analisis.py

Preguntas de Análisis

El archivo analisis.py responde y permite responder preguntas como:

1.Frecuencia → ¿Cuál es la materia con más registros positivos de calificaciones?

2.Agregación → ¿Cuál es la nota promedio por cada materia?

3.Filtrado y Conteo → ¿Cuántos estudiantes aprobaron?

4.Top Rendimiento → ¿Cuál es el estudiante con la nota más alta en todas las materias?

5.Asistencia de datos faltantes → ¿Cuántas notas están vacías (nulas o inválidas)?

//Notas

Los datos contienen errores intencionales: valores nulos, textos con mayúsculas/minúsculas mezcladas, errores de tipeo en materias y notas con formatos inconsistentes (ej: "3,5" o "4.0 ").

El módulo preprocesamiento.py se encarga de limpiar y estandarizar la información antes del análisis.







