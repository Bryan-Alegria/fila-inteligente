import streamlit as st
from modelo import predecir
from graficas import graficar_afluencia, graficar_derivada

st.set_page_config(page_title="Fila Inteligente", layout="wide")
st.title("Fila Inteligente")
st.markdown(
    "Predicción de congestión en el casino universitario "
    "usando Cálculo Diferencial."
)

with st.sidebar:
    st.header("Selecciona una hora")
    hora = st.slider(
        "Hora de consulta",
        min_value=8.0, max_value=22.0, value=15.0, step=0.25,
        format="%.2f h",
    )
    st.caption("Desliza para explorar como cambia la afluencia durante el dia.")

    st.divider()
    st.markdown("### Sobre el modelo")
    st.latex(r"f(t) = 30 + 135 \cdot e^{-(t-13)^2/8}")
    st.caption(
        "Función gaussiana que modela la cantidad de personas en la fila "
        "del casino en función de la hora del día."
    )

pred = predecir(hora)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Personas estimadas", f"{pred['afluencia']} pers.")
col2.metric("Estado", "Hora pico" if pred["es_hora_pico"] else "Hora valle")
col3.metric("Tendencia", pred["tendencia"])
col4.metric(
    "Hora recomendada",
    f"{pred['horario_recomendado']:.0f}:00",
)

st.info(pred["mensaje"])

st.plotly_chart(graficar_afluencia(t_input=hora), width="stretch")
st.plotly_chart(graficar_derivada(t_input=hora), width="stretch")

with st.expander("Análisis matemático", expanded=True):
    st.markdown("### Puntos críticos")
    st.latex(
        r"f'(t) = -33.75\,(t-13)\,e^{-(t-13)^2/8} = 0"
    )
    st.markdown("Solución: $t = 13$ (único punto crítico)")

    st.markdown("### Clasificación con segunda derivada")
    st.latex(r"f''(t) = -33.75\,e^{-(t-13)^2/8}\left(1 - \frac{(t-13)^2}{4}\right)")
    st.latex(r"f''(13) = -33.75 < 0 \implies \text{máximo local}")

    st.markdown("### Interpretación")
    st.markdown(
        "- **8:00** y **22:00**: horas de menor afluencia (~36 personas, mínimos en los extremos del dominio)\n"
        "- **13:00**: hora pico (máxima afluencia, 165 personas, ~85% de capacidad)\n"
        "- La derivada $f'(t)$ indica si la fila está **creciendo** (positiva) "
        "o **decreciendo** (negativa)\n"
        "- La función se mantiene en $[30, 165] \\subset [0, 192]$ en todo el dominio $[8, 22]$"
    )
