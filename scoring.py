def calcular_score(texto):
    if not texto:
        return 0

    texto = texto.lower()

    keywords_alta = [
        "oxigeno", "oxígeno",
        "nitrogeno", "nitrógeno",
        "argon", "argón",
        "acetileno"
    ]

    keywords_media = [
        "soldadura",
        "corte",
        "electrodo",
        "insumos industriales"
    ]

    keywords_negativas = [
        "alimentos",
        "aseo",
        "oficina",
        "ropa"
    ]

    score = 0

    for k in keywords_alta:
        if k in texto:
            score += 40

    for k in keywords_media:
        if k in texto:
            score += 20

    for k in keywords_negativas:
        if k in texto:
            score -= 30

    return score


def clasificar_tipo(texto):
    texto = texto.lower()

    if any(k in texto for k in ["oxígeno", "nitrógeno", "argón", "acetileno"]):
        return "Gas"
    elif "soldadura" in texto:
        return "Soldadura"
    else:
        return "Otro"
