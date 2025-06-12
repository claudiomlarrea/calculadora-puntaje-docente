
# 📊 Calculadora de Puntaje Docente e Investigador

Esta aplicación permite evaluar automáticamente un Currículum Vitae (CV) en PDF para calcular el puntaje total y la categoría correspondiente según los criterios de categorización docente e investigadora.

## 🚀 Características principales

- Subida de CV en formato PDF
- Extracción automática de ítems categorizables
- Asignación de puntajes por ítem (hasta 81 ítems incluidos)
- Cálculo total y determinación de categoría
- Descarga de resultados en formato Excel

## 📁 Estructura del proyecto

```
calculadora_puntaje_docente/
├── streamlit_app.py
├── extractor.py
├── analyzer.py
├── pdf_reader.py
├── requirements.txt
├── README.md
```

## 🛠️ Requisitos

Instalá las dependencias con:

```bash
pip install -r requirements.txt
```

## ▶️ Cómo ejecutar la app

Desde la raíz del proyecto, ejecutá:

```bash
streamlit run streamlit_app.py
```

Luego, abrí tu navegador en `http://localhost:8501` y cargá un CV en PDF para evaluar.

## 📦 Exportación de resultados

Los resultados se pueden descargar en formato `.xlsx` directamente desde la interfaz de la aplicación.

## 👤 Autor

Claudio M. Larrea  
Repositorio: [github.com/claudiomlarrea](https://github.com/claudiomlarrea)
