import streamlit as st
from openai import OpenAI
import os
import PyPDF2
from dotenv import load_dotenv
from fpdf import FPDF

# Configuración de la interfaz web
st.set_page_config(page_title="Optimizador de CV", page_icon="📄", layout="centered")

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
modelo_elegido = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
temperatura_elegida = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

if not api_key:
    st.error("Error: No se encontró la API Key en el archivo .env.")
    st.stop()

client = OpenAI(api_key=api_key)

def extraer_texto_pdf(archivo_pdf):
    lector = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    for pagina in lector.pages:
        if pagina.extract_text():
            texto += pagina.extract_text() + "\n"
    return texto

def generar_pdf_en_memoria(texto_cv):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=11)
    
    # Limpiamos caracteres que FPDF no soporta
    texto_limpio = texto_cv.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Currículum Optimizado", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 6, txt=texto_limpio)
    
    return pdf.output(dest='S').encode('latin-1')

st.title("Optimizador de CV")
st.write(f"*(Modelo: `{modelo_elegido}`)*")
st.write("Sube tu CV en PDF y pega la vacante. Obtendrás un reporte y la versión mejorada de tu CV.")

cv_file = st.file_uploader("1. Sube tu CV (Formato PDF)", type=["pdf"])
vacante_desc = st.text_area("2. Pega la descripción de la vacante", height=200)

if st.button("Analizar y Reescribir CV"):
    if cv_file is not None and vacante_desc.strip() != "":
        with st.spinner(f"Reescribiendo CV con {modelo_elegido}..."):
            try:
                texto_cv = extraer_texto_pdf(cv_file)
                
                prompt_sistema = "Eres un reclutador experto y un sistema ATS. No uses emojis. Responde exactamente con la estructura solicitada."
                
                # Modificamos el prompt para forzar la separación de contenido
                prompt_usuario = f"""
                TEXTO DEL CURRÍCULUM ORIGINAL:
                {texto_cv}
                
                DESCRIPCIÓN DE LA VACANTE:
                {vacante_desc}
                
                Tu respuesta DEBE estar dividida en dos partes separadas exactamente por esta palabra: ===SEPARADOR===
                
                PARTE 1: Reporte ATS
                Genera un reporte breve con:
                1. Porcentaje de Compatibilidad.
                2. Palabras Clave Faltantes.
                3. Veredicto Final corto.
                
                ===SEPARADOR===
                
                PARTE 2: Currículum Optimizado
                Reescribe TODO el currículum original de principio a fin.
                - Mantén la información de contacto y educación.
                - Integra las palabras clave faltantes de forma natural.
                - Reescribe TODA la experiencia laboral utilizando la metodología STAR (Situación, Tarea, Acción, Resultado) para que suene mucho más profesional y de impacto.
                """
                
                respuesta = client.chat.completions.create(
                    model=modelo_elegido,
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    temperature=temperatura_elegida
                )
                
                resultado_completo = respuesta.choices[0].message.content
                
                # Lógica para dividir la respuesta de la IA
                partes = resultado_completo.split("===SEPARADOR===")
                
                if len(partes) >= 2:
                    reporte_ats = partes[0].strip()
                    cv_optimizado = partes[1].strip()
                else:
                    reporte_ats = "Hubo un problema al separar las secciones. Aquí está todo el análisis:"
                    cv_optimizado = resultado_completo
                
                # Mostrar en pantalla
                st.success("Optimización completada con éxito")
                
                tab1, tab2 = st.tabs(["Reporte", "Ver CV Optimizado"])
                
                with tab1:
                    st.markdown(reporte_ats)
                
                with tab2:
                    st.markdown(cv_optimizado)
                
                # El botón de descarga ahora solo recibe la variable 'cv_optimizado'
                st.markdown("---")
                pdf_bytes = generar_pdf_en_memoria(cv_optimizado)
                st.download_button(
                    label="📥 Descargar tu Nuevo CV (PDF)",
                    data=pdf_bytes,
                    file_name="CV_Mejorado.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
    else:
        st.warning("⚠️ Sube tu CV y pega la vacante.") 