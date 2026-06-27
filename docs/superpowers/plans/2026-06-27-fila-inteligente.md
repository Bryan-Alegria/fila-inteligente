# Fila Inteligente — Plan de Implementacion

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir una app Streamlit que modele la afluencia al casino universitario con calculo diferencial, prediga si una hora es pico o valle, y recomiende el horario de menor congestion mas cercano.

**Architecture:** Tres archivos planos: `modelo.py` (matematica pura, funciones puras y testables), `graficas.py` (Plotly charts), `app.py` (Streamlit UI). La app orquesta el modelo y las graficas, cablea entrada de usuario a prediccion, y renderiza todo en un dashboard de una sola pagina.

**Tech Stack:** Python 3.12+, Streamlit, Plotly, pytest

## Global Constraints

- Sin frameworks adicionales fuera de Streamlit + Plotly
- Todo el calculo matematico resuelto analiticamente (sin sympy ni librerias numericas)
- Codigo y UI en espanol (alineado con el contexto del proyecto ABPro)
- Ejecutable con `streamlit run app.py`
- Prototipo funcional apto para presentacion en video de 10-15 min (Etapa 3)

---

### Task 1: Modelo Matematico

**Files:**
- Create: `FilaInteligente/modelo.py`
- Create: `FilaInteligente/tests/test_modelo.py`

**Interfaces:**
- Produces: `f(t)`, `f_prima(t)`, `f_doble_prima(t)`, `encontrar_puntos_criticos()`, `clasificar_puntos_criticos()`, `predecir(t_input)`

#### Funcion elegida

Funcion cuartica simetrica alrededor de t=13:00 (hora pico del almuerzo):

```
f(t) = 0.05*(t - 13)^4 - 2.5*(t - 13)^2 + 60
```

- **Dominio:** t in [6, 20] (6:00 a 20:00)
- **Rango:** [28.75, 60] personas
- **Minimos locales:** t = 8:00 (28.75 pers.), t = 18:00 (28.75 pers.)
- **Maximo local:** t = 13:00 (60 pers.)

Derivadas analiticas:
```
f'(t)  = 0.20*(t - 13)^3 - 5*(t - 13)  = (t-13)(0.20*(t-13)^2 - 5)
f''(t) = 0.60*(t - 13)^2 - 5
```

