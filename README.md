# Optimizador de CV con IA (ATS Matcher)

Una aplicación web interactiva impulsada por Inteligencia Artificial Generativa que evalúa currículums contra descripciones de vacantes (Job Descriptions). El sistema simula el comportamiento de un Applicant Tracking System (ATS) estricto, calculando el porcentaje de compatibilidad, identificando palabras clave faltantes y sugiriendo mejoras en la redacción de la experiencia utilizando la metodología STAR.

Video Presentacion: https://drive.google.com/file/d/1_dFBhCUnl1CpKi2ohoH621yCWCBQQFtw/view?usp=sharing

---

## Arquitectura de la Solución

El proyecto está diseñado siguiendo una arquitectura cliente-servidor simplificada, utilizando las siguientes tecnologías:

*   **Frontend (Interfaz de Usuario):** Construido con **Streamlit**, lo que permite una interfaz web responsiva e interactiva desarrollada enteramente en Python.
*   **Procesamiento de Documentos:** Se utiliza **PyPDF2** para la extracción de texto plano desde los archivos PDF subidos por el usuario.
*   **Motor de IA Generativa:** Integración con la API de **OpenAI** (modelo `gpt-4o-mini`). Se emplea una temperatura baja (`0.3`) para garantizar respuestas analíticas, estructuradas y precisas, mitigando alucinaciones.
*   **Generación de Entregables:** Se utiliza **FPDF** para compilar el análisis final de la IA y generar un nuevo reporte en formato PDF que el usuario puede descargar en tiempo real.
*   **Seguridad:** Manejo de credenciales mediante variables de entorno (`python-dotenv`) para asegurar que la API Key nunca se exponga en el código fuente.

---

## 🛠️ Requisitos Previos

Asegúrate de tener instalado en tu sistema:
*   Python 3.8 o superior.
*   Una cuenta de OpenAI con una API Key válida.

---

## ⚙️ Instalación y Configuración

Sigue estos pasos para ejecutar la aplicación en tu entorno local:

**1. Clonar el repositorio**
```bash
git clone [URL_DE_TU_REPOSITORIO]
cd [NOMBRE_DE_LA_CARPETA]
```
**2. Comando**

(`streamlit run main.py`) para correr el programa


**Ejemplo de .env**

```bash
OPENAI_API_KEY="pega_aqui_tu_clave"
OPENAI_MODEL="gpt-4o-mini"
OPENAI_TEMPERATURE="0.3"
```

**Librerias utilizadas**
```bash
import streamlit as st
from openai import OpenAI
import os
import PyPDF2
from dotenv import load_dotenv
from fpdf import FPDF
```


