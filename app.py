import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Ruta de Decisión - Pruebas Estadísticas", layout="centered")

# ----------------------------------------------------
# Cargar árbol de decisión desde GitHub RAW
# ----------------------------------------------------
@st.cache_data
def cargar_arbol(url):
    return json.loads(pd.read_csv(url).to_json(orient="records"))[0]

# Pega tu enlace RAW:
URL = "AQUI_TU_URL_RAW"
arbol = cargar_arbol(URL)

# ----------------------------------------------------
# Estado
# ----------------------------------------------------
if "nodo" not in st.session_state:
    st.session_state.nodo = "inicio"

if "historial" not in st.session_state:
    st.session_state.historial = []

# ----------------------------------------------------
# Función para avanzar en el árbol
# ----------------------------------------------------
def avanzar(siguiente):
    st.session_state.historial.append(st.session_state.nodo)
    st.session_state.nodo = siguiente

# ----------------------------------------------------
# Mostrar nodo actual
# ----------------------------------------------------
nodo = arbol[st.session_state.nodo]

st.title("📊 Ruta de Decisión – Selección de Pruebas Estadísticas")

st.subheader(nodo["pregunta"])

# Si es un nodo final → mostrar resultado
if nodo["tipo"] == "final":

    st.success(f"### ✔ Prueba recomendada: **{nodo['resultado']}**")
    st.write(f"**Justificación:** {nodo['explicacion']}")

    if st.button("🔄 Reiniciar"):
        st.session_state.nodo = "inicio"
        st.session_state.historial = []
        st.rerun()

else:
    # Mostrar opciones
    for opcion in nodo["opciones"]:
        if st.button(opcion["texto"]):
            avanzar(opcion["siguiente"])
