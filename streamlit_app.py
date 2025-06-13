import streamlit as st
import pandas as pd
from evaluador_backend import extraer_items, calcular_total, clasificar

st.set_page_config(page_title="Evaluador de CV - Resolución 897", layout="centered")
st.title("📄 Evaluador automático de CVs según Resolución 897")
st.markdown("Subí un CV en PDF y el sistema analizará el contenido textual para asignar un puntaje estimado.")

# Subida de archivo y nombre
archivo_pdf = st.file_uploader("📤 Cargar CV (formato PDF)", type=["pdf"])
nombre = st.text_input("Nombre completo del docente evaluado")

if archivo_pdf and nombre:
    if st.button("🧠 Evaluar CV"):
        try:
            # Leer PDF
            import fitz  # PyMuPDF
            texto_extraido = ""
            with fitz.open(stream=archivo_pdf.read(), filetype="pdf") as doc:
                for page in doc:
                    texto_extraido += page.get_text()

            # Evaluar
            resultados = extraer_items(texto_extraido)
            puntaje = calcular_total(resultados)
            categoria = clasificar(puntaje)

            # Mostrar resultados
            st.success(f"✅ Puntaje total estimado: **{puntaje} puntos**")
            st.info(f"📌 Categoría asignada: **{categoria}**")

            with st.expander("🔍 Detalle por categoría"):
                for item, valor in resultados.items():
                    st.write(f"- **{item.replace('_', ' ').capitalize()}**: {valor} puntos")

            # Exportar informe
            df = pd.DataFrame([{
                "Nombre": nombre,
                **resultados,
                "Puntaje total": puntaje,
                "Categoría": categoria
            }])

            st.download_button("📥 Descargar informe en Excel", data=df.to_excel(index=False), file_name="informe_cv.xlsx")

        except Exception as e:
            st.error(f"❌ Error al procesar el CV: {e}")
else:
    st.warning("📌 Por favor, completá el nombre del docente y cargá un archivo PDF para continuar.")
