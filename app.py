import streamlit as st

# -----------------------------------------------------
# RUTA DE DECISIÓN COMPLETA (EMBEBIDA EN EL CÓDIGO)
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


    if st.button("Continuar"):
        avanzar(respuesta)
        st.rerun()

