import streamlit as st
from openai import OpenAI
import os
import PyPDF2
from dotenv import load_dotenv

# Configuracion de la interfaz web
st.set_page_config(page_title="Optimizador de CV IA", page_icon="📄", layout="centered")

# Cargar variables de entorno (Seguridad y Configuración)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Extraer configuracion del modelo con valores por defecto 
modelo_elegido = os.getenv("OPENAI_MODEL", "gpt-4o-mini") 
temperatura_elegida = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

# Validacion de seguridad
if not api_key:
    st.error("Error: No se encontró la API Key. Asegúrate de tener el archivo .env configurado con OPENAI_API_KEY.")
    st.stop()

# Inicializacion segura del cliente de OpenAI
client = OpenAI(api_key=api_key)

# Funcion para procesar el archivo PDF
def extraer_texto_pdf(archivo_pdf):
    lector = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    for pagina in lector.pages:
        texto += pagina.extract_text() + "\n"
    return texto

# Diseño de la Interfaz de Usuario
st.title("🚀 Optimizador de CV con IA")
st.write(f"*(Usando el modelo: `{modelo_elegido}`)*") 
st.write("Sube tu currículum en PDF y pega la descripción de la vacante para analizar tu nivel de compatibilidad.")

# Entradas del usuario
cv_file = st.file_uploader("1. Sube tu CV (Formato PDF)", type=["pdf"])
vacante_desc = st.text_area("2. Pega la descripción de la vacante (Job Description)", height=200)

# Boton de ejecución
if st.button("Analizar y Optimizar CV"):
    if cv_file is not None and vacante_desc.strip() != "":
        with st.spinner(f"Analizando con {modelo_elegido}... esto puede tomar unos segundos."):
            try:
                # Paso 1: Extraer texto del PDF
                texto_cv = extraer_texto_pdf(cv_file)
                
                # Paso 2: Construir el Prompt
                prompt_sistema = "Eres un reclutador experto en tecnología y un sistema ATS (Applicant Tracking System) muy estricto. Responde siempre de forma clara, profesional y estructurada."
                
                prompt_usuario = f"""
                Analiza la siguiente información y genera un reporte estructurado:
                
                TEXTO DEL CURRÍCULUM:
                {texto_cv}
                
                DESCRIPCIÓN DE LA VACANTE:
                {vacante_desc}
                
                El reporte debe contener:
                1. Porcentaje de Compatibilidad.
                2. Palabras Clave Faltantes.
                3. Optimización de Experiencia (Formato STAR): Reescribe 2 viñetas del CV.
                4. Veredicto Final corto.
                """
                
                # Paso 3: Llamar a la API de OpenAI usando las variables dinámicas
                respuesta = client.chat.completions.create(
                    model=modelo_elegido,
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=temperatura_elegida
                )
                
                # Extraer el texto de la respuesta
                resultado_final = respuesta.choices[0].message.content
                
                # Mostrar en pantalla
                st.success("¡Análisis completado con éxito!")
                st.markdown("### Resultados del Análisis ATS")
                st.markdown(resultado_final)
                
            except Exception as e:
                st.error(f"Ocurrió un error al comunicarse con la API: {e}")
    else:
        st.warning("Por favor, sube tu CV en PDF y asegúrate de pegar la descripción de la vacante antes de continuar.")

# correr usando streamlit run main.py