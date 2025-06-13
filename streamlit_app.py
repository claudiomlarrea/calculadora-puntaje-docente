import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
from io import BytesIO
from evaluador_backend import extraer_items, calcular_total, clasificar

st.set_page_config(page_title="Evaluador de CV – Resolución 897", layout="centered")

st.title("📄 Evaluador automático de CVs según Resolución 897")
st.markdown("Subí un CV en PDF y el sistema analizará el contenido textual para asignar un puntaje estimado.")

st.markdown("#### 📤 Cargar CV (formato PDF)")
archivo_pdf = st.file_uploader("Drag and drop file here", type=["pdf"])
nombre = st.text_input("Nombre completo del docente evaluado")

evaluar = st.button("🧠 Evaluar CV")

if evaluar:
    if archivo_pdf and nombre:
        try:
            # Leer PDF y extraer texto
            with fitz.open(stream=archivo_pdf.read(), filetype="pdf") as doc:
                texto_extraido = ""
                for page in doc:
                    texto_extraido += page.get_text()

            # Procesar texto con funciones del backend
            resultados = extraer_items(texto_extraido)
            puntaje = calcular_total(resultados)
            categoria = clasificar(puntaje)

            # Mostrar resultados
            st.success(f"✅ Puntaje total estimado: **{puntaje} puntos**")
            st.info(f"📌 Categoría asignada: **{categoria}**")

            # Mostrar detalle expandible
            with st.expander("🔍 Detalle por categoría"):
                for item, valor in resultados.items():
                    st.markdown(f"- **{item.replace('_', ' ').capitalize()}**: {valor} puntos")

            # Exportar informe a Excel
            df_resultado = pd.DataFrame({
                "Docente": [nombre],
                "Puntaje total": [puntaje],
                "Categoría asignada": [categoria]
            })

            for item, valor in resultados.items():
                df_resultado[item] = [valor]

            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                df_resultado.to_excel(writer, index=False, sheet_name="Resultado")

            st.download_button("💾 Descargar informe en Excel", data=buffer.getvalue(),
                               file_name=f"Evaluacion_{nombre.replace(' ', '_')}.xlsx",
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"❌ Error al procesar el CV: {e}")

    else:
        st.warning("📌 Por favor, completá el nombre del docente y cargá un archivo PDF para continuar.")