Puntos criticos (f'(t) = 0): t = 8, t = 13, t = 18
Clasificacion por f''(t): f''(8)=10>0 (minimo), f''(13)=-5<0 (maximo), f''(18)=10>0 (minimo)

**Justificacion de la eleccion:** Una cuartica con 3 puntos criticos (dos minimos, un maximo) permite demostrar todo el contenido exigido: derivada primera, puntos criticos, segunda derivada, clasificacion de maximos/minimos, y tiene una interpretacion realista (valle en apertura/cierre, pico en almuerzo).

- [ ] **Step 1: Crear estructura de directorios**

```bash
New-Item -ItemType Directory -Path "FilaInteligente\tests" -Force
```

- [ ] **Step 2: Escribir el archivo de pruebas (`test_modelo.py`)**

```python
# FilaInteligente/tests/test_modelo.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from modelo import (
    f, f_prima, f_doble_prima,
    encontrar_puntos_criticos,
    clasificar_puntos_criticos,
    predecir,
)


def test_f_en_puntos_clave():
    assert abs(f(8) - 28.75) < 0.01
    assert abs(f(13) - 60) < 0.01
    assert abs(f(18) - 28.75) < 0.01


def test_f_prima_se_anula_en_puntos_criticos():
    for t in [8.0, 13.0, 18.0]:
        assert abs(f_prima(t)) < 0.001, f"f'({t}) deberia ser 0, fue {f_prima(t)}"


def test_clasificacion_puntos_criticos():
    clasif = clasificar_puntos_criticos()
    assert clasif[8.0] == "minimo local"
    assert clasif[13.0] == "maximo local"
    assert clasif[18.0] == "minimo local"


def test_predecir_hora_pico():
    r = predecir(13.0)
    assert r["es_hora_pico"] is True
    assert "pico" in r["mensaje"].lower()


def test_predecir_hora_valle():
    r = predecir(8.0)
    assert r["es_hora_pico"] is False
    assert r["horario_recomendado"] == 8.0


def test_predecir_tendencia():
    r_crece = predecir(10.0)
    assert r_crece["tendencia"] == "creciendo"
    r_decrece = predecir(14.0)
    assert r_decrece["tendencia"] == "decreciendo"


def test_recomendacion_minimo_mas_cercano():
    r = predecir(10.0)
    assert r["horario_recomendado"] == 8.0
    r = predecir(16.0)
    assert r["horario_recomendado"] == 18.0


def test_en_punto_critico_reconoce_valle():
    r = predecir(8.0)
    assert "valle" in r["mensaje"].lower()
```

- [ ] **Step 3: Ejecutar tests y verificar que fallen**

```bash
python -m pytest FilaInteligente/tests/test_modelo.py -v
```
Esperado: 8 tests FAIL con `ModuleNotFoundError: No module named 'modelo'`.

- [ ] **Step 4: Implementar `modelo.py`**

```python
# FilaInteligente/modelo.py

def f(t):
    a = 0.05
    b = 2.5
    c = 60
    p = 13
    return a * (t - p)**4 - b * (t - p)**2 + c


def f_prima(t):
    return 0.20 * (t - 13)**3 - 5 * (t - 13)


def f_doble_prima(t):
    return 0.60 * (t - 13)**2 - 5


def encontrar_puntos_criticos():
    return [8.0, 13.0, 18.0]


def clasificar_puntos_criticos():
    puntos = encontrar_puntos_criticos()
    resultado = {}
    for t in puntos:
        seg = f_doble_prima(t)
        if seg > 0:
            resultado[t] = "minimo local"
        elif seg < 0:
            resultado[t] = "maximo local"
        else:
            resultado[t] = "punto de inflexion"
    return resultado


def predecir(t_input):
    afluencia = f(t_input)
    valor_maximo = f(13)
    umbral_pico = 0.90 * valor_maximo
    es_hora_pico = afluencia >= umbral_pico
    derivada = f_prima(t_input)

    if derivada > 1.0:
        tendencia = "creciendo"
    elif derivada < -1.0:
        tendencia = "decreciendo"
    else:
        tendencia = "estable"

    clasif = clasificar_puntos_criticos()
    minimos = [t for t, tipo in clasif.items() if tipo == "minimo local"]

    horario_recomendado = min(minimos, key=lambda m: abs(t_input - m))

    if abs(t_input - horario_recomendado) < 0.25:
        mensaje = "Ya estas en una hora valle -- es un buen momento para ir al casino."
    elif es_hora_pico:
        mensaje = (
            f"Hora pico. Se recomienda ir a las {horario_recomendado:.0f}:00 "
            f"({abs(horario_recomendado - t_input):.0f}h de diferencia)."
        )
    else:
        mensaje = (
            f"Afluencia moderada. La hora mas tranquila cercana "
            f"es las {horario_recomendado:.0f}:00."
        )

    return {
        "hora": t_input,
        "afluencia": round(afluencia, 1),
        "es_hora_pico": es_hora_pico,
        "tendencia": tendencia,
        "horario_recomendado": horario_recomendado,
        "mensaje": mensaje,
    }


def demo():
    assert abs(f(8) - 28.75) < 0.01
    assert abs(f(13) - 60) < 0.01
    assert abs(f(18) - 28.75) < 0.01
    for t in [8, 13, 18]:
        assert abs(f_prima(t)) < 0.001
    print("demo(): todas las verificaciones pasaron.")


if __name__ == "__main__":
    demo()
```

- [ ] **Step 5: Ejecutar tests y verificar que pasen**

```bash
python -m pytest FilaInteligente/tests/test_modelo.py -v
```
Esperado: 8 tests PASS.

- [ ] **Step 6: Ejecutar demo() de auto-verificacion**

```bash
python FilaInteligente/modelo.py
```
Esperado: `demo(): todas las verificaciones pasaron.`

---

### Task 2: Visualizacion

**Files:**
- Create: `FilaInteligente/graficas.py`

**Interfaces:**
- Consumes: `f(t)`, `f_prima(t)`, `encontrar_puntos_criticos()`, `clasificar_puntos_criticos()` from `modelo`
- Produces: `graficar_afluencia(t_input=None)`, `graficar_derivada(t_input=None)`

- [ ] **Step 1: Implementar `graficas.py`**

```python
# FilaInteligente/graficas.py
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
```

- [ ] **Step 2: Verificar que las graficas se generan sin errores**

```bash
python -c "from graficas import graficar_afluencia, graficar_derivada; fig1 = graficar_afluencia(13); fig2 = graficar_derivada(13); print('OK: ambas graficas generadas')"
```
Esperado: `OK: ambas graficas generadas`.

---

### Task 3: Aplicacion Streamlit

**Files:**
- Create: `FilaInteligente/app.py`

**Interfaces:**
- Consumes: `f`, `f_prima`, `predecir` from `modelo`; `graficar_afluencia`, `graficar_derivada` from `graficas`
- Produces: app ejecutable con `streamlit run app.py`

- [ ] **Step 1: Implementar `app.py`**

```python
# FilaInteligente/app.py
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
```

- [ ] **Step 2: Lanzar la app y verificar que carga**

```bash
streamlit run FilaInteligente/app.py --server.headless true 2>&1 &
```
Nota: detener con Ctrl+C despues de verificar que carga en el navegador.

- [ ] **Step 3: Probar flujo completo manualmente**
  - Mover slider a 13:00 -> debe mostrar "Hora pico", mensaje de alerta
  - Mover slider a 8:00 -> debe mostrar "Hora valle", mensaje de confirmacion
  - Mover slider a 10:00 -> debe recomendar 8:00, tendencia "creciendo"
  - Mover slider a 15:00 -> debe recomendar 18:00, tendencia "decreciendo"

---

### Task 4: Requirements y verificacion final

**Files:**
- Create: `FilaInteligente/requirements.txt`

- [ ] **Step 1: Crear `requirements.txt`**

```
# FilaInteligente/requirements.txt
streamlit>=1.28
plotly>=5.18
numpy>=1.24
pytest>=7.4
```

- [ ] **Step 2: Instalar dependencias**

```bash
pip install -r FilaInteligente/requirements.txt
```

- [ ] **Step 3: Ejecutar toda la suite de tests final**

```bash
python -m pytest FilaInteligente/tests/test_modelo.py -v
```
Esperado: 8 passed.

- [ ] **Step 4: Verificar demo auto-contenida del modelo**

```bash
python FilaInteligente/modelo.py
```
Esperado: `demo(): todas las verificaciones pasaron.`

- [ ] **Step 5: Verificar que las graficas se generan**

```bash
python -c "from graficas import graficar_afluencia, graficar_derivada; fig1 = graficar_afluencia(13); fig2 = graficar_derivada(13); assert fig1 is not None; assert fig2 is not None; print('OK')"
```

---

## Resumen de archivos creados

```
FilaInteligente/
├── app.py                # Streamlit UI (orquestador)
├── modelo.py             # Funciones matematicas + demo() self-check
├── graficas.py           # Plotly charts
├── requirements.txt      # Dependencias
└── tests/
    └── test_modelo.py    # 8 tests unitarios
```
