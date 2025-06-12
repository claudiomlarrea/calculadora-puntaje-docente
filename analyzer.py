
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
        "desarrollos": 100,
        "nuevos_aportes": 100
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
        "nuevos_aportes": min(sum(respuestas[77:82]), maximos["nuevos_aportes"]),
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
