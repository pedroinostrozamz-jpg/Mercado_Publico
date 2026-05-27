import streamlit as st
import pandas as pd

from scraper import get_licitaciones
from scoring import calcular_score, clasificar_tipo


# ------------------------------------------
# CONFIGURACIÓN APP
# ------------------------------------------
st.set_page_config(page_title="Radar Licitaciones", layout="wide")

st.title("Radar de Licitaciones - Air Products Chile")

st.write("Monitoreo automático de oportunidades desde Mercado Público")

# ------------------------------------------
# BOTÓN DE ACTUALIZACIÓN
# ------------------------------------------
if st.button("Actualizar licitaciones"):

    with st.spinner("Obteniendo licitaciones..."):

        df = get_licitaciones()

        if df.empty:
            st.warning("No se encontraron licitaciones")
        else:
            # -------------------------
            # LIMPIEZA
            # -------------------------
            df["titulo"] = df["titulo"].fillna("")
            df["descripcion"] = df["descripcion"].fillna("")

            # -------------------------
            # TEXTO COMPLETO
            # -------------------------
            df["texto_completo"] = df["titulo"] + " " + df["descripcion"]

            # -------------------------
            # SCORING
            # -------------------------
            df["score"] = df["texto_completo"].apply(calcular_score)

            # -------------------------
            # CLASIFICACIÓN
            # -------------------------
            df["tipo"] = df["texto_completo"].apply(clasificar_tipo)

            # -------------------------
            # FILTRO
            # -------------------------
            df = df[df["score"] >= 40]

            # -------------------------
            # ORDEN
            # -------------------------
            df = df.sort_values(by="score", ascending=False)

            # -------------------------
            # GUARDAR EN SESSION
            # -------------------------
            st.session_state["data"] = df

# ------------------------------------------
# MOSTRAR RESULTADOS
# ------------------------------------------
if "data" in st.session_state:

    df = st.session_state["data"]

    st.subheader(f"Oportunidades detectadas: {len(df)}")

    # -------------------------
    # TABLA PRINCIPAL
    # -------------------------
    st.dataframe(
        df[[
            "codigo",
            "tipo_licitacion",  
            "titulo",
            "entidad",
            "fecha_cierre",
            "tipo",
            "score"
        ]],
        use_container_width=True
    )

    # -------------------------
    # SELECCIÓN
    # -------------------------
    seleccion = st.selectbox(
        "Selecciona una licitación para ver detalle",
        df.index
    )

    # -------------------------
    # DETALLE
    # -------------------------
    if seleccion is not None:

        st.markdown("## Detalle de Licitación")

        st.write("**Código:**", df.loc[seleccion, "codigo"])
        st.write("**Tipo de Licitación:**", df.loc[seleccion, "tipo_licitacion"])  
        st.write("**Entidad:**", df.loc[seleccion, "entidad"])
        st.write("**Fecha de cierre:**", df.loc[seleccion, "fecha_cierre"])
        st.write("**Tipo (clasificación):**", df.loc[seleccion, "tipo"])
        st.write("**Score:**", df.loc[seleccion, "score"])

        st.markdown("### Descripción")
        st.write(df.loc[seleccion, "descripcion"])

        st.markdown("### Abrir en Mercado Público")
        st.markdown(df.loc[seleccion, "link"])
