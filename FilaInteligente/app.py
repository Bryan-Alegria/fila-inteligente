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
    st.latex(r"f(t) = \frac{1}{49}(t-15)^4 - 2(t-15)^2 + 75")
    st.caption(
        "Función cuártica que modela la cantidad de personas en la fila "
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
        r"f'(t) = \frac{4}{49}(t-15)^3 - 4(t-15) = (t-15)\left(\frac{4}{49}(t-15)^2 - 4\right) = 0"
    )
    st.markdown("Soluciones: $t = 8$, $t = 15$, $t = 22$")

    st.markdown("### Clasificación con segunda derivada")
    st.latex(r"f''(t) = \frac{12}{49}(t-15)^2 - 4")
    st.latex(r"f''(8) = 8 > 0 \implies \text{mínimo local}")
    st.latex(r"f''(15) = -4 < 0 \implies \text{máximo local}")
    st.latex(r"f''(22) = 8 > 0 \implies \text{mínimo local}")

    st.markdown("### Interpretación")
    st.markdown(
        "- **8:00** y **22:00**: horas valle (mínima afluencia, ~26 personas)\n"
        "- **15:00**: hora pico (máxima afluencia, 75 personas)\n"
        "- La derivada $f'(t)$ indica si la fila está **creciendo** (positiva) "
        "o **decreciendo** (negativa)"
    )
