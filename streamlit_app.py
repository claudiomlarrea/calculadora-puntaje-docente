import streamlit as st
import pandas as pd
from io import BytesIO
from evaluador_backend import extraer_items, calcular_total, clasificar
import fitz  # PyMuPDF

st.set_page_config(page_title="Evaluador de CV – Resolución 897", layout="centered")

st.title("📄 Evaluador automático de CVs según Resolución 897")
st.markdown("Subí un CV en PDF y el sistema analizará el contenido textual para asignar un puntaje estimado.")

# Subida del archivo
archivo_pdf = st.file_uploader("📤 Cargar CV (formato PDF)", type=["pdf"])
nombre = st.text_input("Nombre completo del docente evaluado")

if st.button("🧠 Evaluar CV") and archivo_pdf and nombre:
    try:
        # Extraer texto del PDF
        texto_extraido = ""
        with fitz.open(stream=archivo_pdf.read(), filetype="pdf") as doc:
            for page in doc:
                texto_extraido += page.get_text()

        # Evaluar el texto
        puntajes = extraer_items(texto_extraido)
        total = calcular_total(puntajes)
        categoria = clasificar(total)

        # Mostrar resultados
        st.success(f"✅ Puntaje total estimado: {total} puntos")
        st.info(f"📌 Categoría asignada: **{categoria}**")

        with st.expander("🔍 Detalle por categoría"):
            for item, valor in puntajes.items():
                st.markdown(f"- **{item.replace('_', ' ').capitalize()}**: {valor} puntos")

        # Generar Excel para descarga
        df = pd.DataFrame([{
            "Nombre del docente": nombre,
            "Puntaje total": total,
            "Categoría asignada": categoria,
            **puntajes
        }])

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Evaluación')
        output.seek(0)

        st.download_button(
            label="📥 Descargar informe en Excel",
            data=output,
            file_name=f"informe_{nombre.replace(' ', '_')}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el CV: {e}")

elif st.button("🧠 Evaluar CV"):
    st.warning("📌 Por favor, completá el nombre del docente y cargá un archivo PDF para continuar.")
