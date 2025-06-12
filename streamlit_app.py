
import streamlit as st
from analyzer import evaluar_cv
from pdf_reader import extraer_texto_pdf
from extractor import detectar_items
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Calculadora de Puntaje Docente", layout="centered")
st.title("📊 Calculadora de Puntaje Docente e Investigador")

archivo_pdf = st.file_uploader("📄 Cargar CV en PDF", type=["pdf"])

def convertir_a_excel(puntos, total, categoria):
    df = pd.DataFrame.from_dict(puntos, orient='index', columns=['Puntaje'])
    df.loc['TOTAL'] = total
    df.loc['CATEGORÍA'] = categoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Resultados')
    output.seek(0)
    return output

if archivo_pdf is not None:
    with open("temp_cv.pdf", "wb") as f:
        f.write(archivo_pdf.read())

    texto_extraido = extraer_texto_pdf("temp_cv.pdf")
    respuestas = detectar_items(texto_extraido)

    puntos, total, categoria = evaluar_cv(respuestas)

    st.subheader("📌 Resultados de Evaluación")
    for clave, valor in puntos.items():
        st.write(f"**{clave.replace('_', ' ').capitalize()}**: {valor} puntos")
    st.markdown(f"### 🧮 Puntaje Total: **{total} puntos**")
    st.success(f"📌 Categoría asignada: **{categoria}**")

    excel_data = convertir_a_excel(puntos, total, categoria)
    st.download_button(
        label="⬇️ Descargar resultados en Excel",
        data=excel_data,
        file_name="resultado_evaluacion.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
