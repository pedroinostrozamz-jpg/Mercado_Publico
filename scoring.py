def calcular_score(texto):
   
    if not isinstance(texto, str):
        return 0

    texto = texto.lower()

    keywords_alta = [
        "oxígeno", "oxigeno",
        "nitrógeno", "nitrogeno",
        "argón", "argon",
        "acetileno",
        "gases",
        "gases medicinales"
    ]

   
    keywords_media = [
        "soldadura",
        "corte",
        "electrodo",
        "insumos industriales",
        "suministro"
    ]

  
    keywords_negativas = [
        "alimentos",
        "aseo",
        "oficina",
        "ropa",
        "publicidad"
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


    if "hospital" in texto:
        score += 20

    if "clinica" in texto or "clínica" in texto:
        score += 20

    if "licitación" in texto and "suministro" in texto:
        score += 10

    return score



def clasificar_tipo(texto):
    if not isinstance(texto, str):
        return "Otro"

    texto = texto.lower()

    if any(k in texto for k in [
        "oxígeno", "oxigeno",
        "nitrógeno", "nitrogeno",
        "argón", "argon",
        "acetileno",
        "gases"
    ]):
        return "Gas"

    elif any(k in texto for k in [
        "soldadura",
        "electrodo",
        "corte"
    ]):
        return "Soldadura"

    else:
        return "Otro"
