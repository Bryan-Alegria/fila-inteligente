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
    st.latex(r"f(t) = 0.216(t-13)^4 - 10.8(t-13)^2 + 165")
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
        r"f'(t) = 0.864(t-13)^3 - 21.6(t-13) = (t-13)(0.864(t-13)^2 - 21.6) = 0"
    )
    st.markdown("Soluciones: $t = 8$, $t = 13$, $t = 18$")

    st.markdown("### Clasificación con segunda derivada")
    st.latex(r"f''(t) = 2.592(t-13)^2 - 21.6")
    st.latex(r"f''(8) = 43.2 > 0 \implies \text{mínimo local}")
    st.latex(r"f''(13) = -21.6 < 0 \implies \text{máximo local}")
    st.latex(r"f''(18) = 43.2 > 0 \implies \text{mínimo local}")

    st.markdown("### Interpretación")
    st.markdown(
        "- **8:00** y **18:00**: horas valle (mínima afluencia, ~30 personas)\n"
        "- **13:00**: hora pico (máxima afluencia, 165 personas)\n"
        "- La derivada $f'(t)$ indica si la fila está **creciendo** (positiva) "
        "o **decreciendo** (negativa)"
    )
