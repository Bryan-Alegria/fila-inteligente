import numpy as np
import plotly.graph_objects as go
from modelo import f, f_prima, encontrar_puntos_criticos, clasificar_puntos_criticos

COLOR_WHITE = "#E0E0E0"
COLOR_RED = "#D01B1B"
COLOR_GREEN = "#00C48C"
COLOR_ORANGE = "#FF8C00"
BG_TRANSPARENT = "rgba(0,0,0,0)"


def _rango_t(paso=0.05):
    return np.arange(8, 22 + paso, paso)


def graficar_afluencia(t_input=None):
    t_vals = _rango_t()
    y_vals = [f(t) for t in t_vals]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t_vals, y=y_vals, mode="lines",
        line=dict(color=COLOR_WHITE, width=2.5),
        name="f(t)  Afluencia",
    ))

    clasif = clasificar_puntos_criticos()
    for t_p, tipo in clasif.items():
        color = COLOR_RED if "maximo" in tipo else COLOR_GREEN
        simbolo = "triangle-down" if "maximo" in tipo else "triangle-up"
        fig.add_trace(go.Scatter(
            x=[t_p], y=[f(t_p)],
            mode="markers+text",
            marker=dict(size=16, color=color, symbol=simbolo,
                        line=dict(width=1, color=color)),
            text=[f"t={t_p:.0f}h"],
            textposition="top center",
            textfont=dict(color=color, size=13),
            name=f"t={t_p:.0f}h ({tipo})",
        ))

    if t_input is not None:
        fig.add_trace(go.Scatter(
            x=[t_input], y=[f(t_input)],
            mode="markers",
            marker=dict(size=18, color=COLOR_ORANGE, symbol="x-thin",
                        line=dict(width=2.5, color=COLOR_ORANGE)),
            name=f"Tu hora: {t_input:.2f}h",
        ))

    fig.update_layout(
        title=dict(
            text="Funcion de Afluencia  f(t)",
            font=dict(size=18, color=COLOR_WHITE),
            x=0.01,
        ),
        xaxis=dict(
            title="Hora del dia",
            tickmode="linear", tick0=8, dtick=2,
            tickformat=".0f:00",
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            title_font=dict(color="#A0A0A0", size=13),
            tickfont=dict(color="#A0A0A0", size=12),
        ),
        yaxis=dict(
            title="Personas",
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            title_font=dict(color="#A0A0A0", size=13),
            tickfont=dict(color="#A0A0A0", size=12),
        ),
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        hovermode="x unified",
        legend=dict(
            orientation="v",
            yanchor="top", y=0.98,
            xanchor="right", x=0.98,
            font=dict(color="#A0A0A0", size=11),
            bgcolor="rgba(30,30,30,0.8)",
        ),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def graficar_derivada(t_input=None):
    t_vals = _rango_t()
    y_vals = [f_prima(t) for t in t_vals]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=t_vals, y=y_vals, mode="lines",
        line=dict(color=COLOR_RED, width=2),
        name="f'(t)  Derivada",
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="rgba(255,255,255,0.15)",
                  line_width=1)

    for t_p in encontrar_puntos_criticos():
        fig.add_trace(go.Scatter(
            x=[t_p], y=[0],
            mode="markers",
            marker=dict(size=14, color="#A855F7", symbol="cross",
                        line=dict(width=1.5, color="#A855F7")),
            name=f"f'({t_p:.0f})=0",
        ))

    if t_input is not None:
        deriv = f_prima(t_input)
        fig.add_trace(go.Scatter(
            x=[t_input], y=[deriv],
            mode="markers+text",
            marker=dict(size=18, color=COLOR_ORANGE, symbol="x-thin",
                        line=dict(width=2.5, color=COLOR_ORANGE)),
            text=[f"f'({t_input:.2f}) = {deriv:.1f}"],
            textposition="top center",
            textfont=dict(color=COLOR_ORANGE, size=11),
            name=f"Tu hora: {t_input:.2f}h",
        ))

    fig.update_layout(
        title=dict(
            text="Derivada f'(t)  Tasa de Cambio",
            font=dict(size=18, color=COLOR_WHITE),
            x=0.01,
        ),
        xaxis=dict(
            title="Hora del dia",
            tickmode="linear", tick0=8, dtick=2,
            tickformat=".0f:00",
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            title_font=dict(color="#A0A0A0", size=13),
            tickfont=dict(color="#A0A0A0", size=12),
        ),
        yaxis=dict(
            title="Tasa de cambio (pers/h)",
            gridcolor="rgba(255,255,255,0.06)",
            zeroline=False,
            title_font=dict(color="#A0A0A0", size=13),
            tickfont=dict(color="#A0A0A0", size=12),
        ),
        paper_bgcolor=BG_TRANSPARENT,
        plot_bgcolor=BG_TRANSPARENT,
        hovermode="x unified",
        legend=dict(
            orientation="v",
            yanchor="top", y=0.98,
            xanchor="right", x=0.98,
            font=dict(color="#A0A0A0", size=11),
            bgcolor="rgba(30,30,30,0.8)",
        ),
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig
