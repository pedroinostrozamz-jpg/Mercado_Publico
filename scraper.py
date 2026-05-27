import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st

def get_licitaciones():
    url = st.secrets["API_URL"]
    api_key = st.secrets["API_KEY"]

    response = requests.get(url + "?ticket=" + api_key)
    
    if response.status_code != 200:
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")

    licitaciones = []

    # ⚠️ Esto lo ajustaremos cuando veamos la estructura real
    items = soup.find_all("item")

    for item in items:
        titulo = item.find("title")
        descripcion = item.find("description")
        entidad = item.find("organismo")
        fecha_cierre = item.find("fechacierre")
        link = item.find("url")

        licitaciones.append({
            "titulo": titulo.text if titulo else "",
            "descripcion": descripcion.text if descripcion else "",
            "entidad": entidad.text if entidad else "",
            "fecha_cierre": fecha_cierre.text if fecha_cierre else "",
            "link": link.text if link else ""
        })

    df = pd.DataFrame(licitaciones)

    return df
