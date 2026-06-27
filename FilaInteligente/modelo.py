import math


def f(t):
    return 30 + 135 * math.exp(-((t - 13) ** 2) / 8)


def f_prima(t):
    return -33.75 * (t - 13) * math.exp(-((t - 13) ** 2) / 8)


def f_doble_prima(t):
    x = t - 13
    exp_term = math.exp(-(x ** 2) / 8)
    return -33.75 * exp_term * (1 - (x ** 2) / 4)


def encontrar_puntos_criticos():
    return [13.0]


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
    umbral_pico = 0.85 * valor_maximo

    es_hora_pico = afluencia >= umbral_pico
    derivada = f_prima(t_input)

    if derivada > 3.0:
        tendencia = "creciendo"
    elif derivada < -3.0:
        tendencia = "decreciendo"
    else:
        tendencia = "estable"

    ventana_min = max(8.0, t_input - 3.0)
    ventana_max = min(22.0, t_input + 3.0)

    mejor_t = ventana_min
    t = ventana_min
    while t <= ventana_max:
        if f(t) < f(mejor_t):
            mejor_t = t
        t += 0.25

    if abs(mejor_t - t_input) < 0.25:
        mensaje = "Ya estas en la mejor hora dentro de un rango de +-3h."
    elif es_hora_pico:
        mensaje = (
            f"Hora pico ({afluencia:.0f} pers.). "
            f"Se recomienda ir a las {mejor_t:.1f}h "
            f"({f(mejor_t):.0f} pers.)."
        )
    else:
        mensaje = (
            f"Afluencia moderada ({afluencia:.0f} pers.). "
            f"La mejor hora cercana es las {mejor_t:.1f}h."
        )

    return {
        "hora": t_input,
        "afluencia": round(afluencia, 1),
        "es_hora_pico": es_hora_pico,
        "tendencia": tendencia,
        "horario_recomendado": mejor_t,
        "mensaje": mensaje,
    }


def demo():
    assert abs(f(8) - 35.93) < 0.1
    assert abs(f(13) - 165) < 0.1
    assert abs(f(18) - 35.93) < 0.1
    assert abs(f_prima(13)) < 0.001
    print("demo(): todas las verificaciones pasaron.")


if __name__ == "__main__":
    demo()
