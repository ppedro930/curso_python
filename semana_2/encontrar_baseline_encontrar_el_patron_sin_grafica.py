import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression




import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler



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

print("🔍 Buscando el baseline perfecto...")
print("=" * 60)

# Probar diferentes baselines del dataset real
mejor_baseline = None
mejor_diferencia = float('inf')

for i in range(min(1000, len(X))):  # Probar los primeros 1000 clientes
    baseline = X.iloc[i].to_dict()
    
    # Crear los dos clientes
    clientes = pd.DataFrame([
        {**baseline, 'InternetService': 'Fiber optic', 'Contract': 'Month-to-month'},
        {**baseline, 'InternetService': 'DSL', 'Contract': 'Two year'}
    ])
    
    # Predecir
    prob = Pipeline_churn.predict_proba(clientes)[:, 1] * 100
    
    # Calcular diferencia con objetivo
    diff_a = abs(prob[0] - 5.6)
    diff_b = abs(prob[1] - 0.6)
    diferencia_total = diff_a + diff_b
    
    if diferencia_total < mejor_diferencia:
        mejor_diferencia = diferencia_total
        mejor_baseline = baseline.copy()
        mejor_prob_a = prob[0]
        mejor_prob_b = prob[1]
        mejor_indice = i
        
        # Si encontramos algo muy cercano, mostrarlo
        if diferencia_total < 0.5:
            print(f"\n✅ ¡Encontrado! Índice {i}")
            print(f"   Cliente A: {prob[0]:.2f}% (objetivo: 5.6%)")
            print(f"   Cliente B: {prob[1]:.2f}% (objetivo: 0.6%)")
            print(f"   Diferencia total: {diferencia_total:.3f}")
            break

print("\n" + "=" * 60)
print("🎯 MEJOR BASELINE ENCONTRADO:")
print("=" * 60)
print(f"Índice del dataset: {mejor_indice}")
print(f"Cliente A (Mes a mes + Fibra): {mejor_prob_a:.2f}%")
print(f"Cliente B (2 años + DSL): {mejor_prob_b:.2f}%")
print(f"\nDiferencia con objetivo: {mejor_diferencia:.3f}")

print("\n📋 CARACTERÍSTICAS DEL BASELINE:")
print("-" * 60)
for key, value in mejor_baseline.items():
    print(f"{key:20s}: {value}")

print("\n💾 CÓDIGO PARA USAR ESTE BASELINE:")
print("-" * 60)
print("baseline = {")
for key, value in mejor_baseline.items():
    if isinstance(value, str):
        print(f"    '{key}': '{value}',")
    else:
        print(f"    '{key}': {value},")
print("}")

















# Valores reales encontrados
cliente_a = mejor_prob_a
cliente_b = mejor_prob_b

# Objetivos
objetivo_a = 5.6
objetivo_b = 0.6

# Crear DataFrame para graficar
df_plot = pd.DataFrame({
    'Tipo': ['Cliente A', 'Cliente B'],
    'Probabilidad Encontrada': [cliente_a, cliente_b],
    'Objetivo': [objetivo_a, objetivo_b]
})

# Configuración estética
sns.set(style="whitegrid")
plt.figure(figsize=(8,6))

# Gráfico de barras comparativo
x = np.arange(len(df_plot['Tipo']))
width = 0.35

plt.bar(x - width/2, df_plot['Probabilidad Encontrada'], width, label='Encontrado')
plt.bar(x + width/2, df_plot['Objetivo'], width, label='Objetivo')

# Etiquetas
plt.xticks(x, df_plot['Tipo'])
plt.ylabel('Probabilidad (%)')
plt.title('Comparación Baseline vs Objetivo')
plt.legend()

# Mostrar valores encima de las barras
for i in range(len(df_plot)):
    plt.text(i - width/2, df_plot['Probabilidad Encontrada'][i] + 0.1,
             f"{df_plot['Probabilidad Encontrada'][i]:.2f}%",
             ha='center')

    plt.text(i + width/2, df_plot['Objetivo'][i] + 0.1,
             f"{df_plot['Objetivo'][i]:.2f}%",
             ha='center')

plt.tight_layout()
plt.show()

