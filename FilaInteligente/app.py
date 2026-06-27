import streamlit as st
from modelo import predecir
from graficas import graficar_afluencia, graficar_derivada

st.set_page_config(page_title="Fila Inteligente", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

div[data-testid="stMetric"] {
    background: #F8F8F8;
    border: 1px solid #E5E5E5;
    padding: 10px 12px;
    border-radius: 0;
}

div[data-testid="stMetric"] label {
    font-size: 11px !important;
    white-space: nowrap;
    overflow: visible;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    font-size: 22px !important;
}

.reco-banner {
    background: #FFF3F3;
    border: 1px solid #FFD4D4;
    border-left: 3px solid #D01B1B;
    padding: 12px 16px;
    margin: 8px 0 16px 0;
    font-size: 14px;
    color: #1A1A1A;
}

.reco-banner.ok {
    background: #F0FFF4;
    border-color: #C6F6D5;
    border-left-color: #2E8B57;
}
</style>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.markdown(
        '<h1 style="font-size:24px;font-weight:700;color:#1A1A1A;'
        'margin:0;">Fila Inteligente</h1>',
        unsafe_allow_html=True,
    )
with col_h2:
    st.markdown(
        '<p style="font-size:13px;color:#888;text-align:right;'
        'margin:8px 0 0 0;">INACAP Puente Alto &middot; '
        'Cálculo Diferencial</p>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<hr style="border-color:#E5E5E5;margin:4px 0 12px 0;">',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        '<p style="font-size:16px;font-weight:600;color:#1A1A1A;'
        'margin-bottom:4px;">Selecciona una hora</p>',
        unsafe_allow_html=True,
    )
    hora = st.slider(
        "Hora",
        min_value=8.0, max_value=22.0, value=15.0, step=0.25,
        format="%.2f h",
        label_visibility="collapsed",
    )
    st.caption(
        "Desliza para explorar como cambia la afluencia "
        "durante el día."
    )

    st.divider()
    st.markdown(
        '<p style="font-size:14px;font-weight:600;color:#1A1A1A;">'
        'Sobre el modelo</p>',
        unsafe_allow_html=True,
    )
    st.latex(
        r"f'(t) = k\,(t-8)(t-13)(t-18)\,e^{-(t-13)^2/\sigma^2}"
    )
    st.caption(
        "Modelo polinómico-exponencial. "
        "3 puntos críticos: 8h, 13h, 18h."
    )

pred = predecir(hora)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Personas estimadas", f"{pred['afluencia']} pers.")
with col2:
    st.metric("Estado",
              "Hora pico" if pred["es_hora_pico"] else "Hora valle")
with col3:
    st.metric("Tendencia", pred["tendencia"].capitalize())
with col4:
    st.metric(
        "Hora recomendada",
        f"{pred['horario_recomendado']:.0f}:00"
        if pred["horario_recomendado"] is not None
        else "N/A",
    )

banner_clase = "" if pred["es_hora_pico"] else "ok"
st.markdown(
    f'<div class="reco-banner {banner_clase}">{pred["mensaje"]}</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<h2 style="font-size:18px;font-weight:700;color:#1A1A1A;'
    'margin:0;">Gráficas de Afluencia y Derivada</h2>',
    unsafe_allow_html=True,
)

st.plotly_chart(graficar_afluencia(t_input=hora), width="stretch")
st.plotly_chart(graficar_derivada(t_input=hora), width="stretch")

with st.expander("Análisis matemático", expanded=True):
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown(
            '<h3 style="font-size:15px;font-weight:600;color:#1A1A1A;">'
            'Puntos críticos</h3>',
            unsafe_allow_html=True,
        )
        st.latex(
            r"f'(t) = k\,(t-8)(t-13)(t-18)\,"
            r"e^{-(t-13)^2/\sigma^2} = 0"
        )
        st.markdown(
            "<p style='color:#555;'>Soluciones: "
            "<b>t = 8</b>, <b>t = 13</b>, <b>t = 18</b></p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<h3 style="font-size:15px;font-weight:600;color:#1A1A1A;">'
            'Clasificación con segunda derivada</h3>',
            unsafe_allow_html=True,
        )
        st.latex(
            r"f''(t) = k\,e^{-(t-13)^2/\sigma^2}"
            r"\left[g'(t) - "
            r"\frac{2(t-13)}{\sigma^2}g(t)\right]"
        )

        st.markdown("""
        <table style="width:100%;border-collapse:collapse;
        font-size:13px;color:#1A1A1A;">
        <tr style="border-bottom:1px solid #E5E5E5;">
        <td style="padding:6px 8px;color:#888;">t</td>
        <td style="padding:6px 8px;color:#888;">f''(t)</td>
        <td style="padding:6px 8px;color:#888;">Tipo</td></tr>
        <tr style="border-bottom:1px solid #E5E5E5;">
        <td style="padding:6px 8px;">8:00</td>
        <td style="padding:6px 8px;color:#2E8B57;">+9.9</td>
        <td style="padding:6px 8px;color:#2E8B57;">Mínimo local</td>
        </tr>
        <tr style="border-bottom:1px solid #E5E5E5;">
        <td style="padding:6px 8px;">13:00</td>
        <td style="padding:6px 8px;color:#D01B1B;">-38.4</td>
        <td style="padding:6px 8px;color:#D01B1B;">Máximo local</td>
        </tr>
        <tr>
        <td style="padding:6px 8px;">18:00</td>
        <td style="padding:6px 8px;color:#2E8B57;">+9.9</td>
        <td style="padding:6px 8px;color:#2E8B57;">Mínimo local</td>
        </tr>
        </table>
        """, unsafe_allow_html=True)

    with col_der:
        st.markdown(
            '<h3 style="font-size:15px;font-weight:600;color:#1A1A1A;">'
            'Interpretación</h3>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#555;font-size:14px;line-height:1.9;'>"
            "<span style='color:#2E8B57;font-weight:600;'>8:00</span> "
            "y "
            "<span style='color:#2E8B57;font-weight:600;'>18:00</span> "
            "son horas valle con minima afluencia "
            "(~30 personas).<br><br>"
            "<span style='color:#D01B1B;font-weight:600;'>13:00</span> "
            "es la hora pico con maxima afluencia "
            "(165 personas, ~85% de capacidad).<br><br>"
            "La derivada "
            "<span style='color:#D01B1B;'>f'(t)</span> "
            "indica si la fila esta "
            "<span style='color:#2E8B57;'>creciendo</span> "
            "(f' &gt; 0) o "
            "<span style='color:#D01B1B;'>decreciendo</span> "
            "(f' &lt; 0).<br><br>"
            "El factor exponencial amortigua el crecimiento "
            "en los extremos del dominio, manteniendo la funcion "
            "acotada en [30, 165] personas."
            "</p>",
            unsafe_allow_html=True,
        )
