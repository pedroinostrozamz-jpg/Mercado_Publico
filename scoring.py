def calcular_score(texto):
    if not isinstance(texto, str):
        return 0

    texto = texto.lower()

    keywords_alta = ["oxígeno", "oxigeno", "nitrógeno", "nitrogeno", "argón", "argon", "Gases"]

    score = 0

    for k in keywords_alta:
        if k in texto:
            score += 40

    return score


def clasificar_tipo(texto):
    if not isinstance(texto, str):
        return "Otro"

    texto = texto.lower()

    if any(k in texto for k in ["oxígeno", "oxigeno", "nitrógeno", "nitrogeno", "argón", "argon", "gases"]):
        return "Gas"
    elif "soldadura" in texto:
        return "Soldadura"
    else:
        return "Otro"
