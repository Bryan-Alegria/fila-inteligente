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
    assert abs(f(8) - 30.0) < 0.5
    assert abs(f(13) - 165.0) < 0.5
    assert abs(f(18) - 30.0) < 0.5


def test_f_prima_se_anula_en_puntos_criticos():
    for t in encontrar_puntos_criticos():
        assert abs(f_prima(t)) < 0.01, f"f'({t}) deberia ser 0, fue {f_prima(t)}"


def test_clasificacion_puntos_criticos():
    clasif = clasificar_puntos_criticos()
    assert clasif[8.0] == "minimo local"
    assert clasif[13.0] == "maximo local"
    assert clasif[18.0] == "minimo local"


def test_predecir_hora_pico():
    r = predecir(13.0)
    assert r["es_hora_pico"] is True
    assert r["afluencia"] > 100
    assert "pico" in r["mensaje"].lower()


def test_predecir_hora_pico_recomienda():
    r = predecir(13.0)
    assert r["horario_recomendado"] is not None
    assert abs(r["horario_recomendado"] - 13.0) <= 2.0


def test_predecir_no_pico():
    r = predecir(9.0)
    assert not r["es_hora_pico"]
    assert "no estas en hora pico" in r["mensaje"].lower()


def test_predecir_tendencia():
    r_crece = predecir(10.0)
    assert r_crece["tendencia"] == "creciendo"
    r_decrece = predecir(16.0)
    assert r_decrece["tendencia"] == "decreciendo"


def test_recomendacion_no_excede_4h():
    for hora in [11.0, 13.0, 14.5]:
        r = predecir(hora)
        if r["horario_recomendado"] is not None:
            assert abs(r["horario_recomendado"] - hora) <= 4.0
