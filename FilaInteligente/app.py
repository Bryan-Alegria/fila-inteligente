import streamlit as st
import time
from modelo import predecir, hora_a_string
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

if "hora" not in st.session_state:
    st.session_state.hora = 15.0
if "demo_running" not in st.session_state:
    st.session_state.demo_running = False

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
        'C\u00e1lculo Diferencial</p>',
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
        min_value=8.0, max_value=22.0,
        value=st.session_state.hora, step=0.25,
        format="%.2f h",
        label_visibility="collapsed",
        key="slider_hora",
    )
    st.session_state.hora = hora

    st.caption(
        "Desliza para explorar c\u00f3mo cambia la afluencia "
        "durante el d\u00eda."
    )

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("Iniciar Demo",
                     use_container_width=True,
                     disabled=st.session_state.demo_running):
            st.session_state.demo_running = True
            st.session_state.hora = 8.0
            st.rerun()
    with col_b2:
        if st.button("Detener Demo",
                     use_container_width=True,
                     disabled=not st.session_state.demo_running):
            st.session_state.demo_running = False
            st.rerun()

    st.divider()
    st.markdown(
        '<p style="font-size:14px;font-weight:600;color:#1A1A1A;">'
        'Sobre el modelo</p>',
        unsafe_allow_html=True,
    )
    st.latex(
        r"f'(t) = k\,(t-8)(t-13)(t-18)\;"
        r"e^{-(t-13)^2/\sigma^2}"
    )
    st.caption(
        "Modelo polin\u00f3mico-exponencial. "
        "3 puntos cr\u00edticos: 8h, 13h, 18h."
    )

main_area = st.empty()


