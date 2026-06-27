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
    assert abs(f(8) - 26.0) < 0.01
    assert abs(f(15) - 75.0) < 0.01
    assert abs(f(22) - 26.0) < 0.01


def test_f_prima_se_anula_en_puntos_criticos():
    for t in [8.0, 15.0, 22.0]:
        assert abs(f_prima(t)) < 0.001, f"f'({t}) deberia ser 0, fue {f_prima(t)}"


def test_clasificacion_puntos_criticos():
    clasif = clasificar_puntos_criticos()
    assert clasif[8.0] == "minimo local"
    assert clasif[15.0] == "maximo local"
    assert clasif[22.0] == "minimo local"


def test_predecir_hora_pico():
    r = predecir(15.0)
    assert r["es_hora_pico"] is True
    assert "pico" in r["mensaje"].lower()


def test_predecir_hora_valle():
    r = predecir(8.0)
    assert r["es_hora_pico"] is False
    assert r["horario_recomendado"] == 8.0


def test_predecir_tendencia():
    r_crece = predecir(10.0)
    assert r_crece["tendencia"] == "creciendo"
    r_decrece = predecir(17.0)
    assert r_decrece["tendencia"] == "decreciendo"


def test_recomendacion_minimo_mas_cercano():
    r = predecir(10.0)
    assert r["horario_recomendado"] == 8.0
    r = predecir(16.0)
    assert r["horario_recomendado"] == 22.0


def test_en_punto_critico_reconoce_valle():
    r = predecir(8.0)
    assert "valle" in r["mensaje"].lower()
