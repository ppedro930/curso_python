# proyecto final TR NETWORK

Pipeline automatizado (es una automatizacion de como procesar todos los archivos pero sin ir ejecutando uno por uno) esto ejecuta el 90% mi proyecto y se usa para detectar zonas saturadas combinando datos de Airbnb y Profeco presentandolo a traves de graficas.

## 📌 Arquitectura

El pipeline está dividido en 4 fases:

1. ETL (Limpieza y transformación)
2. Machine Learning (Regresión + Clustering)
3. IA Generativa (Gemini API)
4. Persistencia en Base de Datos + Dashboard Power BI

## 🚀 Ejecución

Ejecutar el pipeline completo:

se ejecuta en git bash

```bash
python main.py