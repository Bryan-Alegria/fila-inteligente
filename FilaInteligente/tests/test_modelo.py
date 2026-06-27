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
    assert abs(f(8) - 35.93) < 0.5
    assert abs(f(13) - 165) < 0.5
    assert abs(f(18) - 35.93) < 0.5


def test_f_prima_se_anula_en_puntos_criticos():
    for t in encontrar_puntos_criticos():
        assert abs(f_prima(t)) < 0.01, f"f'({t}) deberia ser 0, fue {f_prima(t)}"


def test_clasificacion_puntos_criticos():
    clasif = clasificar_puntos_criticos()
    assert clasif[13.0] == "maximo local"


def test_predecir_hora_pico():
    r = predecir(13.0)
    assert r["es_hora_pico"] is True
    assert "pico" in r["mensaje"].lower()


def test_predecir_tendencia():
    r_crece = predecir(10.0)
    assert r_crece["tendencia"] == "creciendo"
    r_decrece = predecir(16.0)
    assert r_decrece["tendencia"] == "decreciendo"


def test_predecir_hora_valle_reconoce_propia():
    r = predecir(8.0)
    assert not r["es_hora_pico"]
    assert "mejor hora" in r["mensaje"].lower()


def test_recomendacion_dentro_ventana():
    r = predecir(13.0)
    assert 10.0 <= r["horario_recomendado"] <= 16.0
    assert r["horario_recomendado"] != 13.0


def test_funcion_dentro_de_rango():
    for t in [v / 4.0 for v in range(32, 89)]:
        valor = f(t)
        assert 0 <= valor <= 192, f"f({t})={valor} fuera de [0,192]"
