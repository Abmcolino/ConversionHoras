import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Gestor de Horas",
    page_icon="⏱️",
    layout="centered"
)

FILE = "historial.csv"

# -----------------------
# Cargar historial
# -----------------------

if os.path.exists(FILE):
    historial = pd.read_csv(FILE)
else:
    historial = pd.DataFrame(columns=["persona","semana","horas"])
    historial.to_csv(FILE,index=False)

# -----------------------
# Selección de persona
# -----------------------

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

# -----------------------
# Conversión de horas
# -----------------------

conversion = {
    1: 2,
    2: 4,
    3: 8,
    5: 16,
    8: 40
}

semanas = [
    "9 de marzo",
    "16 de marzo",
    "23 de marzo",
    "30 de marzo"
]

# -----------------------
# Pestañas
# -----------------------

tab1, tab2 = st.tabs(["Calculadora", "Historial"])

# ===================================================
# CALCULADORA
# ===================================================

with tab1:

    st.title("⏱️ Calculadora de Horas")

    semana = st.selectbox("Selecciona la semana", semanas)

    entrada = st.text_input(
        "Vector de tareas (separado por comas)",
        placeholder="Ejemplo: 1,2,3"
    )

    if st.button("Calcular y guardar horas"):

        try:
            vector = [int(x.strip()) for x in entrada.split(",")]

            for n in vector:
                if n not in conversion:
                    st.error("Solo se permiten: 1,2,3,5,8")
                    st.stop()

            vector_convertido = [conversion[n] for n in vector]
            horas_calculadas = sum(vector_convertido)

            st.write("Vector convertido:", vector_convertido)
            st.metric("Horas calculadas", f"{horas_calculadas} h")

            # buscar registro existente
            fila = (historial["persona"] == persona) & (historial["semana"] == semana)

            if fila.any():
                horas_actuales = historial.loc[fila,"horas"].values[0]
            else:
                horas_actuales = 0

            nuevas_horas = horas_actuales + horas_calculadas

            if nuevas_horas > 40:

                st.warning(
                    f"⚠️ Superarías las 40 horas. "
                    f"Actualmente tienes {horas_actuales} h."
                )

            else:

                if fila.any():
                    historial.loc[fila,"horas"] = nuevas_horas
                else:

                    nueva_fila = pd.DataFrame({
                        "persona":[persona],
                        "semana":[semana],
                        "horas":[horas_calculadas]
                    })

                    historial = pd.concat([historial,nueva_fila],ignore_index=True)

                historial.to_csv(FILE,index=False)

                st.success(
                    f"Horas añadidas correctamente. "
                    f"Total en la semana: {nuevas_horas} h"
                )

        except:
            st.error("Introduce números separados por comas")

# ===================================================
# HISTORIAL
# ===================================================

with tab2:

    st.title(f"📅 Historial de {persona}")

    datos_persona = historial[historial["persona"] == persona].copy()

    if not datos_persona.empty:

        datos_persona["horas_libres"] = 40 - datos_persona["horas"]

        st.dataframe(datos_persona)

    else:

        st.info("Aún no tienes horas registradas.")
