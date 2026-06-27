import streamlit as st
from modelo import predecir
from graficas import graficar_afluencia, graficar_derivada

st.set_page_config(page_title="Fila Inteligente", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: #0D0D0D;
}

[data-testid="stSidebar"] {
    background: #161616;
    min-width: 220px;
    max-width: 220px;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] .stCaption {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] hr {
    border-color: #2A2A2A;
}

div[data-testid="stMetric"] {
    background: #1E1E1E;
    border: 1px solid #2A2A2A;
    padding: 10px 14px;
    border-radius: 0;
}

div[data-testid="stMetric"] label {
    color: #A0A0A0 !important;
    font-size: 12px !important;
}

div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 28px !important;
}

.metric-peak div[data-testid="stMetric"] {
    border-left: 3px solid #D01B1B !important;
}

.metric-valley div[data-testid="stMetric"] {
    border-left: 3px solid #00C48C !important;
}

.header-title {
    font-size: 22px;
    font-weight: 700;
    color: #FFFFFF;
}

.header-subtitle {
    font-size: 13px;
    color: #A0A0A0;
}

.section-title {
    font-size: 18px;
    font-weight: 700;
    color: #FFFFFF;
    margin-top: 8px;
}

.stAlert {
    background: #1E1E1E !important;
    border: 1px solid #D01B1B !important;
    color: #FFFFFF !important;
    border-radius: 0;
}

.stAlert p { font-size: 14px !important; }

[data-testid="stExpander"] {
    background: #1E1E1E;
    border: 1px solid #2A2A2A;
}

[data-testid="stExpander"] details summary p {
    color: #FFFFFF !important;
    font-size: 16px !important;
    font-weight: 600;
}

[data-testid="stExpander"] [data-testid="stMarkdownContainer"] {
    color: #A0A0A0;
}

div.stSlider > div[data-baseweb="slider"] > div {
    background: #D01B1B;
}

div.stSlider [data-testid="stThumbValue"] {
    background: #D01B1B;
    color: #FFFFFF;
}

.stDivider {
    border-color: #2A2A2A;
}

