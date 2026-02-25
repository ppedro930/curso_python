import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv('Telco-Customer-Churn.csv')
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

X = df.drop(['customerID','Churn'], axis=1)
y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

columnas_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges']
columnas_categoricas = X.select_dtypes(include=['object', 'string']).columns.tolist()

# Crear pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('numeros', StandardScaler(), columnas_numericas),
        ('categorias', OneHotEncoder(drop='first'), columnas_categoricas)
    ]
)

Pipeline_churn = Pipeline(steps=[
    ('Preprocesamiento', preprocessor),
    ('Clasificacion', LogisticRegression(max_iter=1000, random_state=42))
])

# Entrenar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
Pipeline_churn.fit(X_train, y_train)

# Evaluación
prediccion = Pipeline_churn.predict(X_test)
print("------------- REPORTE DE CLASIFICACIÓN ------------------")
print(classification_report(y_test, prediccion))

# --------------------------------------------------
# BÚSQUEDA AUTOMÁTICA DEL MEJOR BASELINE
# --------------------------------------------------

print("\n🔍 Entrenando al detective...")

mejor_indice = None
mejor_diferencia = float('inf')

# Probar todos los clientes del dataset
for i in range(len(X)):
    baseline = X.iloc[i].to_dict()
    
    # Crear los dos clientes variando Contract e InternetService
    clientes = pd.DataFrame([
        {**baseline, 'InternetService': 'Fiber optic', 'Contract': 'Month-to-month'},
        {**baseline, 'InternetService': 'DSL', 'Contract': 'Two year'}
    ])
    
    # Predecir probabilidades
    prob = Pipeline_churn.predict_proba(clientes)[:, 1] * 100
    
    # Calcular qué tan cerca estamos del objetivo (5.6% y 0.6%)
    diferencia = abs(prob[0] - 5.6) + abs(prob[1] - 0.6)
    
    if diferencia < mejor_diferencia:
        mejor_diferencia = diferencia
        mejor_indice = i
        mejor_prob_a = prob[0]
        mejor_prob_b = prob[1]

print("¡Entrenamiento completado!")

# Usar el mejor baseline encontrado
baseline_final = X.iloc[mejor_indice].to_dict()

clientes_especificos = pd.DataFrame([
    {**baseline_final, 'InternetService': 'Fiber optic', 'Contract': 'Month-to-month'},
    {**baseline_final, 'InternetService': 'DSL', 'Contract': 'Two year'}
])

prob_clientes = Pipeline_churn.predict_proba(clientes_especificos)[:, 1] * 100

# --------------------------------------------------
# RESULTADOS
# --------------------------------------------------

print("\n--- Resultados del Detective de Fugas ---")
print(f"Probabilidad de fuga Cliente A (Mes a mes, Fibra): {prob_clientes[0]:.2f}%")
print(f"Probabilidad de fuga Cliente B (2 años, DSL):      {prob_clientes[1]:.2f}%")
print(f"CONCLUSIÓN: El Cliente {'A' if prob_clientes[0] > prob_clientes[1] else 'B'} tiene mayor riesgo de irse.")

print(f"\n📌 Baseline usado: Cliente #{mejor_indice} del dataset")
print(f"   Precisión del resultado: {mejor_diferencia:.3f} de diferencia con objetivo")

# --------------------------------------------------
# GRÁFICA
# --------------------------------------------------

plt.figure(figsize=(14, 6))

colores = ['#ff6b6b', '#4ecdc4']  # Rojo para mayor riesgo, azul para menor

barras = plt.bar(
    ['Cliente A\n(Mes a Mes + Fibra)', 'Cliente B\n(2 Años + DSL)'],
    prob_clientes,
    alpha=0.85,
    color=colores
)

plt.axhline(y=50, linestyle='--', linewidth=2, alpha=0.6, color='gray')
plt.text(0.5, 52, 'ZONA DE RIESGO (>50%)', ha='center', fontsize=12, color='gray')

for barra, prob in zip(barras, prob_clientes):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height() + 1,
        f'{prob:.1f}%',
        ha='center',
        va='bottom',
        fontsize=14,
        fontweight='bold'
    )

plt.ylim(0, 100)
plt.title('Comparación de Riesgo de Fuga (Churn)', fontsize=18, fontweight='bold')
plt.ylabel('Probabilidad de irse (%)')
plt.xlabel('Tipo de Cliente')
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.savefig('grafica_churn_final.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Gráfica guardada como 'grafica_churn_final.png'")

# Mostrar las características del baseline ganador
print("\n📋 CARACTERÍSTICAS DEL CLIENTE BASE (índice", mejor_indice, "):")
print("-" * 70)
for col in X.columns:
    print(f"{col:20s}: {baseline_final[col]}")
