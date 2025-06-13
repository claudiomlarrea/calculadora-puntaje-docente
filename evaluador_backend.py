import re
from unidecode import unidecode

def normalizar_texto(texto):
    return unidecode(texto.lower())

def calcular_puntaje(texto):
    texto = normalizar_texto(texto)

    puntaje_total = 0

    # Diccionario de palabras clave agrupadas por ítem (número ficticio, se puede reemplazar por ID real)
    palabras_clave = {
        "grado": {
            "keywords": ["titulo de grado", "abogado", "abogada", "licenciado", "licenciada", "ingeniero", "ingeniera", "médico", "médica"],
            "puntaje": 30
        },
        "especializacion": {
            "keywords": ["especializacion", "especialista en", "diplomatura", "postitulo"],
            "puntaje": 75
        },
        "maestria": {
            "keywords": ["maestria", "magister", "master en"],
            "puntaje": 150
        },
        "doctorado": {
            "keywords": ["doctorado", "doctor", "doctora"],
            "puntaje": 250
        },
        "cursos": {
            "keywords": ["curso", "taller", "seminario", "capacitacion", "jornada", "formacion continua"],
            "puntaje": 25
        },
        "docencia": {
            "keywords": ["docente", "catedra", "profesor", "profesora", "suplente", "titular", "adjunto", "jtp", "patrocinio juridico"],
            "puntaje": 20
        },
        "investigacion": {
            "keywords": ["investigacion", "proyecto de investigacion", "estancia de investigacion", "i+d", "investigador", "investigacion penal", "derecho penal"],
            "puntaje": 20
        },
        "publicaciones": {
            "keywords": ["publicacion", "articulo cientifico", "libro", "capitulo de libro", "revista arbitrada"],
            "puntaje": 30
        },
        "congresos": {
            "keywords": ["congreso", "jornadas", "ponencia", "expositor", "evento academico", "reunion cientifica"],
            "puntaje": 20
        }
    }

    # Evitar sumar múltiples veces el mismo ítem
    encontrados = []

    for key, data in palabras_clave.items():
        for keyword in data["keywords"]:
            if re.search(rf"\b{re.escape(keyword)}\b", texto):
                if key not in encontrados:
                    puntaje_total += data["puntaje"]
                    encontrados.append(key)
                    break

    return puntaje_total
