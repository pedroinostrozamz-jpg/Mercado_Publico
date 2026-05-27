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
            "link": f"https://www.mercadopublico.cl/Home/BusquedaLicitacion?textoBusqueda={lic.get('CodigoExterno')}",
            "titulo": lic.get("Nombre"),
            "descripcion": lic.get("Descripcion"),
            "entidad": lic.get("NombreOrganismo"),
            "fecha_cierre": lic.get("FechaCierre"),
        })

    return pd.DataFrame(rows)

    def obtener_tipo_licitacion(codigo):
    if not isinstance(codigo, str):
        return "Desconocido"

    try:
        # Extraer parte final (ej: LR26)
        tipo_raw = codigo.split("-")[-1]

        # Extraer solo letras (ej: LR)
        tipo = ''.join([c for c in tipo_raw if c.isalpha()])

        tipos_map = {
            # Públicas
            "L1": "Licitación Pública menor a 100 UTM",
            "LE": "Licitación Pública entre 100 y 1000 UTM",
            "LP": "Licitación Pública >= 1.000 y < 2.000 UTM",
            "LQ": "Licitación Pública >= 2.000 y < 5.000 UTM",
            "LR": "Licitación Pública >= 5.000 UTM",
            "LS": "Licitación Pública servicios personales especializados",

            # Obras
            "O1": "Licitación Pública de Obras",
            "O2": "Licitación Privada de Obras",

            # Privadas
            "E2": "Licitación Privada < 100 UTM",
            "CO": "Licitación Privada >= 100 y < 1.000 UTM",
            "B2": "Licitación Privada >= 1.000 y < 2.000 UTM",
            "H2": "Licitación Privada >= 2.000 y < 5.000 UTM",
            "I2": "Licitación Privada > 5.000 UTM",

            # Innovación
            "CI": "Contrato de Innovación con preselección",
            "DC": "Diálogos Competitivos",
            "CI2": "Contrato Innovación Fase 2",
            "DC2": "Diálogos Competitivos Fase 2"
        }

        return tipos_map.get(tipo, f"Tipo desconocido ({tipo})")

    except:
        return "Desconocido"
