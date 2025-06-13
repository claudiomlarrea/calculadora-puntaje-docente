import re
from unidecode import unidecode

# Diccionario con palabras clave por ítem
palabras_clave = {
    1: ["titulo de grado", "farmaceutica", "farmaceutica nacional"],
    2: ["profesora de educacion secundaria", "profesionalizacion docente"],
    3: ["formacion docente", "profesorado universitario", "actualizacion academica"],
    10: ["curso", "jornada", "taller", "capacitacion", "diplomatura", "congreso", "perfeccionamiento"],
    5: ["docente universitaria", "profesora en uccuyo", "clase en grado"],
    18: ["miembro del departamento de investigacion", "integrante de departamento de investigacion"],
    66: ["participacion en congreso", "evento academico", "presentacion oral", "reunion cientifica"],
    71: ["material educativo", "diseno de proyectos", "material didactico", "sistematizacion didactica"],
    40: ["formacion de recursos humanos", "direccion de tesis", "tutorias de grado", "desarrollo profesional"],
}

# Puntajes por ítem
puntajes = {
    1: 30, 2: 75, 3: 150, 5: 100, 10: 10, 18: 50,
    40: 50, 66: 70, 71: 20
}

# Máximos por bloque (clave: ítems implicados, valor: puntaje máximo)
bloques = {
    (1, 2, 3): 300,
    (5,): 300,
    (10,): 75,
    (18,): 200,
    (40,): 200,
    (66, 71): 600
}

def normalizar_texto(texto):
    return unidecode(texto.lower())

def calcular_puntaje(texto_cv):
    texto = normalizar_texto(texto_cv)
    puntajes_detectados = {k: 0 for k in puntajes}

    # Buscar coincidencias
    for item, keywords in palabras_clave.items():
        for palabra in keywords:
            if re.search(rf"\b{re.escape(palabra)}\b", texto):
                if item == 10:  # Curso: acumula hasta 75 puntos
                    puntajes_detectados[item] += 10
                else:
                    puntajes_detectados[item] = puntajes[item]
                break  # Si encuentra uno, no sigue buscando más para ese ítem

    # Aplicar topes por bloque
    puntaje_final = 0
    for items, max_puntaje in bloques.items():
        subtotal = sum(puntajes_detectados[i] for i in items)
        puntaje_final += min(subtotal, max_puntaje)

    return puntaje_final
