
import fitz  # PyMuPDF

def extraer_texto_pdf(ruta_pdf):
    texto = ""
    with fitz.open(ruta_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto.lower()  # Pasamos todo a minúsculas para facilitar la búsqueda
