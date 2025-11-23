import streamlit as st
import pandas as pd

# ---------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------
st.set_page_config(page_title="Dashboard Rutas de Decisión", layout="centered")

# ---------------------------------------------------
# CARGA DE ÍTEMS DESDE GITHUB
# ---------------------------------------------------
@st.cache_data
def cargar_items(url):
    return pd.read_csv(url)

# Pega aquí tu enlace RAW de GitHub:
URL = "AQUI_TU_URL_RAW"
items = cargar_items(URL)

# ---------------------------------------------------
# MANEJO DE ESTADO
# ---------------------------------------------------
if "indice" not in st.session_state:
    st.session_state.indice = 0

if "respondido" not in st.session_state:
    st.session_state.respondido = False

if "retro" not in st.session_state:
    st.session_state.retro = ""

if "puntos" not in st.session_state:
    st.session_state.puntos = 0

# ---------------------------------------------------
# FUNCIÓN PARA PROCESAR RESPUESTA
# ---------------------------------------------------
def procesar_respuesta(opcion, correcta, retro):
    if opcion == correcta:
        st.session_state.retro = f"✅ Respuesta correcta. {retro}"
        st.session_state.puntos += 1
    else:
        st.session_state.retro = f"❌ Incorrecto. La correcta era {correcta.upper()}. {retro}"

    st.session_state.respondido = True

# ---------------------------------------------------
# MOSTRAR PREGUNTA ACTUAL
# ---------------------------------------------------
if st.session_state.indice < len(items):

    item = items.iloc[st.session_state.indice]

    st.title("📊 Dashboard: Ruta de Decisión en Pruebas Psicométricas")
    st.write(f"### Pregunta {st.session_state.indice + 1} de {len(items)}")
    st.write(f"**{item['pregunta']}**")

    opciones = {
        "a": item["opcion_a"],
        "b": item["opcion_b"],
        "c": item["opcion_c"],
        "d": item["opcion_d"]
    }

    opcion_seleccionada = st.radio(
        "Selecciona una opción:",
        options=list(opciones.keys()),
        format_func=lambda x: f"{x.upper()}. {opciones[x]}",
        disabled=st.session_state.respondido
    )

    if st.button("Responder", disabled=st.session_state.respondido):
        procesar_respuesta(opcion_seleccionada, item["correcta"], item["retro"])

    if st.session_state.respondido:
        st.info(st.session_state.retro)

        if st.button("Siguiente ➡️"):
            st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.retro = ""
            st.rerun()

else:
    # ---------------------------------------------------
    # RESULTADO FINAL
    # ---------------------------------------------------
    st.title("🎉 ¡Has completado la evaluación!")
    total = len(items)
    puntuacion = st.session_state.puntos
    porcentaje = round((puntuacion / total) * 100, 2)

    st.write(f"### Puntaje final: **{puntuacion} / {total}**")
    st.write(f"### Porcentaje: **{porcentaje}%**")

    # Mensaje final
    if porcentaje == 100:
        st.success("🔥 ¡Excelente dominio de las rutas de decisión!")
    elif porcentaje >= 80:
        st.success("Muy bien, manejas bien las pruebas psicométricas.")
    elif porcentaje >= 60:
        st.warning("Bien, pero puedes reforzar algunos conceptos.")
    else:
        st.error("Necesitas repasar
