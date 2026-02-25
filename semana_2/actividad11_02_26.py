# ==================================================
#  MODELO RANDOM FOREST - TELCO CHURN OPTIMIZADO
# ==================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #libreria con modulo
#import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV # la libreria es Scikit-Learn con el modulo .model_selection
# train_test_split y GridSearchCV son los parametros utilizados
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report


# 1. CARGA DE DATOS

df = pd.read_csv('Telco-Customer-Churn.csv')


# 2. LIMPIEZA

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce') # Convertir a dato numérico para hacer los calculos, 
#forzando errores a NaN
df = df.dropna() # Eliminar filas con valores faltantes (NaN) para evitar problemas en el modelo

X = df.drop(['customerID', 'Churn'], axis=1) # customerID y churn es un identificador único que no
# aporta información para la predicción, por lo que se elimina y axis=1 le está diciendo a Python en qué dirección trabajar (horizontalmente)
y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0) # se selecciona la columna y luego 
#apply() aplica una función a cada valor de la columna en este caso un booleano pero tipo binario


# 3. COLUMNAS NUMÉRICAS Y CATEGÓRICAS

columnas_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges'] #ya estando cpnvertidas a dato numerico se seleccionan 
# las columnas que se consideran numéricas para el modelo
columnas_cat = X.select_dtypes(include=['object', 'str']).columns.tolist() # al especificar las columnas numericas se asume 
# que las demas son formato string y se seleccionan para el preprocesamiento de variables categoricas


# 4. PREPROCESAMIENTO

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), columnas_numericas),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), columnas_cat)
    ]
)
# Prepara automáticamente los datos numéricos y categóricos para que el modelo pueda entrenarse correctamente.


# 5. PIPELINE RANDOM FOREST

pipeline_rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        random_state=42,
        class_weight='balanced' # esto es para darle mas importancia a datos mas pequeños
    ))
])
# aca se indican el orden de pasos a seguir, primero se preprocesan los datos y luego se entrena el modelo de Random Forest.

# 6. TRAIN - TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

#Divide el dataset en entrenamiento (80%) y prueba (20%) 
# #para evaluar el rendimiento del modelo en datos que no ha visto antes.

#X_train → datos para entrenar
'''
X_test → datos para probar

y_train → respuestas correctas del entrenamiento

y_test → respuestas correctas de prueba
'''


# 7. GRID SEARCH (OPTIMIZACIÓN)

param_grid = {
    'classifier__n_estimators': [200, 500],
    'classifier__max_depth': [10, 20],
    'classifier__min_samples_split': [2, 10]
}
'''
classifier = nombre del modelo dentro del pipeline
 __ = separador
 después va el parámetro del modelo
Es una lista de hiperparámetros que se prueban automáticamente para optimizar 
el modelo usando búsqueda en cuadrícula (Grid Search).'''

grid_search = GridSearchCV(
    pipeline_rf,
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1
)

'''pipeline_rf → tu modelo completo (preprocesamiento + Random Forest).

param_grid → los valores que quieres probar.

cv=5 → usa validación cruzada de 5 partes.

scoring='f1' → evalúa usando la métrica F1 (buena para clasificación desbalanceada).

n_jobs=-1 → usa todos los núcleos del CPU (más rápido).'''

print("\nBuscando mejores parámetros...\n")
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

'''Entrena el modelo

Prueba todas las combinaciones del param_grid

Usa validación cruzada (cv=5)

Calcula el F1 de cada combinación

Decide cuál es la mejor

👉 Aquí es donde realmente aprende patrones múltiples veces.'''

print("Mejores parámetros encontrados:")
print(grid_search.best_params_)

'''Muestra en pantalla los mejores hiperparámetros encontrados después de hacer GridSearchCV.'''



# 8. AJUSTE DE UMBRAL (OPTIMIZAR RECALL)

y_probs = best_model.predict_proba(X_test)[:, 1]

'''predict_proba() devuelve probabilidades de cada clase, y [:,1] extrae la probabilidad de la clase positiva para cada observación.'''

# UMBRAL QUE GENERA LA MATRIZ ÓPTIMA
umbral_optimizado = 0.33
y_pred_custom = (y_probs >= umbral_optimizado).astype(int)

'''Se convierte la probabilidad en clase binaria usando un umbral personalizado,
 permitiendo ajustar el equilibrio entre precisión y recall según el problema.'''

# 9. MATRIZ DE CONFUSIÓN

cm = confusion_matrix(y_test, y_pred_custom)
verdaderos_negativos, falso_positivo, falso_negativo, verdaderos_positivos = cm.ravel()

'''Se genera la matriz de confusión para evaluar el desempeño del modelo y se extraen
 TN, falso_positivo, FN y TP para calcular métricas de clasificación.'''

# 10. CÁLCULO DE IMPACTO ECONÓMICO

costo_fugas = falso_negativo * 1000      # Cliente perdido
costo_promos = falso_positivo * 50      # Promo innecesaria
costo_total = costo_fugas + costo_promos


'''Se calculan los costos asociados a los errores del modelo (FN y falso_positivo) para medir su impacto 
financiero y tomar decisiones basadas en rentabilidad.'''

# 11. VISUALIZACIÓN

labels = ['Se Queda', 'Se Va']
fig, ax = plt.subplots(figsize=(10, 8))

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp.plot(cmap='Blues', ax=ax, values_format='d')

plt.title(
    f"Matriz Final (Optimizado para Recall)\nCosto Total: ${costo_total:,}",
    fontsize=14
)
plt.xlabel("Predicted label")
plt.ylabel("True label")

plt.show()


# 12. REPORTE FINAL

print("\n==================================================")
print("💰  REPORTE FINANCIERO FINAL  💰")
print("==================================================\n")

print("------------- REPORTE DE CLASIFICACIÓN -------------\n")
print(classification_report(y_test, y_pred_custom))

print("\n---------------- IMPACTO ECONÓMICO ----------------\n")
print(f"Falsos Negativos (FN): {falso_negativo} -> Costo: ${costo_fugas:,.2f}")
print(f"Falsos Positivos (falso_positivo): {falso_positivo} -> Costo: ${costo_promos:,.2f}")

print(f"\n💸 COSTO TOTAL DEL MODELO: ${costo_total:,.2f}")
print("==================================================")
