
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aviator Predictor", layout="wide")
st.title("✈️ Aviator Predictor - Versión Inicial")

st.markdown("""
**Instrucciones:**
1. Carga tu archivo Excel con el historial de rondas.
2. La app analizará las últimas 5 rondas y te dirá si hay alta probabilidad de una ronda buena (>= 2x).
3. Apuesta solo si aparece una sugerencia positiva.
""")

uploaded_file = st.file_uploader("Sube tu archivo Excel con las rondas registradas", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Archivo cargado exitosamente.")

    df["Multiplicador Final"] = pd.to_numeric(df["Multiplicador Final"], errors="coerce")
    df["Probabilidad Alta"] = False

    ventana = 5
    umbral_bajo = 2.0
    umbral_bajas_repetidas = 4

    for i in range(ventana, len(df)):
        ultimos = df["Multiplicador Final"].iloc[i-ventana:i]
        bajas = ultimos[ultimos < umbral_bajo].count()
        if bajas >= umbral_bajas_repetidas:
            df.loc[i, "Probabilidad Alta"] = True

    st.subheader("Resultado del Análisis")
    st.dataframe(df.tail(10))

    if df.iloc[-1]["Probabilidad Alta"]:
        st.markdown("### 🟢 **Recomendación:** Hay alta probabilidad de una buena ronda (>= 2x). Considera apostar.")
    else:
        st.markdown("### 🔴 **Recomendación:** Baja probabilidad. Mejor esperar.")

    with st.expander("Ver gráfica de multiplicadores"):
        st.line_chart(df[["Multiplicador Final"]])
