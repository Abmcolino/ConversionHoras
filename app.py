import streamlit as st

st.set_page_config(
    page_title="Calculadora de Horas",
    page_icon="⏱️",
    layout="centered"
)

st.title("⏱️ Calculadora de Horas")
st.markdown("Introduce un **vector separado por comas**.")

st.info("Valores permitidos: **1, 2, 3, 5, 8**")

conversion = {
    1: 2,
    2: 4,
    3: 8,
    5: 16,
    8: 40
}

entrada = st.text_input(
    "Vector de entrada",
    placeholder="Ejemplo: 1,2,3"
)

if st.button("Calcular horas", use_container_width=True):

    try:
        vector = [int(x.strip()) for x in entrada.split(",")]

        for n in vector:
            if n not in conversion:
                st.error("❌ Solo se permiten los valores: 1, 2, 3, 5, 8")
                st.stop()

        vector_convertido = [conversion[n] for n in vector]
        resultado = sum(vector_convertido)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Vector original")
            st.success(vector)

        with col2:
            st.subheader("Horas convertidas")
            st.success(vector_convertido)

        st.divider()

        st.subheader("Total acumulado")

        st.metric(
            label="Horas totales",
            value=f"{resultado} h"
        )

    except:
        st.error("⚠️ Introduce números separados por comas (ej: 1,2,3)")
