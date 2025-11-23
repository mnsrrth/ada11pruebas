import streamlit as st

# -----------------------------------------------------
# RUTA DE DECISIÓN COMPLETA (CORREGIDA)
# -----------------------------------------------------
ruta_decision = {
    "pregunta": "¿Cuántos grupos deseas comparar?",
    "opciones": {
        "2": {
            "pregunta": "¿Los grupos son independientes?",
            "opciones": {
                "Sí": {
                    "pregunta": "¿Los datos son normales y de escala intervalo/razón?",
                    "opciones": {
                        "Sí": {"resultado": "t de Student para muestras independientes"},
                        "No": {"resultado": "U de Mann–Whitney"}
                    }
                },
                "No": {
                    "pregunta": "¿Los datos son normales?",
                    "opciones": {
                        "Sí": {"resultado": "t de Student para muestras relacionadas"},
                        "No": {"resultado": "Wilcoxon para muestras relacionadas"}
                    }
                }
            }
        },
        "3 o más": {
            "pregunta": "¿Los datos cumplen normalidad y homogeneidad de varianzas?",
            "opciones": {
                "Sí": {"resultado": "ANOVA de un factor"},
                "No": {"resultado": "Kruskal–Wallis"}
            }
        },
        "Ninguno (variables categóricas)": {
            "resultado": "Chi-cuadrada"
        }
    }
}

# -----------------------------------------------------
# INICIALIZACIÓN DE SESIÓN
# -----------------------------------------------------
if "nodo_actual" not in st.session_state:
    st.session_state.nodo_actual = ruta_decision

if "historial" not in st.session_state:
    st.session_state.historial = []


def avanzar(respuesta):
    """Avanza en la ruta de decisión según la respuesta."""
    nodo = st.session_state.nodo_actual
    st.session_state.historial.append((nodo.get("pregunta"), respuesta))

    if "opciones" in nodo and respuesta in nodo["opciones"]:
        st.session_state.nodo_actual = nodo["opciones"][respuesta]
    else:
        st.error("Ruta de decisión no válida.")


def reiniciar():
    """Reinicia la ruta completa."""
    st.session_state.nodo_actual = ruta_decision
    st.session_state.historial = []


# -----------------------------------------------------
# INTERFAZ STREAMLIT
# -----------------------------------------------------
st.title("🌿 Ruta de Decisión para Pruebas Psicométricas")

nodo = st.session_state.nodo_actual

# Si ya hay resultado final
if "resultado" in nodo:
    st.success(f"✔ **Prueba recomendada:** {nodo['resultado']}")
    
    st.subheader("Ruta tomada:")
    for pregunta, respuesta in st.session_state.historial:
        st.write(f"📌 **{pregunta}** → {respuesta}")

    st.button("Reiniciar", on_click=reiniciar)

else:
    st.subheader(nodo["pregunta"])
    opciones = list(nodo["opciones"].keys())

    respuesta = st.radio("Selecciona una opción:", opciones)

    if st.button("Continuar"):
        avanzar(respuesta)
        st.rerun()


