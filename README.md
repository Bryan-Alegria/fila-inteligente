# Fila Inteligente

Sistema de predicción de congestión para el casino universitario de INACAP Puente Alto, desarrollado con Cálculo Diferencial.

## Equipo

- Bryan Alegría
- Diego Aránguiz
- Romina Baeza
- Elisa Oyarzun
- Cristina Sepúlveda

**Asignatura:** Cálculo Diferencial
**Profesor:** Natalia Pinilla Morales
**Institución:** INACAP Puente Alto

## Descripción

Aplicación web interactiva que modela la afluencia del casino universitario usando una función polinómico-exponencial con 3 puntos críticos (t=8, t=13, t=18). Permite predecir congestión y recomendar el mejor horario para ir al casino.

## Requisitos

- Windows 10 u 11
- Python 3.10 o superior
- Conexión a internet (solo para la instalación)

## Instalación

1. Verifica que tienes Python instalado:
   ```
   python --version
   ```

2. Clona o descarga el proyecto en tu computador.

3. Abre una terminal en la carpeta raíz del proyecto.

4. Instala las dependencias:
   ```
   pip install -r FilaInteligente/requirements.txt
   ```

## Ejecución

Desde la carpeta raíz del proyecto ejecuta:

```
streamlit run FilaInteligente/app.py
```

La aplicación abrirá automáticamente en tu navegador en http://localhost:8501

Si no abre automáticamente, copia esa URL en tu navegador.

## Uso

- Desliza el control de hora para explorar la afluencia durante el día
- Usa el botón "Iniciar Demo" para ver la animación automática de 8:00 a 22:00
- Revisa la sección "Análisis matemático" para ver los puntos críticos, clasificación con segunda derivada e interpretación del modelo

## Estructura del proyecto

```
FilaInteligente/
├── app.py              # Interfaz web con Streamlit
├── modelo.py           # Función f(t), derivadas y predicción
├── graficas.py         # Gráficos interactivos con Plotly
├── requirements.txt    # Dependencias del proyecto
└── tests/
    └── test_modelo.py  # Tests unitarios
```

## Tests

Para ejecutar los tests:

```
pytest FilaInteligente/tests/
```
