# Integrantes - Actividad Integradora 2

## Equipo

| Integrante | Rol | Ramas principales |
|---|---|---|
| Sergio Esteban León García | Administrador del repositorio | `main` |
| Jose Isaias Diaz Dumett | Modelo, entrenamiento y API | `feature/model-training`, `feature/fastapi-service` |
| Luis Jimenez | Ingesta de datos con yfinance | `feature/data-ingestion` |

## Responsabilidades por integrante

### Sergio Esteban León García
- Creación y administración del repositorio en GitHub.
- Revisión y aprobación de Pull Requests.
- Validación de que la documentación coincida con el código entregado.
- Integración final de ramas hacia `main`.

### Jose Isaias Diaz Dumett
- Entrenamiento y serialización del modelo predictivo.
- Generación de artefactos en `artifacts/`.
- Implementación de la API FastAPI y contratos Pydantic.
- Configuración de pruebas automatizadas, `Dockerfile` y `compose.yaml`.

### Luis Jimenez
- Descarga de datos históricos con `yfinance`.
- Construcción del dataset local en `data/raw/` y `data/processed/`.
- Documentación del flujo de ingesta para reproducibilidad offline.

## Nota académica

Este proyecto es una herramienta educativa de análisis de señales financieras.
No constituye asesoría financiera ni recomendación de inversión.
