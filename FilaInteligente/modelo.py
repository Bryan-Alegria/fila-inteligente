def f(t):
    a = 0.216
    b = 10.8
    c = 165
    p = 13
    return a * (t - p)**4 - b * (t - p)**2 + c


def f_prima(t):
    return 0.864 * (t - 13)**3 - 21.6 * (t - 13)


def f_doble_prima(t):
    return 2.592 * (t - 13)**2 - 21.6


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

    if es_hora_pico:
        ventana_min = max(8.0, t_input - 2.0)
        ventana_max = min(22.0, t_input + 2.0)

        mejor_t = ventana_min
        t = ventana_min
        while t <= ventana_max:
            if f(t) < f(mejor_t):
                mejor_t = t
            t += 0.25

        mejor_f = f(mejor_t)
        if mejor_f <= 0.8 * afluencia:
            diferencia = abs(mejor_t - t_input)
            if diferencia <= 4.0:
                horario_recomendado = mejor_t
                mensaje = (
                    f"Hora pico ({afluencia:.0f} pers.). "
                    f"Se recomienda ir a las {mejor_t:.1f}h "
                    f"({mejor_f:.0f} pers.)."
                )
            else:
                mensaje = (
                    "No hay una hora cercana mejor, considera ir "
                    "antes de las 12:00 o despues de las 15:00."
                )
        else:
            mensaje = (
                "No hay una hora cercana mejor, considera ir "
                "antes de las 12:00 o despues de las 15:00."
            )
    else:
        horario_recomendado = t_input
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
    for t in [8, 13, 18]:
        assert abs(f_prima(t)) < 0.01
    print("demo(): todas las verificaciones pasaron.")


if __name__ == "__main__":
    demo()
