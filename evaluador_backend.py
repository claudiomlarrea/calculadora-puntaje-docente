import re
import unicodedata
from collections import defaultdict

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("utf-8")
    return texto

def extraer_items(texto):
    texto = normalizar_texto(texto)
    resultados = defaultdict(int)

    # Diccionario de palabras clave y pesos por ítem
    palabras_clave = {
        "formacion_academica": {
            "grado": ["titulo de grado", "abogado", "abogada", "medico", "contador", "ingeniero"],
            "especializacion": ["especializacion", "diplomatura", "postitulo", "posgrado"],
            "maestria": ["maestria", "master", "magister"],
            "doctorado": ["doctorado", "phd", "doctor en"]
        },
        "cargos_docentes": {
            "titular": ["profesor titular", "profesora titular"],
            "asociado": ["profesor asociado", "profesora asociada"],
            "adjunto": ["profesor adjunto", "profesora adjunta"],
            "jtp": ["jefe de trabajos practicos", "jtp"],
            "auxiliar": ["ayudante de primera", "ayudante de segunda", "docente auxiliar", "suplente", "docente"]
        },
        "investigacion": {
            "director": ["director de proyecto", "direccion de proyecto", "ip"],
            "integrante": ["proyecto de investigacion", "investigador", "grupo de investigacion"],
            "becario": ["becario", "becaria", "pasantia", "pasante", "recursos humanos"]
        },
        "gestion": {
            "gestion": ["coordinador", "coordinadora", "jefa de departamento", "jefe de departamento", "secretario academico"]
        },
        "formacion_continua": {
            "curso_50": [r"curso.{0,40}(?:50 horas|mas de 50|más de 50|superior a 50)"],
            "curso_25": [r"curso.{0,40}(?:25 horas|entre 25 y 50|mas de 25|más de 25)"]
        },
        "eventos": {
            "congreso": ["congreso", "jornadas", "encuentro", "simposio", "ponencia", "presentacion de trabajo"]
        }
    }

    # Puntajes máximos por área (ajustables si necesitás topes)
    puntajes = {
        "formacion_academica": {"grado": 30, "especializacion": 75, "maestria": 150, "doctorado": 250},
        "cargos_docentes": {"titular": 100, "asociado": 90, "adjunto": 80, "jtp": 70, "auxiliar": 20},
        "investigacion": {"director": 40, "integrante": 20, "becario": 10},
        "gestion": {"gestion": 20},
        "formacion_continua": {"curso_50": 20, "curso_25": 10},
        "eventos": {"congreso": 10}
    }

    # Lógica de asignación
    for area, subcategorias in palabras_clave.items():
        for subcat, claves in subcategorias.items():
            for clave in claves:
                if "curso" in subcat:  # búsqueda con regex para formaciones
                    matches = re.findall(clave, texto)
                    resultados[subcat] += len(matches) * puntajes[area][subcat]
                else:
                    if clave in texto:
                        resultados[subcat] += puntajes[area][subcat]

    return resultados

def calcular_total(resultados):
    total = sum(resultados.values())
    return total

def clasificar(total):
    if total >= 400:
        return "INVESTIGADOR INDEPENDIENTE (III)"
    elif total >= 300:
        return "INVESTIGADOR ADJUNTO (IV)"
    elif total >= 200:
        return "INVESTIGADOR ASISTENTE (V)"
    else:
        return "BECARIO DE INICIACIÓN (VI)"
