import streamlit as st
import pandas as pd

from scraper import get_licitaciones
from scoring import calcular_score, clasificar_tipo


st.set_page_config(page_title="Radar Licitaciones", layout="wide")

st.title("🔎 Radar de Licitaciones - Air Products Chile")

# -------------------------
# BOTÓN DE ACTUALIZACIÓN
# -------------------------

if st.button("🔄 Actualizar licitaciones"):
    with st.spinner("Cargando datos desde Mercado Público..."):
        df = get_licitaciones()

        if df.empty:
            st.warning("No se pudieron obtener datos.")
        else:
            # Score
            df["texto_completo"] = (
                df["titulo"].fillna("") + " " + df["descripcion"].fillna("")
            )

            df["score"] = df["texto_completo"].apply(calcular_score)
            df["tipo"] = df["texto_completo"].apply(clasificar_tipo)


            # Filtro relevante
            df = df[df["score"] >= 40]

            # Ordenar
            df = df.sort_values(by="score", ascending=False)

            st.session_state["data"] = df


# -------------------------
# MOSTRAR RESULTADOS
# -------------------------

if "data" in st.session_state:
    df = st.session_state["data"]

    st.subheader(f"✅ Oportunidades detectadas: {len(df)}")

    st.dataframe(
        df[["titulo", "entidad", "fecha_cierre", "tipo", "score"]],
        use_container_width=True
    )

    # -------------------------
    # DETALLE
    # -------------------------

    seleccion = st.selectbox(
        "Selecciona una licitación para ver detalle",
        df.index
    )

    if seleccion is not None:
        st.markdown("### 📄 Detalle")

        st.write("**Título:**", df.loc[seleccion, "titulo"])
        st.write("**Entidad:**", df.loc[seleccion, "entidad"])
        st.write("**Fecha cierre:**", df.loc[seleccion, "fecha_cierre"])
        st.write("**Tipo:**", df.loc[seleccion, "tipo"])
        st.write("**Score:**", df.loc[seleccion, "score"])

        st.markdown("**Descripción:**")
        st.write(df.loc[seleccion, "descripcion"])

        st.markdown("🔗 [Ver en Mercado Público](" + df.loc[seleccion, "link"] + ")")
