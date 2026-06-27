# Fila Inteligente

Sistema de prediccion de congestion para el casino universitario de INACAP Puente Alto, desarrollado con Calculo Diferencial.

## Equipo

- Bryan Alegria
- Diego Aranguiz
- Romina Baeza
- Elisa Oyarzun
- Cristina Sepulveda

**Asignatura:** Calculo Diferencial
**Profesor:** Natalia Pinilla Morales
**Institucion:** INACAP Puente Alto

## Descripcion

Aplicacion web interactiva que modela la afluencia del casino universitario usando una funcion polinomico-exponencial con 3 puntos criticos (t=8, t=13, t=18). Permite predecir congestion y recomendar el mejor horario para ir al casino.

## Requisitos

- Windows 10 u 11
- Python 3.10 o superior
- Conexion a internet (solo para la instalacion)

## Instalacion

1. Verifica que tienes Python instalado:
   ```
   python --version
   ```

2. Clona o descarga el proyecto en tu computador.

3. Abre una terminal en la carpeta raiz del proyecto.

4. Instala las dependencias:
   ```
   pip install -r FilaInteligente/requirements.txt
   ```

## Ejecucion

Desde la carpeta raiz del proyecto ejecuta:

```
streamlit run FilaInteligente/app.py
```

La aplicacion abrira automaticamente en tu navegador en http://localhost:8501

Si no abre automaticamente, copia esa URL en tu navegador.

## Uso

- Desliza el control de hora para explorar la afluencia durante el dia
- Usa el boton "Iniciar Demo" para ver la animacion automatica de 8:00 a 22:00
- Revisa la seccion "Analisis matematico" para ver los puntos criticos, clasificacion con segunda derivada e interpretacion del modelo

## Estructura del proyecto

```
FilaInteligente/
├── app.py              # Interfaz web con Streamlit
├── modelo.py           # Funcion f(t), derivadas y prediccion
├── graficas.py         # Graficos interactivos con Plotly
├── requirements.txt    # Dependencias del proyecto
└── tests/
    └── test_modelo.py  # Tests unitarios
```

## Tests

Para ejecutar los tests:

```
pytest FilaInteligente/tests/
```
