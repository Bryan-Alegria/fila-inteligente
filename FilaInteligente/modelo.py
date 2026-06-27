import math


K = 1.5369
SIGMA_SQ = 12.25


def f_prima(t):
    return K * (t - 8) * (t - 13) * (t - 18) * math.exp(-((t - 13) ** 2) / SIGMA_SQ)


def f_doble_prima(t):
    g = (t - 8) * (t - 13) * (t - 18)
    g_prima = (t - 13) * (t - 18) + (t - 8) * (t - 18) + (t - 8) * (t - 13)
    exp_term = math.exp(-((t - 13) ** 2) / SIGMA_SQ)
    return K * exp_term * (g_prima - 2 * g * (t - 13) / SIGMA_SQ)


def f(t):
    if abs(t - 13) < 0.001:
        return 165.0
    paso = 0.005
    desde = 13.0
    hasta = t
    n = max(10, int(abs(hasta - desde) / paso))
    dt = (hasta - desde) / n
    integral = 0.0
    for i in range(n):
        u1 = desde + i * dt
        u2 = u1 + dt
        integral += (f_prima(u1) + f_prima(u2)) * dt / 2
    return 165.0 + integral


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
    es_hora_pico = afluencia > 100
    derivada = f_prima(t_input)

    if derivada > 3.0:
        tendencia = "creciendo"
    elif derivada < -3.0:
        tendencia = "decreciendo"
    else:
        tendencia = "estable"

    horario_recomendado = None
    mensaje = ""

    ventana_min = max(8.0, t_input + 1.0)
    ventana_max = min(22.0, t_input + 3.0)

    if ventana_min <= ventana_max:
        mejor_t = ventana_min
        mejor_f = f(ventana_min)
        t = ventana_min + 0.25
        while t <= ventana_max:
            valor = f(t)
            if valor < mejor_f:
                mejor_f = valor
                mejor_t = t
            t += 0.25

        if mejor_f < afluencia and mejor_f < 80:
            horario_recomendado = mejor_t
            if es_hora_pico:
                mensaje = (
                    f"Hora pico ({afluencia:.0f} pers.). "
                    f"Se recomienda ir a las {mejor_t:.1f}h "
                    f"({mejor_f:.0f} pers.)."
                )
            else:
                mensaje = (
                    f"Se recomienda ir a las {mejor_t:.1f}h "
                    f"({mejor_f:.0f} pers. estimadas)."
                )

    if horario_recomendado is None:
        if es_hora_pico:
            mensaje = (
                f"Hora pico ({afluencia:.0f} pers.). "
                "No hay una hora cercana mejor disponible hoy."
            )
        else:
            mensaje = (
                f"No estas en hora pico ({afluencia:.0f} pers.). "
                "Buen momento para ir al casino."
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
    assert abs(f(8) - 30.0) < 0.5
    assert abs(f(13) - 165.0) < 0.5
    assert abs(f(18) - 30.0) < 0.5
    assert f(22) <= 80.0
    for t in [8, 13, 18]:
        assert abs(f_prima(t)) < 0.1
    print("demo(): todas las verificaciones pasaron.")


if __name__ == "__main__":
    demo()
