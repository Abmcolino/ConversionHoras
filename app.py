import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Calculadora de Horas",
    page_icon="⏱️",
    layout="centered"
)

FILE = "historial.csv"

# ---------------------------
# Cargar historial
# ---------------------------

if os.path.exists(FILE):
    historial = pd.read_csv(FILE)
else:
    historial = pd.DataFrame(columns=["persona","semana","horas"])
    historial.to_csv(FILE,index=False)

# ---------------------------
# Selección de persona
# ---------------------------

st.sidebar.title("Usuario")

personas = sorted(historial["persona"].dropna().unique())

persona = st.sidebar.selectbox(
    "¿Quién eres?",
    options=list(personas) + ["Nueva persona"]
)

if persona == "Nueva persona":
    persona = st.sidebar.text_input("Escribe tu nombre")

if persona == "":
    st.stop()

# ---------------------------
# Conversión
# ---------------------------

conversion = {
    1: 2,
    2: 4,
    3: 8,
    5: 16,
    8: 40
}

# ---------------------------
# Pestañas
# ---------------------------

tab1, tab2 = st.tabs(["Calculadora", "Historial"])

# =================================================
# CALCULADORA
# =================================================

with tab1:

    st.title("⏱️ Calculadora de Horas")

    entrada = st.text_input(
        "Vector de entrada (separado por comas)",
        placeholder="Ejemplo: 1,2,3"
    )

    if st.button("Calcular horas"):

        try:
            vector = [int(x.strip()) for x in entrada.split(",")]

            for n in vector:
                if n not in conversion:
                    st.error("Solo se permiten: 1,2,3,5,8")
                    st.stop()

            vector_convertido = [conversion[n] for n in vector]
            resultado = sum(vector_convertido)

            col1, col2 = st.columns(2)

            col1.subheader("Vector original")
            col1.success(vector)

            col2.subheader("Horas convertidas")
            col2.success(vector_convertido)

            st.metric("Horas totales", f"{resultado} h")

        except:
            st.error("Introduce números separados por comas")

# =================================================
# HISTORIAL
# =================================================

with tab2:

    st.title(f"📅 Historial de {persona}")

    semanas = [
        "9 de marzo",
        "16 de marzo",
        "23 de marzo",
        "30 de marzo"
    ]

    semana = st.selectbox("Semana", semanas)

    horas = st.number_input(
        "Horas trabajadas",
        min_value=0,
        max_value=100,
        step=1
    )

    if st.button("Guardar horas"):

        if horas > 40:
            st.warning("⚠️ No puedes superar las 40 horas por semana")

        else:

            fila = (historial["persona"] == persona) & (historial["semana"] == semana)

            if fila.any():
                historial.loc[fila, "horas"] = horas
            else:
                nueva = pd.DataFrame({
                    "persona":[persona],
                    "semana":[semana],
                    "horas":[horas]
                })

                historial = pd.concat([historial, nueva], ignore_index=True)

            historial.to_csv(FILE,index=False)

            st.success("Horas guardadas")

    st.divider()

    datos_persona = historial[historial["persona"] == persona].copy()

    if not datos_persona.empty:

        datos_persona["horas_libres"] = 40 - datos_persona["horas"]

        st.subheader("Resumen semanal")

        st.dataframe(datos_persona)

    else:

        st.info("Aún no tienes horas registradas.")