a, .stMarkdown a { color: #D01B1B; }
</style>
""", unsafe_allow_html=True)

col_h1, col_h2 = st.columns([3, 2])
with col_h1:
    st.markdown(
        '<div class="header-title">Fila Inteligente</div>',
        unsafe_allow_html=True,
    )
with col_h2:
    st.markdown(
        '<div class="header-subtitle" style="text-align:right;">'
        'INACAP Puente Alto &middot; Calculo Diferencial'
        '</div>',
        unsafe_allow_html=True,
    )

st.markdown('<hr style="border-color:#2A2A2A;margin:6px 0 16px 0;">',
            unsafe_allow_html=True)

with st.sidebar:
    st.markdown(
        '<div class="section-title">Selecciona una hora</div>',
        unsafe_allow_html=True,
    )
    hora = st.slider(
        "Hora",
        min_value=8.0, max_value=22.0, value=15.0, step=0.25,
        format="%.2f h",
        label_visibility="collapsed",
    )
    st.caption("Desliza para explorar la afluencia durante el dia.")

    st.divider()

    pred = predecir(hora)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Personas", f"{pred['afluencia']}")
    with col_b:
        st.metric("Estado",
                  "Pico" if pred["es_hora_pico"] else "Valle")

    col_c, col_d = st.columns(2)
    with col_c:
        st.metric("Tendencia", pred["tendencia"])
    with col_d:
        st.metric(
            "Recomendada",
            f"{pred['horario_recomendado']:.0f}h"
            if pred["horario_recomendado"] is not None
            else "N/A",
        )

    if pred["es_hora_pico"]:
        clase_alerta = "metric-peak"
    else:
        clase_alerta = "metric-valley"

    alerta_html = (
        f'<div class="{clase_alerta}" style="margin-top:12px;'
        f'padding:12px 14px;background:#1E1E1E;'
        f'border:1px solid #2A2A2A;'
        f'border-left:3px solid '
        f'{"#D01B1B" if pred["es_hora_pico"] else "#00C48C"};'
        f'font-size:13px;color:#E0E0E0;line-height:1.5;">'
        f'{pred["mensaje"]}</div>'
    )
    st.markdown(alerta_html, unsafe_allow_html=True)

    st.divider()
    st.markdown(
        '<div class="section-title" style="font-size:14px;">'
        'Sobre el modelo</div>',
        unsafe_allow_html=True,
    )
    st.latex(
        r"f'(t) = k\,(t-8)(t-13)(t-18)\,e^{-(t-13)^2/\sigma^2}"
    )
    st.caption(
        "Modelo polinomico-exponencial. "
        "3 puntos criticos: 8h, 13h, 18h."
    )

st.markdown(
    '<div class="section-title">'
    'Graficas de Afluencia y Derivada</div>',
    unsafe_allow_html=True,
)

st.plotly_chart(graficar_afluencia(t_input=hora), width="stretch")
st.plotly_chart(graficar_derivada(t_input=hora), width="stretch")

with st.expander("Analisis matematico", expanded=True):
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.markdown(
            '<div class="section-title" style="font-size:15px;">'
            'Puntos criticos</div>',
            unsafe_allow_html=True,
        )
        st.latex(
            r"f'(t) = k\,(t-8)(t-13)(t-18)\,"
            r"e^{-(t-13)^2/\sigma^2} = 0"
        )
        st.markdown(
            "<p style='color:#A0A0A0;'>Soluciones: "
            "$t = 8$, $t = 13$, $t = 18$</p>",
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-title" style="font-size:15px;">'
            'Clasificacion</div>',
            unsafe_allow_html=True,
        )
        st.latex(
            r"f''(t) = k\,e^{-(t-13)^2/\sigma^2}"
            r"\left[g'(t) - "
            r"\frac{2(t-13)}{\sigma^2}g(t)\right]"
        )

        tabla_html = """
        <table style="width:100%;border-collapse:collapse;
        font-size:13px;color:#E0E0E0;">
        <tr style="border-bottom:1px solid #2A2A2A;">
        <td style="padding:6px 8px;color:#A0A0A0;">t</td>
        <td style="padding:6px 8px;color:#A0A0A0;">f''(t)</td>
        <td style="padding:6px 8px;color:#A0A0A0;">Tipo</td></tr>
        <tr style="border-bottom:1px solid #2A2A2A;">
        <td style="padding:6px 8px;">8:00</td>
        <td style="padding:6px 8px;color:#00C48C;">+9.9</td>
        <td style="padding:6px 8px;color:#00C48C;">Minimo local</td>
        </tr>
        <tr style="border-bottom:1px solid #2A2A2A;">
        <td style="padding:6px 8px;">13:00</td>
        <td style="padding:6px 8px;color:#D01B1B;">-38.4</td>
        <td style="padding:6px 8px;color:#D01B1B;">Maximo local</td>
        </tr>
        <tr>
        <td style="padding:6px 8px;">18:00</td>
        <td style="padding:6px 8px;color:#00C48C;">+9.9</td>
        <td style="padding:6px 8px;color:#00C48C;">Minimo local</td>
        </tr>
        </table>
        """
        st.markdown(tabla_html, unsafe_allow_html=True)

    with col_der:
        st.markdown(
            '<div class="section-title" style="font-size:15px;">'
            'Interpretacion</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='color:#A0A0A0;font-size:14px;line-height:1.8;'>"
            "<span style='color:#00C48C;font-weight:600;'>8:00</span> "
            "y "
            "<span style='color:#00C48C;font-weight:600;'>18:00</span> "
            "son horas valle con minima afluencia "
            "(~30 personas).<br><br>"
            "<span style='color:#D01B1B;font-weight:600;'>13:00</span> "
            "es la hora pico con maxima afluencia "
            "(165 personas, ~85% de capacidad).<br><br>"
            "La derivada "
            "<span style='color:#D01B1B;'>f'(t)</span> "
            "indica si la fila esta "
            "<span style='color:#00C48C;'>creciendo</span> "
            "(f' &gt; 0) o "
            "<span style='color:#D01B1B;'>decreciendo</span> "
            "(f' &lt; 0).<br><br>"
            "El factor exponencial amortigua el crecimiento "
            "en los extremos del dominio, manteniendo la funcion "
            "acotada en [30, 165] personas."
            "</p>",
            unsafe_allow_html=True,
        )