def renderizar_dashboard(hora_actual):
    pred = predecir(hora_actual)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Personas estimadas",
                  f"{pred['afluencia']} pers.")
    with col2:
        st.metric("Estado",
                  "Hora pico" if pred["es_hora_pico"]
                  else "Hora valle")
    with col3:
        st.metric("Tendencia", pred["tendencia"].capitalize())
    with col4:
        st.metric(
            "Hora recomendada",
            hora_a_string(pred["horario_recomendado"])
            if pred["horario_recomendado"] is not None
            else "N/A",
        )

    banner_clase = "" if pred["es_hora_pico"] else "ok"
    st.markdown(
        f'<div class="reco-banner {banner_clase}">'
        f'{pred["mensaje"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<h2 style="font-size:18px;font-weight:700;color:#1A1A1A;'
        'margin:0;">Gr\u00e1ficas de Afluencia y Derivada</h2>',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        graficar_afluencia(t_input=hora_actual),
        width="stretch",
    )
    st.plotly_chart(
        graficar_derivada(t_input=hora_actual),
        width="stretch",
    )

    with st.expander("An\u00e1lisis matem\u00e1tico",
                     expanded=True):
        col_izq, col_der = st.columns(2)

        with col_izq:
            st.markdown(
                '<h3 style="font-size:15px;font-weight:600;'
                'color:#1A1A1A;">Puntos cr\u00edticos</h3>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='color:#555;font-size:13px;"
                "line-height:1.7;'>"
                "Para encontrar los puntos cr\u00edticos "
                "igualamos la derivada a cero: "
                "<b>f'(t) = 0</b>. Esto nos indica "
                "d\u00f3nde la funci\u00f3n deja de crecer "
                "o decrecer.</p>",
                unsafe_allow_html=True,
            )
            st.latex(
                r"f'(t) = k\,(t-8)(t-13)(t-18)\,"
                r"e^{-(t-13)^2/\sigma^2} = 0"
            )
            st.markdown(
                "<p style='color:#555;font-size:13px;"
                "line-height:1.7;'>"
                "Como la exponencial nunca se anula, "
                "factorizamos:</p>",
                unsafe_allow_html=True,
            )
            st.latex(
                r"(t-8)(t-13)(t-18) = 0"
            )
            st.markdown(
                "<p style='color:#555;font-size:13px;"
                "line-height:1.7;'>"
                "Soluciones:<br>"
                "<b>t\u2081 = 8</b> &rarr; 8:00 h<br>"
                "<b>t\u2082 = 13</b> &rarr; 13:00 h<br>"
                "<b>t\u2083 = 18</b> &rarr; 18:00 h</p>",
                unsafe_allow_html=True,
            )

            st.markdown(
                '<h3 style="font-size:15px;font-weight:600;'
                'color:#1A1A1A;margin-top:20px;">'
                'Clasificaci\u00f3n con segunda derivada</h3>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='color:#555;font-size:13px;"
                "line-height:1.7;'>"
                "Usamos el criterio de la segunda derivada: "
                "si <b>f''(t) &gt; 0</b> es un "
                "<span style='color:#2E8B57;'>"
                "m\u00ednimo local</span>, "
                "si <b>f''(t) &lt; 0</b> es un "
                "<span style='color:#D01B1B;'>"
                "m\u00e1ximo local</span>.</p>",
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
            <td style="padding:5px 6px;color:#888;">t</td>
            <td style="padding:5px 6px;color:#888;">f''(t)</td>
            <td style="padding:5px 6px;color:#888;">Tipo</td>
            <td style="padding:5px 6px;color:#888;">
            Interpretaci&oacute;n real</td></tr>
            <tr style="border-bottom:1px solid #E5E5E5;">
            <td style="padding:5px 6px;">8:00</td>
            <td style="padding:5px 6px;color:#2E8B57;">+9.9</td>
            <td style="padding:5px 6px;color:#2E8B57;">
            M&iacute;nimo local</td>
            <td style="padding:5px 6px;color:#555;">
            Casino casi vac&iacute;o</td>
            </tr>
            <tr style="border-bottom:1px solid #E5E5E5;">
            <td style="padding:5px 6px;">13:00</td>
            <td style="padding:5px 6px;color:#D01B1B;">-38.4</td>
            <td style="padding:5px 6px;color:#D01B1B;">
            M&aacute;ximo local</td>
            <td style="padding:5px 6px;color:#555;">
            Casino al 85% de capacidad</td>
            </tr>
            <tr>
            <td style="padding:5px 6px;">18:00</td>
            <td style="padding:5px 6px;color:#2E8B57;">+9.9</td>
            <td style="padding:5px 6px;color:#2E8B57;">
            M&iacute;nimo local</td>
            <td style="padding:5px 6px;color:#555;">
            Casino casi vac&iacute;o</td>
            </tr>
            </table>
            """, unsafe_allow_html=True)

        with col_der:
            st.markdown(
                '<h3 style="font-size:15px;font-weight:600;'
                'color:#1A1A1A;">Interpretaci\u00f3n</h3>',
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='color:#555;font-size:13px;"
                "line-height:1.8;'>"
                "<b>&iquest;Qu\u00e9 significa f'(t)?</b><br>"
                "La derivada representa la "
                "<b>tasa de cambio</b> de personas "
                "en la fila. "
                "Cuando <span style='color:#2E8B57;'>"
                "f'(t) &gt; 0</span> la fila "
                "<span style='color:#2E8B57;'>"
                "est\u00e1 creciendo</span>, "
                "cuando <span style='color:#D01B1B;'>"
                "f'(t) &lt; 0</span> la fila "
                "<span style='color:#D01B1B;'>"
                "est\u00e1 decreciendo</span>. "
                "Cuando <b>f'(t) = 0</b> se alcanza un "
                "punto cr\u00edtico: la fila deja de crecer "
                "o decrecer moment\u00e1neamente.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='color:#555;font-size:13px;"
                "line-height:1.8;'>"
                "<b>Horarios clave:</b><br>"
                "<span style='color:#2E8B57;font-weight:600;'>"
                "8:00</span> y "
                "<span style='color:#2E8B57;font-weight:600;'>"
                "18:00</span> son horas valle con "
                "m\u00ednima afluencia (~30 personas).<br>"
                "<span style='color:#D01B1B;font-weight:600;'>"
                "13:00</span> es la hora pico con "
                "m\u00e1xima afluencia "
                "(165 personas, ~85% de capacidad).<br><br>"
                "El factor exponencial amortigua el "
                "crecimiento en los extremos del dominio, "
                "manteniendo la funci\u00f3n acotada en "
                "[30, 165] personas."
                "</p>",
                unsafe_allow_html=True,
            )


if st.session_state.demo_running:
    t = st.session_state.hora
    while t <= 22.0:
        st.session_state.hora = t
        with main_area.container():
            renderizar_dashboard(t)
        t += 0.5
        time.sleep(0.3)
    st.session_state.demo_running = False
    st.session_state.hora = 22.0
    st.rerun()
else:
    with main_area.container():
        renderizar_dashboard(st.session_state.hora)
