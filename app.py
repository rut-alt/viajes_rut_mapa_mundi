import streamlit as st

st.set_page_config(
    page_title="Mapa de Viajes",
    layout="wide"
)

st.title("Mapa de Viajes")

opcion = st.radio(
    "",
    ["Iniciar sesión", "Crear cuenta"]
)

if opcion == "Crear cuenta":

    usuario = st.text_input("Usuario")
    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Crear cuenta"):
        st.success("Cuenta creada")

else:

    usuario = st.text_input("Usuario")
    password = st.text_input(
        "Contraseña",
        type="password"
    )

    if st.button("Entrar"):
        st.success("Login correcto")
