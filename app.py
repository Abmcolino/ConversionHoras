import streamlit as st

st.title("Calculadora de conversión")

conversion = {
    1: 2,
    2: 4,
    3: 8,
    5: 16,
    8: 40
}

entrada = st.text_input("Vector de entrada (separado por comas)")

if st.button("Calcular"):

    try:
        vector = [int(x.strip()) for x in entrada.split(",")]

        for n in vector:
            if n not in conversion:
                st.error("Solo se permiten: 1, 2, 3, 5, 8")
                st.stop()

        vector_convertido = [conversion[n] for n in vector]

        resultado = sum(vector_convertido)

        st.write("Vector convertido:", vector_convertido)
        st.success(f"Suma total: {resultado}")

    except:
        st.error("Introduce números separados por comas (ej: 1,2,3)")