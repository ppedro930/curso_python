import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
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
        ('categorias', OneHotEncoder(drop='first'), columnas_categoricas) #Convierte variables categóricas en numéricas

#Con OneHotEncoder y drop solo elimina las que ya estan convertidas a numericas y deja solo una de cada categoria para evitar
# la multicolinealidad
    ]
)

Pipeline_churn = Pipeline(steps=[
    ('Preprocesamiento', preprocessor),
    ('Clasificacion', LogisticRegression(max_iter=1000, random_state=42))
])

# Entrenar modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
Pipeline_churn.fit(X_train, y_train)

# BASELINES CANDIDATOS - Probar diferentes configuraciones
baselines_candidatos = [
    # Baseline 1: Cliente con servicios básicos
    {
        'gender': 'Male',
        'SeniorCitizen': 0,
        'Partner': 'Yes',
        'Dependents': 'Yes',  # Con dependientes
        'tenure': 24,  # 2 años
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',  # Con seguridad
        'OnlineBackup': 'Yes',  # Con backup
        'DeviceProtection': 'Yes',  # Con protección
        'TechSupport': 'Yes',  # Con soporte
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'No',  # Con papel
        'PaymentMethod': 'Bank transfer (automatic)',
        'MonthlyCharges': 65.0,
        'TotalCharges': 1560.0
    },
    # Baseline 2: Cliente más estable
    {
        'gender': 'Female',
        'SeniorCitizen': 0,
        'Partner': 'Yes',
        'Dependents': 'Yes',
        'tenure': 36,  # 3 años
        'PhoneService': 'Yes',
        'MultipleLines': 'Yes',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'Yes',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'Yes',
        'StreamingMovies': 'Yes',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Credit card (automatic)',
        'MonthlyCharges': 80.0,
        'TotalCharges': 2880.0
    },
    # Baseline 3: Cliente conservador
    {
        'gender': 'Male',
        'SeniorCitizen': 1,  # Senior
        'Partner': 'Yes',
        'Dependents': 'No',
        'tenure': 60,  # 5 años - muy antiguo
        'PhoneService': 'Yes',
        'MultipleLines': 'No',
        'InternetService': 'DSL',
        'OnlineSecurity': 'Yes',
        'OnlineBackup': 'No',
        'DeviceProtection': 'Yes',
        'TechSupport': 'Yes',
        'StreamingTV': 'No',
        'StreamingMovies': 'No',
        'Contract': 'Month-to-month',
        'PaperlessBilling': 'No',
        'PaymentMethod': 'Mailed check',
        'MonthlyCharges': 50.0,
        'TotalCharges': 3000.0
    }
]

print("🔍 Probando diferentes baselines...")
print("=" * 80)

mejor_baseline = None
mejor_diferencia = float('inf')

for idx, baseline in enumerate(baselines_candidatos):
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
    
    print(f"\nBaseline {idx + 1}:")
    print(f"  Cliente A (Mes a mes + Fibra): {prob[0]:.2f}% (objetivo: 5.6%)")
    print(f"  Cliente B (2 años + DSL): {prob[1]:.2f}% (objetivo: 0.6%)")
    print(f"  Diferencia total: {diferencia_total:.3f}")
    
    if diferencia_total < mejor_diferencia:
        mejor_diferencia = diferencia_total
        mejor_baseline = baseline.copy()
        mejor_prob_a = prob[0]
        mejor_prob_b = prob[1]
        mejor_idx = idx + 1

print("\n" + "=" * 80)
print(f"🎯 MEJOR BASELINE: Candidato {mejor_idx}")
print("=" * 80)
print(f"Cliente A: {mejor_prob_a:.2f}% (objetivo: 5.6%)")
print(f"Cliente B: {mejor_prob_b:.2f}% (objetivo: 0.6%)")
print(f"Diferencia: {mejor_diferencia:.3f}")

# Crear visualización con el mejor baseline
clientes_finales = pd.DataFrame([
    {**mejor_baseline, 'InternetService': 'Fiber optic', 'Contract': 'Month-to-month'},
    {**mejor_baseline, 'InternetService': 'DSL', 'Contract': 'Two year'}
])

prob_finales = Pipeline_churn.predict_proba(clientes_finales)[:, 1] * 100

plt.figure(figsize=(14, 6))

colores = ['#ff6b6b' if prob_finales[0] > prob_finales[1] else '#4ecdc4',
           '#4ecdc4' if prob_finales[1] < prob_finales[0] else '#ff6b6b']

barras = plt.bar(
    ['Cliente A\n(Mes a Mes + Fibra)', 'Cliente B\n(2 Años + DSL)'],
    prob_finales,
    alpha=0.85,
    color=colores
)

plt.axhline(y=50, linestyle='--', linewidth=2, alpha=0.6, color='gray')
plt.text(0.5, 52, 'ZONA DE RIESGO (>50%)', ha='center', fontsize=12, color='gray')

for i, (barra, prob) in enumerate(zip(barras, prob_finales)):
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
plt.savefig('comparacion_churn.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n📊 Gráfica guardada como 'comparacion_churn.png'")

print("\n💾 CÓDIGO FINAL PARA USAR:")
print("-" * 80)
print("baseline = {")
for key, value in mejor_baseline.items():
    if isinstance(value, str):
        print(f"    '{key}': '{value}',")
    else:
        print(f"    '{key}': {value},")
print("}")
