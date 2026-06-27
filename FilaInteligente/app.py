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
    st.latex(
        r"f'(t) = k\,(t-8)(t-13)(t-18)\,e^{-(t-13)^2/\sigma^2}"
    )
    st.caption(
        "Modelo polinomico-exponencial que representa la afluencia "
        "al casino en funcion de la hora del dia."
    )

pred = predecir(hora)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Personas estimadas", f"{pred['afluencia']} pers.")
col2.metric("Estado", "Hora pico" if pred["es_hora_pico"] else "Hora valle")
col3.metric("Tendencia", pred["tendencia"])
col4.metric(
    "Hora recomendada",
    f"{pred['horario_recomendado']:.0f}:00"
    if pred["horario_recomendado"] is not None
    else "N/A",
)

st.info(pred["mensaje"])

st.plotly_chart(graficar_afluencia(t_input=hora), width="stretch")
st.plotly_chart(graficar_derivada(t_input=hora), width="stretch")

with st.expander("Análisis matemático", expanded=True):
    st.markdown("### Puntos críticos")
    st.latex(
        r"f'(t) = k\,(t-8)(t-13)(t-18)\,e^{-(t-13)^2/\sigma^2} = 0"
    )
    st.markdown(
        "Soluciones: $t = 8$, $t = 13$, $t = 18$ "
        "(la exponencial nunca se anula)"
    )

    st.markdown("### Clasificación con segunda derivada")
    st.latex(
        r"f''(t) = k\,e^{-(t-13)^2/\sigma^2}\left[g'(t) - "
        r"\frac{2(t-13)}{\sigma^2}g(t)\right]"
    )
    st.latex(r"f''(8) = k \cdot 50 \cdot e^{-25/\sigma^2} > 0 \implies \text{mínimo local}")
    st.latex(r"f''(13) = -25k < 0 \implies \text{máximo local}")
    st.latex(r"f''(18) = k \cdot 50 \cdot e^{-25/\sigma^2} > 0 \implies \text{mínimo local}")

    st.markdown("### Interpretación")
    st.markdown(
        "- **8:00** y **18:00**: horas valle (~30 personas, mínimos locales)\n"
        "- **13:00**: hora pico (165 personas, máximo local)\n"
        "- **22:00**: afluencia baja (~44 personas, dentro del rango permitido)\n"
        "- La función se mantiene en $[30, 165] \\subset [0, 192]$ en todo el dominio\n"
        "- El factor exponencial amortigua el crecimiento en los extremos"
    )
