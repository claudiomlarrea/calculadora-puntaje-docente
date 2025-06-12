
import streamlit as st
import pandas as pd
import fitz
import re
from io import BytesIO

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Valorador Docente", layout="centered")
st.markdown("## 🎓 Universidad Católica de Cuyo")
st.markdown("### Secretaría de Investigación")
st.markdown("#### Valorador Docente - Resolución 897")

# --- NOMBRE DEL DOCENTE ---
nombre_docente = st.text_input("Nombre completo del docente:")

# --- CARGA DEL CV EN PDF ---
archivo_pdf = st.file_uploader("📄 Cargar CV en formato PDF", type=["pdf"])

# --- CÓDIGOS DE ÍTEMS Y PUNTAJES ---
codigos_items = {
    "título de grado": 30,
    "curso de postgrado": 75,
    "especialización": 75,
    "maestría": 150,
    "doctorado": 250,
    "profesor titular": 200,
    "profesor asociado": 160,
    "profesor adjunto": 120,
    "jtp": 80,
    "ayudante de primera": 40,
    "tribunal de concursos": 60,
    "docencia en postgrado acreditado": 100,
    "docencia en postgrado no acreditado": 50,
    "tribunal de tesis": 60,
    "dirección de programa": 200,
    "co-dirección de programa": 150,
    "dirección de proyecto": 150,
    "co-dirección de proyecto": 100,
    "integrante de proyecto": 60,
    "auxiliar o becario o adscripto": 30,
    "libro": 120,
    "capítulo de libro": 60,
    "patente": 60,
    "registro de propiedad intelectual": 60,
    "publicación con referato": 180,
    "publicación sin referato": 50,
}

# --- FUNCIÓN PARA EXTRAER TEXTO Y DETECTAR ÍTEMS ---
def extraer_items_desde_pdf(pdf_file):
    texto = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            texto += page.get_text()
    texto = texto.lower()

    encontrados = {}
    for clave, puntaje in codigos_items.items():
        if re.search(rf"\b{clave}\b", texto):
            encontrados[clave] = puntaje
    return encontrados

# --- FUNCIÓN PARA CATEGORIZAR ---
def determinar_categoria(total):
    if total >= 1500:
        return "INVESTIGADOR SUPERIOR (I)"
    elif total >= 1000:
        return "INVESTIGADOR PRINCIPAL (II)"
    elif total >= 600:
        return "INVESTIGADOR INDEPENDIENTE (III)"
    elif total >= 300:
        return "INVESTIGADOR ADJUNTO (IV)"
    elif total >= 1:
        return "INVESTIGADOR ASISTENTE (V)"
    else:
        return "BECARIO DE INICIACIÓN (VI)"

# --- PROCESAMIENTO ---
if archivo_pdf and nombre_docente:
    st.success("✔ CV cargado correctamente.")
    resultados = extraer_items_desde_pdf(archivo_pdf)
    total = sum(resultados.values())
    categoria = determinar_categoria(total)

    st.markdown("### 🧾 Resultados del análisis")
    df_resultados = pd.DataFrame(resultados.items(), columns=["Ítem detectado", "Puntaje asignado"])
    st.dataframe(df_resultados, use_container_width=True)
    st.markdown(f"**Total acumulado:** {total} puntos")
    st.markdown(f"**Categoría asignada:** 🏅 {categoria}")

    # --- DESCARGA DEL EXCEL ---
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df_resultados.to_excel(writer, sheet_name="Puntajes", index=False)
        resumen = pd.DataFrame({
            "Docente": [nombre_docente],
            "Puntaje total": [total],
            "Categoría": [categoria]
        })
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
    st.download_button("📥 Descargar informe en Excel", data=output.getvalue(),
                       file_name=f"Informe_{nombre_docente.replace(' ', '_')}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.info("Por favor, complete el nombre del docente y cargue un archivo PDF para comenzar.")
