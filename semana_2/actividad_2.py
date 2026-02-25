import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report


# 1. CARGA DE DATOS
# Asegúrate de que el archivo esté en la misma carpeta
df = pd.read_csv('Telco-Customer-Churn.csv')

# 2. LIMPIEZA
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

X = df.drop(['customerID', 'Churn'], axis=1)
y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

# 3. DEFINICIÓN DE COLUMNAS
columnas_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges']
columnas_categoricas = X.select_dtypes(include=['object', 'string']).columns.to_list()

# 4. PREPROCESAMIENTO
preprocessor = ColumnTransformer(
    transformers=[
        ('numeros', StandardScaler(), columnas_numericas),
        ('categorias', OneHotEncoder(drop='first'), columnas_categoricas)
        #('categorias', OneHotEncoder(drop='first', handle_unknown='ignore'), columnas_categoricas)
    ]
)

# 5. PIPELINE (CORREGIDO: random_state y solver para consistencia)
Pipeline_churn = Pipeline(steps=[
    ('Preprocesamiento', preprocessor),
    #('Clasificacion', LogisticRegression(random_state=42, solver='liblinear')
    ('Clasificacion', LogisticRegression())
])

# 6. ENTRENAMIENTO
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#Pipeline_churn.fit(X_train, y_train)

# 7. EVALUACIÓN
#prediccion = Pipeline_churn.predict(X_test)
print("------------- entrenando ------------------")
Pipeline_churn.fit(X_train, y_train)
print("------------- entrenamiento terminado ------------------")
#print(classification_report(y_test, prediccion))

# 8. CREACIÓN DE CLIENTES ESPECÍFICOS
# Usamos el primer registro como base (asegúrate que el CSV no haya cambiado el orden)
baseline = X_test.iloc[0].copy()

print("el cliente base es :\n")
print(baseline)

cliente_a =baseline.copy()
cliente_a['Contract'] = 'Month-to-month'
cliente_a['InternetService'] = 'Fiber optic'

cliente_b = baseline.copy()
cliente_b['Contract'] = 'Two year'
cliente_b['Internet Service'] = 'DSL'

df_comparacion = pd.DataFrame([cliente_a, cliente_b])

probabilidades = Pipeline_churn.predict_proba(df_comparacion)[:,1]

print("\n--- data frame de comparacion ---")

print(probabilidades)

prob_a = probabilidades[0] * 100
prob_b = probabilidades[1] * 100

nombres = ['Cliente A\n(Mes a Mes + Fibra)', 'Cliente B\n(2 Años + DSL)']

probabilidades = [prob_a, prob_b]
colres = ['#ff4d4d', '#74b9ff']

plt.figure(figsize=(10, 6))

barras = plt.bar(nombres, probabilidades, color=colres, alpha=0.8, width=0.6)

plt.title('comparacion de riesgo de fuga (churn)', fontsize=16, fontweight='bold')
plt.ylabel('probabilidad de irse (%)', fontsize=12)

plt.ylim(0, 30)

for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2., altura +1,
            f'{altura:.1f}%', ha='center', va='bottom', fontsize=14, fontweight='bold', color='black')

plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()
































'''clientes_especificos = pd.DataFrame([
    {
        **baseline.to_dict(),
        'InternetService': 'Fiber optic',
        'Contract': 'Month-to-month'
    },
    {
        **baseline.to_dict(),
        'InternetService': 'DSL',
        'Contract': 'Two year'
    }
])

# 9. PREDICCIÓN DE PROBABILIDAD (CORREGIDO: Multiplicado por 100)
# Obtenemos la probabilidad de la clase 1 (Churn) y la convertimos a porcentaje
prob_clientes = Pipeline_churn.predict_proba(clientes_especificos)[:, 1] * 100

clientes_especificos['Cliente_Etiqueta'] = [
    'Cliente A\n(Mes a Mes + Fibra)',
    'Cliente B\n(2 Años + DSL)'
]
clientes_especificos['Probabilidad (%)'] = prob_clientes

print("\n--- COMPARACIÓN DE CLIENTES ---")
print(clientes_especificos[['Cliente_Etiqueta', 'Contract', 'InternetService', 'Probabilidad (%)']])

# 10. GRÁFICA COMPARATIVA (Igual a tu imagen)
plt.figure(figsize=(12, 6))
colores = ['#ff7675', '#74b9ff'] # Colores similares a los de tu gráfica

barras = plt.bar(
    clientes_especificos['Cliente_Etiqueta'],
    clientes_especificos['Probabilidad (%)'],
    color=colores,
    alpha=0.9,
    width=0.6
)

# Línea de zona de riesgo
plt.axhline(y=50, color='gray', linestyle='--', linewidth=1.5, alpha=0.6)
plt.text(0.5, 52, 'ZONA DE RIESGO (>50%)', ha='center', color='dimgray', fontweight='bold')

# Etiquetas sobre las barras
for barra in barras:
    yval = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width()/2, 
        yval + 1, 
        f'{yval:.1f}%', 
        ha='center', 
        va='bottom', 
        fontsize=13, 
        fontweight='bold'
    )

plt.ylim(0, 100)
plt.title('Comparación de Riesgo de Fuga (Churn)', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Probabilidad de Irse (%)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()'''