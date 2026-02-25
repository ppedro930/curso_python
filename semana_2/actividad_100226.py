import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

import seaborn as sns
import matplotlib.pyplot as plt

# =========================================================
# 1. CARGA Y LIMPIEZA DEL DATASET
# =========================================================
df = pd.read_csv('Telco-Customer-Churn.csv')

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

X = df.drop(['customerID', 'Churn'], axis=1)
y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

# =========================================================
# 2. DEFINICIÓN DE COLUMNAS
# =========================================================
columnas_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges']

columnas_categoricas = [
    'gender', 'Partner', 'Dependents',
    'PhoneService', 'MultipleLines',
    'InternetService', 'OnlineSecurity', 'OnlineBackup',
    'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies',
    'Contract', 'PaperlessBilling', 'PaymentMethod'
]

# =========================================================
# 3. PREPROCESAMIENTO
# =========================================================
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), columnas_numericas),
        ('cat', OneHotEncoder(drop='first'), columnas_categoricas)
    ]
)

# =========================================================
# 4. PIPELINE DE CHURN
# =========================================================
Pipeline_churn = Pipeline(steps=[
    ('Preprocesamiento', preprocessor),
    ('Clasificacion', LogisticRegression(max_iter=1000))
])

# =========================================================
# 5. ENTRENAMIENTO
# =========================================================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

Pipeline_churn.fit(X_train, y_train)

# =========================================================
# 6. EVALUACIÓN DEL MODELO
# =========================================================
prediccion = Pipeline_churn.predict(X_test)

print("------------- REPORTE DE CLASIFICACIÓN ------------------")
print(classification_report(y_test, prediccion))

# =========================================================
# 7. MATRIZ DE CONFUSIÓN
# =========================================================
matrix_confusion = confusion_matrix(y_test, prediccion)

plt.figure(figsize=(10, 6))
ax = sns.heatmap(
    matrix_confusion,
    annot=True,
    fmt='d',
    cmap='rocket',
    xticklabels=['Pred: se queda', 'Pred: se va'],
    yticklabels=['Real: se queda', 'Real: se va']
)

ax.set(
    xlabel='Predicción del modelo',
    ylabel='Valor real',
    title='Matriz de confusión - Regresión logística (Churn)'
)

plt.show()

# =========================================================
# 8. LISTA DE CLIENTES EN RIESGO
# =========================================================
prob_fuga = Pipeline_churn.predict_proba(X_test)[:, 1]

lista_marketing = pd.DataFrame({
    'Customer ID': df.loc[X_test.index, 'customerID'],
    'Probabilidad de fuga': prob_fuga,
    'Status real': y_test
})

lista_llamadas = lista_marketing[
    lista_marketing['Probabilidad de fuga'] > 0.3
].sort_values(by='Probabilidad de fuga', ascending=False)

print(f"\nClientes en riesgo de abandono: {len(lista_llamadas)}")
print(lista_llamadas.head(10))

# =========================================================
# 9. COMPARACIÓN DE CLIENTES ESPECÍFICOS (ENTREGABLE)
# =========================================================
clientes_especificos = pd.DataFrame([
    # -------- CLIENTE A --------
    {
        'gender': 'Male',
        'Partner': 'No',
        'Dependents': 'No',
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'Fiber optic',
        'OnlineSecurity': 'No',
        'OnlineBackup': 'No',
        'DeviceProtection': 'No',
        'TechSupport': 'No',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'Yes',
        'PaymentMethod': 'Electronic check',
        'tenure': 5,
        'MonthlyCharges': 85,
        'TotalCharges': 400
    },
    # -------- CLIENTE B --------
    {
        'gender': 'Male',
        'Partner': 'Yes',
        'Dependents': 'Yes',
        'PhoneService': 'Yes',
        'MultipleLines': 'Yes',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Two year',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Bank transfer (automatic)',
        'tenure': 48,
        'MonthlyCharges': 55,
        'TotalCharges': 2600
    }
])

# Probabilidades de abandono
prob_clientes = Pipeline_churn.predict_proba(clientes_especificos)[:, 1]

clientes_especificos['Probabilidad de fuga (%)'] = prob_clientes * 100

print("\n--- COMPARACIÓN DE CLIENTES ---")
print(clientes_especificos[['Contract', 'InternetService', 'Probabilidad de fuga (%)']])
