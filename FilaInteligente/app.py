import streamlit as st
from modelo import predecir
from graficas import graficar_afluencia, graficar_derivada

st.set_page_config(page_title="Fila Inteligente", layout="wide")
st.title("Fila Inteligente")
st.markdown(
    "Prediccion de congestion en el casino universitario "
    "usando Calculo Diferencial."
)

with st.sidebar:
    st.header("Selecciona una hora")
    hora = st.slider(
        "Hora de consulta",
        min_value=6.0, max_value=20.0, value=13.0, step=0.25,
        format="%.2f h",
    )
    st.caption("Desliza para explorar como cambia la afluencia durante el dia.")

    st.divider()
    st.markdown("### Sobre el modelo")
    st.latex(r"f(t) = 0.05(t-13)^4 - 2.5(t-13)^2 + 60")
    st.caption(
        "Funcion cuartica que modela la cantidad de personas en la fila "
        "del casino en funcion de la hora del dia."
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

st.plotly_chart(graficar_afluencia(t_input=hora), use_container_width=True)
st.plotly_chart(graficar_derivada(t_input=hora), use_container_width=True)

with st.expander("Analisis matematico", expanded=True):
    st.markdown("### Puntos criticos")
    st.latex(
        r"f'(t) = 0.20(t-13)^3 - 5(t-13) = (t-13)(0.20(t-13)^2 - 5) = 0"
    )
    st.markdown("Soluciones: $t = 8$, $t = 13$, $t = 18$")

    st.markdown("### Clasificacion con segunda derivada")
    st.latex(r"f''(t) = 0.60(t-13)^2 - 5")
    st.latex(r"f''(8) = 10 > 0 \implies \text{minimo local}")
    st.latex(r"f''(13) = -5 < 0 \implies \text{maximo local}")
    st.latex(r"f''(18) = 10 > 0 \implies \text{minimo local}")

    st.markdown("### Interpretacion")
    st.markdown(
        "- **8:00** y **18:00**: horas valle (minima afluencia, ~29 personas)\n"
        "- **13:00**: hora pico (maxima afluencia, 60 personas)\n"
        "- La derivada $f'(t)$ indica si la fila esta **creciendo** (positiva) "
        "o **decreciendo** (negativa)"
    )
