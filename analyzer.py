
import streamlit as st
import pandas as pd
import fitz
from analyzer import evaluar_cv

st.set_page_config(page_title="Evaluador de CV - Resolución 897", layout="centered")
st.title("📄 Evaluador automático de CVs según Resolución 897")
st.markdown("**Subí un PDF con el CV del docente. Se extraerá texto y se sugerirá una puntuación editable por ítem.**")

archivo_pdf = st.file_uploader("📥 Cargar CV en PDF", type=["pdf"])
nombre = st.text_input("Nombre completo del docente evaluado")

# Inicializar vector de respuestas (ítems 1 a 76)
respuestas = [0] * 77

def extraer_texto(pdf_file):
    texto = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            texto += page.get_text()
    return texto.lower()

# Diccionario base de sugerencias simples por ítem
palabras_clave = {
    1: ["título de grado", "farmacéutico", "licenciado", "ingeniero", "abogado"],
    2: ["especialización"],
    3: ["maestría", "magister"],
    4: ["doctorado"],
    10: ["curso", "capacitacion", "diplomatura"],
    64: ["libro"],
    65: ["capítulo de libro"],
    66: ["evento científico", "congreso"],
    67: ["tesis"],
    68: ["traducción", "artículo traducido"],
    69: ["traducción de libro"],
    70: ["reseña bibliográfica"],
    71: ["material didáctico"],
    72: ["innovación pedagógica"],
}

if archivo_pdf and nombre:
    texto_extraido = extraer_texto(archivo_pdf)

    st.subheader("✍️ Revisión de Ítems Detectados")
    for i in range(1, 77):
        sugerencia = 0
        for palabra in palabras_clave.get(i, []):
            if palabra in texto_extraido:
                sugerencia = 10 if i == 10 else 1
                break
        respuestas[i] = st.number_input(f"Ítem {i}", min_value=0, value=sugerencia, step=1)

    if st.button("Evaluar"):
        puntos, total, categoria = evaluar_cv(respuestas)
        st.success(f"✅ Puntaje Total: {total} puntos")
        st.info(f"📌 Categoría Asignada: {categoria}")

        st.markdown("### 🔍 Detalle por categoría")
        for clave, valor in puntos.items():
            st.markdown(f"- **{clave.replace('_', ' ').capitalize()}**: {valor} puntos")

        # Descargar Excel
        df = pd.DataFrame(list(puntos.items()), columns=["Categoría", "Puntaje"])
        df.loc[len(df)] = ["TOTAL", total]
        df.loc[len(df)] = ["CATEGORÍA", categoria]
        st.download_button("📥 Descargar informe Excel", data=df.to_excel(index=False), file_name=f"Evaluación_{nombre}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.warning("Por favor, completá el nombre y cargá un archivo PDF para comenzar.")
