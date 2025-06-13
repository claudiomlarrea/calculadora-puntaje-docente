import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

st.set_page_config(page_title="Evaluador de CV - Resolución 897", layout="centered")
st.title("📄 Evaluador automático de CVs según Resolución 897")
st.markdown("**Subí un PDF con el CV del docente. Se extraerá texto y se sugerirá una puntuación editable por ítem.**")

archivo_pdf = st.file_uploader("📥 Cargar CV en PDF", type=["pdf"])
nombre = st.text_input("Nombre completo del docente evaluado")

respuestas = [0] * 77

def extraer_texto(pdf_file):
    texto = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            texto += page.get_text()
    return texto.lower()

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

def evaluar_cv(respuestas):
    maximos = {
        "formacion_academica": 300,
        "cargos_docentes": 300,
        "cursos_posgrado": 75,
        "cargos_id": 50,
        "carrera_conicet": 100,
        "cargos_otras_instituciones": 200,
        "gestion_institucional": 300,
        "formacion_rh": 200,
        "financiamiento_cyt": 150,
        "evaluaciones_premios": 200,
        "evaluacion_proyectos": 300,
        "premios": 100,
        "producciones": 600,
        "desarrollos": 100
    }

    puntos = {
        "formacion_academica": min(sum(respuestas[1:5]), maximos["formacion_academica"]),
        "cargos_docentes": min(sum(respuestas[5:10]), maximos["cargos_docentes"]),
        "cursos_posgrado": min(respuestas[10], maximos["cursos_posgrado"]),
        "cargos_id": min(sum(respuestas[11:13]), maximos["cargos_id"]),
        "carrera_conicet": min(sum(respuestas[13:18]), maximos["carrera_conicet"]),
        "cargos_otras_instituciones": min(sum(respuestas[18:21]), maximos["cargos_otras_instituciones"]),
        "gestion_institucional": min(sum(respuestas[21:40]), maximos["gestion_institucional"]),
        "formacion_rh": min(sum(respuestas[40:46]), maximos["formacion_rh"]),
        "financiamiento_cyt": min(sum(respuestas[46:48]), maximos["financiamiento_cyt"]),
        "evaluaciones_premios": min(sum(respuestas[48:56]), maximos["evaluaciones_premios"]),
        "evaluacion_proyectos": min(sum(respuestas[56:63]), maximos["evaluacion_proyectos"]),
        "premios": min(respuestas[63], maximos["premios"]),
        "producciones": min(sum(respuestas[64:73]), maximos["producciones"]),
        "desarrollos": min(sum(respuestas[73:77]), maximos["desarrollos"]),
    }

    total = sum(puntos.values())

    if total >= 1500:
        categoria = "INVESTIGADOR SUPERIOR"
    elif total >= 1000:
        categoria = "INVESTIGADOR PRINCIPAL"
    elif total >= 600:
        categoria = "INVESTIGADOR INDEPENDIENTE"
    elif total >= 300:
        categoria = "INVESTIGADOR ADJUNTO"
    elif total >= 101:
        categoria = "INVESTIGADOR ASISTENTE"
    else:
        categoria = "BECARIO DE INICIACIÓN"

    return puntos, total, categoria

# === APP ===
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

        df = pd.DataFrame(list(puntos.items()), columns=["Categoría", "Puntaje"])
        df.loc[len(df)] = ["TOTAL", total]
        df.loc[len(df)] = ["CATEGORÍA", categoria]
        st.download_button("📥 Descargar informe Excel", data=df.to_excel(index=False), file_name=f"Evaluación_{nombre}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    st.warning("Por favor, completá el nombre y cargá un archivo PDF para comenzar.")
