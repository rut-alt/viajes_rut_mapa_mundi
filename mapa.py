import streamlit as st
import pandas as pd
import json
import pycountry
import plotly.express as px
from pathlib import Path

# =====================================================
# CONFIGURACIÓN
# =====================================================

st.set_page_config(
    page_title="Mi Mapa de Viajes",
    page_icon="🌍",
    layout="wide"
)

DATA_FILE = "viajes.json"
PHOTO_DIR = Path("fotos_viajes")
PHOTO_DIR.mkdir(exist_ok=True)

# =====================================================
# CARGAR DATOS
# =====================================================

if Path(DATA_FILE).exists():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        viajes = json.load(f)
else:
    viajes = []

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.header("✈️ Nuevo viaje")

    lista_paises = sorted([
        country.name
        for country in pycountry.countries
    ])

    pais = st.selectbox(
        "País",
        lista_paises
    )

    ciudad = st.text_input("Ciudad")

    fecha = st.date_input("Fecha")

    notas = st.text_area("Notas")

    fotos = st.file_uploader(
        "Fotos",
        accept_multiple_files=True,
        type=["jpg", "jpeg", "png", "webp"]
    )

    if st.button("Guardar viaje"):

        rutas_fotos = []

        for foto in fotos or []:

            ruta = PHOTO_DIR / foto.name

            with open(ruta, "wb") as f:
                f.write(foto.getbuffer())

            rutas_fotos.append(str(ruta))

        viajes.append({
            "pais": pais,
            "ciudad": ciudad,
            "fecha": str(fecha),
            "notas": notas,
            "fotos": rutas_fotos
        })

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                viajes,
                f,
                ensure_ascii=False,
                indent=4
            )

        st.success("Viaje guardado")
        st.rerun()

# =====================================================
# TÍTULO
# =====================================================

st.title("🌍 Mi Mapa de Viajes")

st.write(
    "Registra todos tus viajes y construye tu mapa personal."
)

# =====================================================
# ESTADÍSTICAS
# =====================================================

if viajes:

    paises_visitados = sorted(
        list(set(
            v["pais"]
            for v in viajes
        ))
    )

    ciudades_visitadas = sorted(
        list(set(
            v["ciudad"]
            for v in viajes
        ))
    )

    total_paises = len(paises_visitados)
    total_ciudades = len(ciudades_visitadas)

    porcentaje = round(
        (total_paises / 195) * 100,
        2
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🌍 Países",
        total_paises
    )

    c2.metric(
        "🏙️ Ciudades",
        total_ciudades
    )

    c3.metric(
        "% Mundo",
        f"{porcentaje}%"
    )

    # =================================================
    # MAPA MUNDIAL
    # =================================================

    iso_codes = []

    for pais in paises_visitados:

        try:

            country = pycountry.countries.search_fuzzy(
                pais
            )[0]

            iso_codes.append(
                country.alpha_3
            )

        except:
            pass

    mapa_df = pd.DataFrame({
        "iso_alpha": iso_codes,
        "visitado": [1] * len(iso_codes)
    })

    fig = px.choropleth(
        mapa_df,
        locations="iso_alpha",
        color="visitado",
        projection="natural earth",
        title="🌎 Países visitados"
    )

    fig.update_layout(
        height=650,
        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # =================================================
    # PAÍSES VISITADOS
    # =================================================

    st.subheader("📍 Países visitados")

    cols = st.columns(4)

    for i, pais in enumerate(
        paises_visitados
    ):
        cols[i % 4].success(
            f"✅ {pais}"
        )

    # =================================================
    # HISTORIAL
    # =================================================

    st.subheader("✈️ Historial de viajes")

    for viaje in reversed(viajes):

        with st.expander(
            f"{viaje['pais']} - "
            f"{viaje['ciudad']} "
            f"({viaje['fecha']})"
        ):

            st.write(
                viaje["notas"]
            )

            if viaje["fotos"]:

                cols = st.columns(3)

                for i, foto in enumerate(
                    viaje["fotos"]
                ):

                    with cols[i % 3]:

                        st.image(
                            foto,
                            use_container_width=True
                        )

    # =================================================
    # GALERÍA POR PAÍS
    # =================================================

    st.subheader("📸 Galería")

    pais_seleccionado = st.selectbox(
        "Selecciona un país",
        paises_visitados
    )

    viajes_pais = [
        v
        for v in viajes
        if v["pais"] == pais_seleccionado
    ]

    for viaje in viajes_pais:

        st.markdown(
            f"### {viaje['ciudad']}"
        )

        if viaje["fotos"]:

            cols = st.columns(3)

            for i, foto in enumerate(
                viaje["fotos"]
            ):

                with cols[i % 3]:

                    st.image(
                        foto,
                        use_container_width=True
                    )

else:

    st.info(
        "Añade tu primer viaje."
    )
