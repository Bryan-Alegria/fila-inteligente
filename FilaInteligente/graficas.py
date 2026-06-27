import numpy as np
import plotly.graph_objects as go
from modelo import f, f_prima, encontrar_puntos_criticos, clasificar_puntos_criticos


def _rango_t(paso=0.05):
    return np.arange(6, 20 + paso, paso)


def graficar_afluencia(t_input=None):
    t_vals = _rango_t()
    y_vals = [f(t) for t in t_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_vals, y=y_vals, mode="lines",
        line=dict(color="royalblue", width=2),
        name="f(t) - Afluencia",
    ))

    clasif = clasificar_puntos_criticos()
    for t_p, tipo in clasif.items():
        color = "crimson" if "maximo" in tipo else "seagreen"
        fig.add_trace(go.Scatter(
            x=[t_p], y=[f(t_p)],
            mode="markers+text",
            marker=dict(size=14, color=color, symbol="diamond"),
            text=[f"t={t_p:.0f}h"],
            textposition="top center",
            name=f"t={t_p:.0f}h ({tipo})",
        ))

    if t_input is not None:
        fig.add_trace(go.Scatter(
            x=[t_input], y=[f(t_input)],
            mode="markers",
            marker=dict(size=16, color="darkorange", symbol="x-thin", line=dict(width=2)),
            name=f"Tu hora: {t_input:.2f}h",
        ))

    fig.update_layout(
        title="Funcion de Afluencia f(t)",
        xaxis_title="Hora del dia",
        yaxis_title="Personas en fila",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def graficar_derivada(t_input=None):
    t_vals = _rango_t()
    y_vals = [f_prima(t) for t in t_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_vals, y=y_vals, mode="lines",
        line=dict(color="darkviolet", width=2),
        name="f'(t) - Derivada",
    ))

    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.4)

    for t_p in encontrar_puntos_criticos():
        fig.add_trace(go.Scatter(
            x=[t_p], y=[0],
            mode="markers",
            marker=dict(size=12, color="purple", symbol="cross"),
            name=f"f'({t_p:.0f})=0",
        ))

    if t_input is not None:
        deriv = f_prima(t_input)
        fig.add_trace(go.Scatter(
            x=[t_input], y=[deriv],
            mode="markers+text",
            marker=dict(size=16, color="darkorange", symbol="x-thin", line=dict(width=2)),
            text=[f"f'({t_input:.2f})={deriv:.1f}"],
            textposition="top center",
            name=f"Tu hora: {t_input:.2f}h",
        ))

    fig.update_layout(
        title="Derivada f'(t) - Tasa de Cambio",
        xaxis_title="Hora del dia",
        yaxis_title="Tasa de cambio (personas/hora)",
        hovermode="x unified",
        template="plotly_white",
    )
    return fig
