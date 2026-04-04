# 🏠 Análisis de Airbnb Buenos Aires
### Desafío Profesional Data Analyst - Digital House

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Dash](https://img.shields.io/badge/Dash-Plotly-red) ![Pandas](https://img.shields.io/badge/Pandas-2.0-green)

## 📋 Descripción
Análisis completo del mercado de Airbnb en Buenos Aires para identificar oportunidades de inversión inmobiliaria. Se procesaron más de 23.000 propiedades y 387.000 reseñas aplicando técnicas de EDA, limpieza de datos y visualización interactiva.

## 🎯 Objetivo
Determinar en qué barrios de Buenos Aires conviene invertir en propiedades para alquilar por Airbnb, maximizando el retorno mediante análisis de precio, disponibilidad y demanda.

## 📁 Estructura del Proyecto
## 🔍 Etapas del Proyecto

### Etapa 1 - Análisis Exploratorio (EDA)
- Exploración de 23.729 propiedades y 106 variables
- Análisis de distribución de precios (ARS)
- Visualización de propiedades por barrio y tipo
- Análisis de evolución de reseñas 2010-2020

### Etapa 2 - Limpieza y Transformación (ETL)
- Eliminación de columnas irrelevantes y con >50% nulos
- Imputación de valores faltantes
- Detección y eliminación de outliers (método IQR)
- Consultas SQL con pandasql
- Dataset final: 21.647 filas × 85 columnas, 0 nulos

### Etapa 3 - Dashboard Interactivo
- Dashboard desarrollado con Plotly Dash
- Mapa geográfico de precios por barrio
- Análisis de precios, disponibilidad y demanda
- Score de inversión ponderado por barrio
- Filtros interactivos por tipo, barrio y precio

## 📊 Hallazgos Principales
- **Palermo y Recoleta** concentran la mayor cantidad de propiedades
- **Puerto Madero** lidera en precio promedio entre barrios relevantes
- **76%** del mercado son casas/departamentos completos
- Las reseñas crecieron exponencialmente entre 2015 y 2019
- **Top barrios para invertir:** Puerto Madero, Palermo, San Nicolás, Retiro, Monserrat

## 🚀 Cómo ejecutar el dashboard

### Requisitos
```bash
pip install dash plotly pandas statsmodels
```

### Ejecutar
```bash
python dashboard_airbnb.py
```
Abrir en el navegador: `http://127.0.0.1:8050`

## 🛠️ Tecnologías utilizadas
- **Python 3.13**
- **Pandas** - Manipulación de datos
- **Matplotlib / Seaborn** - Visualizaciones estáticas
- **Plotly / Dash** - Dashboard interactivo
- **pandasql** - Consultas SQL sobre DataFrames
- **NumPy** - Cálculos numéricos

## 📈 Dataset
Datos de Airbnb Buenos Aires (Inside Airbnb):
- `listings.csv` - 23.729 propiedades
- `calendar.csv` - 8.661.286 registros de disponibilidad
- `reviews.csv` - 387.099 reseñas

> Los datasets originales no están incluidos en el repositorio por su tamaño.

## 👩‍💻 Autora
**Camila** - Estudiante Data Analyst - Digital House 2024
