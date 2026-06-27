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
