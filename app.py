import streamlit as st
import requests
import json

# ---------------------------
# Cargar JSON desde GitHub
# ---------------------------
URL_RAW_JSON = "https://raw.githubusercontent.com/USUARIO/REPOSITORIO/main/ruta_decision.json"

def cargar_ruta():
    response = requests.get(URL_RAW_JSON)
    return response.json()

ruta = cargar_ruta()

# Inicializar estado
if "nodo_actual" not in st.session_state:
    st.session_state.nodo_actual = ruta
if "historial" not in st.session_state:
    st.session_state.historial = []

# Función para avanzar
def avanzar(respuesta):
    nodo = st.session_state.nodo_actual
    st.session_state.historial.append(respuesta)

    if "opciones" in nodo and respuesta in nodo["opciones"]:
        st.session_state.nodo_actual = nodo["opciones"][respuesta]
    else:
        st.error("Error en la ruta de decisión.")
        return


# Función para reiniciar
def reiniciar():
    st.session_state.nodo_actual = ruta
    st.session_state.historial = []


# ---------------------------
# INTERFAZ STREAMLIT
# ---------------------------
st.title("🌿 Ruta de Decisión para Pruebas Psicométricas")

nodo = st.session_state.nodo_actual

# Si ya hay resultado, mostrarlo
if "resultado" in nodo:
    st.success(f"✔ **Prueba recomendada: {nodo['resultado']}**")
    st.button("Reiniciar", on_click=reiniciar)
else:
    st.subheader(nodo["pregunta"])

    opciones = list(nodo["opciones"].keys())
    respuesta = st.radio("Selecciona una opción:", opciones)

    if st.button("Continuar"):
        avanzar(respuesta)
        st.rerun()

