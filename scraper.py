import requests
import pandas as pd
import streamlit as st

def get_licitaciones():
    url = st.secrets["API_URL"]
    ticket = st.secrets["API_KEY"]

    params = {
    "estado": "publicada",
    "ticket": ticket,
    "cantidad": 100  
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return pd.DataFrame()

    data = response.json()

    licitaciones = data.get("Listado", [])

    rows = []

    for lic in licitaciones:
        rows.append({
            "codigo": lic.get("CodigoExterno"),
            "titulo": lic.get("Nombre"),
            "descripcion": lic.get("Descripcion"),
            "entidad": lic.get("NombreOrganismo"),
            "fecha_cierre": lic.get("FechaCierre"),
            "link": f"https://www.mercadopublico.cl/Procurement/Modules/RFB/DetailsAcquisition.aspx?qs={lic.get('CodigoExterno')}"
        })

    return pd.DataFrame(rows)
