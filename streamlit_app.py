import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from io import BytesIO
from evaluador_backend import extraer_items, calcular_total, clasificar


# Configuración de la interfaz
st.set_page_config(page_title="Evaluador de CV por IA", layout="centered")
st.title("📄 Evaluador automático de CVs según Resolución 897")
st.markdown("Subí un CV en PDF y el sistema analizará el contenido textual para asignar un puntaje estimado.")

# Subida del CV y nombre del docente
archivo_pdf = st.file_uploader("📥 Cargar CV (formato PDF)", type=["pdf"])
nombre = st.text_input("Nombre completo del docente evaluado")

# Función para extraer texto desde el archivo PDF
def extraer_texto(pdf_file):
    texto = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            texto += page.get_text()
    return texto

# Verificar que haya archivo y nombre cargado
if archivo_pdf and nombre:
    texto_extraido = extraer_texto(archivo_pdf)

    if st.button("🧠 Evaluar CV"):
        # Calcular puntaje con función del backend
        resultados = extraer_items(texto_extraido)
        puntaje = calcular_total(resultados)
        categoria = clasificar(puntaje)


        st.success(f"✅ Puntaje total estimado: {puntaje} puntos")

        # Determinar categoría según puntaje
        if puntaje >= 1500:
            categoria = "INVESTIGADOR SUPERIOR"
        elif puntaje >= 1000:
            categoria = "INVESTIGADOR PRINCIPAL"
        elif puntaje >= 600:
            categoria = "INVESTIGADOR INDEPENDIENTE"
        elif puntaje >= 300:
            categoria = "INVESTIGADOR ADJUNTO"
        elif puntaje >= 101:
            categoria = "INVESTIGADOR ASISTENTE"
        else:
            categoria = "BECARIO DE INICIACIÓN"

        st.info(f"📌 Categoría asignada: **{categoria}**")

        # Crear informe Excel
        df = pd.DataFrame({
            "Docente": [nombre],
            "Puntaje total": [puntaje],
            "Categoría asignada": [categoria]
        })

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        # Botón para descargar el Excel
        st.download_button(
            label="📥 Descargar informe en Excel",
            data=output,
            file_name=f"Evaluación_{nombre.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("Por favor, completá el nombre del docente y cargá un archivo PDF para continuar.")
