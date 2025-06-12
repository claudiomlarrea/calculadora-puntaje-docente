import streamlit as st
import pandas as pd
import xlsxwriter
import io

# Configuración inicial
st.set_page_config(page_title="Valorador Docente - UCCuyo", layout="centered")
st.title("🎓 Universidad Católica de Cuyo")
st.subheader("Secretaría de Investigación")
st.markdown("### Valorador Docente - Resolución 897")

# Ingreso del nombre del docente
docente = st.text_input("Nombre completo del docente:")

# Diccionario de bloques con ítems y puntajes máximos
bloques = {
    "Formación Académica (Max: 480)": [
        ("Títulos de Grado", 30),
        ("Cursos de Postgrado", 75),
        ("Especializaciones", 75),
        ("Maestrías", 150),
        ("Doctorados", 250)
    ],
    "Docencia Universitaria (Max: 350)": [
        ("Profesor Titular", 200),
        ("Profesor Asociado", 160),
        ("Profesor Adjunto", 120),
        ("JTP", 80),
        ("Ayudante 1ra", 40),
        ("Tribunal Concursos", 60),
        ("Docencia en Postgrados acreditados", 100),
        ("Docencia en Postgrados no acreditados", 50),
        ("Tribunal de Tesis", 60)
    ],
    "Investigación Científica (Max: 350)": [
        ("Dirección de Programa", 200),
        ("Co-dirección de Programa", 150),
        ("Dirección de Proyecto", 150),
        ("Co-dirección Proyecto", 100),
        ("Integrante con al menos 1 año", 60),
        ("Auxiliar, becario o adscripto", 30)
    ]
}

puntajes_totales = {}
total_general = 0

st.markdown("---")

# Carga de puntajes por bloque
def ingresar_bloque(nombre, items):
    st.markdown(f"#### {nombre}")
    subtotal = 0
    for item, maximo in items:
        valor = st.number_input(f"{item} (hasta {maximo} pts):", min_value=0, max_value=maximo, step=1, key=f"{nombre}-{item}")
        subtotal += valor
    st.markdown(f"**Subtotal: {subtotal} puntos**")
    return subtotal

for bloque, items in bloques.items():
    subtotal = ingresar_bloque(bloque, items)
    puntajes_totales[bloque] = subtotal
    total_general += subtotal

st.markdown("---")
st.markdown(f"### Total general: **{total_general} puntos**")

# Asignar categoría
if total_general >= 900:
    categoria = "Investigador Categoría I"
elif total_general >= 700:
    categoria = "Investigador Categoría II"
elif total_general >= 500:
    categoria = "Investigador Categoría III"
elif total_general >= 300:
    categoria = "Investigador en formación"
else:
    categoria = "No categorizado"

st.success(f"Categoría alcanzada: **{categoria}**")

# Generar Excel descargable
if st.button("📥 Descargar informe Excel"):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    df = pd.DataFrame([
        {"Bloque": bloque, "Puntaje obtenido": puntos, "Puntaje máximo": sum([p for _, p in bloques[bloque]])}
        for bloque, puntos in puntajes_totales.items()
    ])
    df.loc[len(df.index)] = ["TOTAL GENERAL", total_general, ""]
    df.loc[len(df.index)] = ["CATEGORÍA", categoria, ""]
    df.to_excel(writer, index=False, sheet_name="Informe")
    writer.close()
    output.seek(0)

    st.download_button(
        label="Descargar informe personalizado",
        data=output,
        file_name=f"Informe_{docente.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
