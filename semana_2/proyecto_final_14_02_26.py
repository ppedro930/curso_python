# ==========================================================
# Proyecto Final - Data Driven Banking (Banca Impulsada por Datos)
# Version realizada con pipelines y GridSearchCV para optimización de hiperparámetros.
# ==========================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, confusion_matrix, roc_curve
from sklearn.metrics import mean_squared_error

from sklearn.metrics import ConfusionMatrixDisplay


# ==========================================
# CONFIGURACIÓN INICIAL
# ==========================================
np.random.seed(42) #se usa de numpy.random para asegurar 
#reproducibilidad en operaciones aleatorias.
# el .seed Fija la "semilla" del generador de números 
# aleatorios de NumPy.se usa 42 por default
#(el 42 se usa para dar resultados fijos, aunque se puede 
# usar cualquier otro numero)

'''Si no usas seed:

El K-Means puede formar clusters distintos

El RandomForest puede cambiar ligeramente

Los resultados no serían 100% reproducibles'''



# ==========================================
# FASE NUMERO 0 — PREPROCESAMIENTO
# ==========================================

print("\n===== FASE NUMERO 0: PREPROCESAMIENTO =====")

df = pd.read_csv("proyecto_final.csv")

print("\nValores nulos: esto es para verificar si hay algun dato nulo en la bd") #
print(df.isnull().sum()) 

'''Si hay valores nulos, se podrían 
imputar con la media, mediana o moda según corresponda.'''

# Eliminamos columnas irrelevantes
df = df.drop(['RowNumber','CustomerId','Surname'], axis=1) 

'''Estas columnas no aportan información 
predictiva y podran 
generar ruido en los modelos.'''

# Variables
X = df.drop("Exited", axis=1)
y = df["Exited"]

'''Elimina la columna "Exited"
Guarda todo lo demás en X
axis=1 significa columnas
Si pusieras axis=0, eliminaría filas.'''

# Columnas
categoricas = ["Geography","Gender"]
numericas = [col for col in X.columns if col not in categoricas]

#se seleccionan las columnas categóricas 
# y numéricas para el preprocesamiento.

# Preprocesador AUTOMATIZADO
'''Qué es ColumnTransformer?
Es una clase de scikit-learn que permite aplicar diferentes transformaciones 
a diferentes columnas del DataFrame al mismo tiempo.'''

preprocessor = ColumnTransformer([  

    ("num", StandardScaler(), numericas), #se convierten a desviacion estandar y media 0
    ("cat", OneHotEncoder(drop="first"), categoricas) #se borran la primera categoria para evitar multicolinealidad
])

# División train/test

'''
¿Qué es train_test_split?
Es una función de Scikit-Learn (librería de Machine Learning en Python) que separa tu dataset en dos partes:
Train (entrenamiento) → para que el modelo aprenda
Test (prueba) → para evaluar qué tan bien aprendió'''

X_train, X_test, y_train, y_test = train_test_split( 
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Datos listos.")

""" ==========================================================
FASE 1 — SEGMENTACIÓN - Toma de datos
Encuentra patrones de comportamiento
Agrupa automáticamente en k grupos similares
==========================================================

    """

print("\n===== FASE 1: SEGMENTACIÓN =====")

seg_data = df[["Balance","EstimatedSalary"]] #Balance → saldo en cuenta EstimatedSalary → salario estimado

scaler_seg = StandardScaler()  #se estandarizan las variables para que tengan media 0 y desviación estándar 1, 
#lo que mejora el rendimiento de K-Means.

seg_scaled = scaler_seg.fit_transform(seg_data)

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10) #se agarran 5 clusters para segmentar a los clientes en 
#5 grupos distintos, con 10 inicializaciones para asegurar estabilidad en los resultados.
df["Cluster"] = kmeans.fit_predict(seg_scaled) # fit_predict() Ajusta el modelo Asigna cada cliente a un cluster (0–4)

cluster_stats = df.groupby("Cluster")[["Balance","EstimatedSalary"]].mean() #Agrupa por cluster y calcula el promedio de: 
#Balance EstimatedSalary  
#.mean es para Sumar todos los valores numéricos de una lista o columna y los divide entre la cantidad total de elementos. 
vip_cluster = cluster_stats.sum(axis=1).idxmax() #Suma Balance + Salary por cluster. .idxmax() Devuelve el índice (cluster) con mayor valor.

print("\nEstadísticas por Cluster:")
print(cluster_stats) 
print(f"\nCluster VIP identificado: {vip_cluster}")

plt.figure(figsize=(9,6))
sns.scatterplot(
    data=df,
    x="Balance",
    y="EstimatedSalary",
    hue="Cluster",
    palette="viridis"
)
plt.title(f"Segmentación Económica clasificacion mayor a menor (VIP = Cluster {vip_cluster})")
plt.xlabel("Balance")
plt.ylabel("Salario Estimado")
#plt.show()

"""  en esta fase 1, Se identificaron 5 perfiles de comportamiento. El Grupo VIP se caracteriza por 
     tener el mayor balance promedio y salarios altos. Este grupo es prioritario para estrategias de retención. """


"""   ==========================================================
      FASE 2 — MODELO CHURN CON PIPELINE
      ========================================================== """

print("\n===== FASE 2: MODELO DE ABANDONO =====")

pipeline_clf = Pipeline([
    ("preprocess", preprocessor),
    ("model", RandomForestClassifier( #se usa Random Forest para clasificación
        random_state=42, #para reproducibilidad
        class_weight="balanced" #se le da más peso a la clase minoritaria (clientes que abandonan) para mejorar el recall.
    ))
])

param_grid = {
    "model__n_estimators": [150, 250], # n_estimators es la cantidad de árboles en el bosque. 
    #Más árboles pueden mejorar el rendimiento pero aumentan el tiempo de entrenamiento.
    "model__max_depth": [10, 20], # max_depth es la profundidad máxima de cada árbol. Limitarla puede prevenir el sobreajuste.
    "model__min_samples_split": [2, 5] # min_samples_split es el número mínimo de muestras necesarias para 
    #dividir un nodo. Aumentarlo puede hacer el modelo más general y evitar el sobreajuste.
}

grid = GridSearchCV( #GridSearchCV es una técnica de búsqueda exhaustiva para encontrar la mejor combinación de hiperparámetros.
    pipeline_clf, #el modelo con pipeline que incluye preprocesamiento y Random Forest
    param_grid, #el espacio de hiperparámetros a explorar
    cv=3, #cross-validation con 3 folds para evaluar cada combinación de hiperparámetros de manera robusta.
    scoring="recall", #se prioriza el recall para detectar la mayor cantidad posible de clientes que abandonan,
     # aunque esto pueda aumentar los falsos positivos.
    n_jobs=-1 #para usar todos los núcleos de la CPU y acelerar la búsqueda.
)

grid.fit(X_train, y_train) #entrena el modelo con cada combinación de hiperparámetros y encuentra la mejor según el recall.

best_model = grid.best_estimator_ # el mejor modelo encontrado por GridSearchCV, que incluye el 
#preprocesamiento y los hiperparámetros óptimos para Random Forest.
 
print("\nMejores parámetros: con este parametro se dio el mejor resultado en la busqueda de patrones 250:randomforest profundidad maxima de cada arbol:10 nodo nodo necesita 5 clientes para seguir dividiendo") # se muestran los hiperparámetros que dieron el mejor resultado en la búsqueda.
print(grid.best_params_) # muestra los mejores hiperparámetros encontrados por GridSearchCV, como el número de
#árboles, la profundidad máxima y el mínimo de muestras para dividir un nodo.

# Predicciones
y_probs = best_model.predict_proba(X_test)[:,1] #predict_proba devuelve la probabilidad de cada clase. 
#[:,1] selecciona la probabilidad de la clase positiva (abandono).

# 🔥 Ajuste de umbral personalizado (priorizar recall)
threshold = 0.35 #se establece un umbral más bajo que el 0.5 estándar para clasificar a un cliente como "abandono".
y_pred_custom = (y_probs >= threshold).astype(int) #si la probabilidad de abandono es mayor o igual al umbral, se clasifica como 1 (abandono),

print("\nMatriz de Confusión:") 
print(confusion_matrix(y_test, y_pred_custom)) # La matriz de confusión muestra el número de verdaderos 
#positivos, falsos positivos, verdaderos negativos y falsos negativos, lo que ayuda a evaluar el rendimiento
# del modelo con el umbral personalizado.

print("\nReporte Clasificación cliente se queda = 0 abandona = 1:... precision es que predice y recall es el real, f.1 valor de score  de precision  y Accuracy es que acierta")
print(classification_report(y_test, y_pred_custom)) # El reporte de clasificación muestra métricas como
# precisión, recall y F1-score para cada clase 
# precision es que predice y recall es el real, f.1 valor de score 
# de precision  y Accuracy es que acierta

# Probabilidad para toda la base
df["Churn_Probability"] = best_model.predict_proba(X)[:,1] #se agrega una nueva columna al DataFrame con la 
#probabilidad de abandono para cada cliente según el modelo entrenado.

'''Riesgo de Abandono (Fase 2): El modelo de Random Forest logró un Recall del 75% para la clase de 
abandono, lo que significa que detectamos a 3 de cada 4 clientes que realmente se van a ir.'''


''' ==========================================================
#    FASE 3 — MOTOR CREDITICIO (REGRESIÓN)
#   =========================================================='''

print("\nFASE 3: MOTOR CREDITICIO - error promedio del modelo. el modelo se equivoca en unidades monetarias")

# SOLO variables solicitadas en el enunciado
X_reg = df[["Age","Balance","NumOfProducts"]] #se seleccionan solo las variables relevantes para predecir el salario estimado,
y_reg = df["EstimatedSalary"] #que es la variable objetivo en este caso.

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split( #se divide el dataset en entrenamiento y prueba para el modelo de regresión.
    X_reg, y_reg, test_size=0.2, random_state=42 #para reproducibilidad, aunque no es estrictamente necesario usar 
    #el mismo random_state que en la clasificación,
)

pipeline_reg = Pipeline([ #se crea un pipeline para el modelo de regresión que incluye escalado y el modelo de Random Forest Regressor.
    ("scaler", StandardScaler()), #se estandarizan las variables numéricas para mejorar el rendimiento del modelo de regresión.
    ("model", RandomForestRegressor( #se usa Random Forest para regresión
        random_state=42, #para reproducibilidad
        n_estimators=150 #número de árboles en el bosque, se puede ajustar para mejorar el rendimiento.
    ))
])

pipeline_reg.fit(X_train_r, y_train_r) #entrena el modelo de regresión con el conjunto de entrenamiento.

y_pred_r = pipeline_reg.predict(X_test_r) #se generan las predicciones de salario estimado para el conjunto de prueba.

rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r)) #se calcula el RMSE (Root Mean Squared Error) para 
#evaluar la precisión del modelo de regresión.
print(f"RMSE modelo salarial: {rmse:.2f}") # Un RMSE más bajo indica un mejor ajuste del modelo a los datos.

# Residuos
residuos = y_test_r - y_pred_r #se calculan los residuos (errores) restando las predicciones de los valores reales.

plt.figure(figsize=(8,6)) #se crea una gráfica de dispersión para analizar los residuos del modelo de regresión.
sns.scatterplot(x=y_pred_r, y=residuos) #en el eje x se colocan las predicciones y en el eje y los residuos.
plt.axhline(0, color="red", linestyle="--") #se agrega una línea horizontal en y=0 para facilitar la visualización 
#de los residuos positivos y negativos.
plt.title("Análisis de Residuos") #el análisis de residuos ayuda a verificar si los errores del modelo están distribuidos 
#aleatoriamente, lo que es un buen indicador de un modelo bien ajustado.
plt.xlabel("Salario Predicho") #se etiqueta el eje x como "Salario Predicho" para indicar que las predicciones de salario están en ese eje.
plt.ylabel("Error") #se etiqueta el eje y como "Error" para indicar que los residuos (errores) del modelo están en ese eje.
#plt.show()









#matrix de confusion para el modelo de clasificación con umbral personalizado


cm = confusion_matrix(y_test, y_pred_custom)

# ---- GRAFICA ----
plt.figure(figsize=(6,5))

sns.heatmap(cm,
            annot=True,
            fmt='d',
            cmap='rocket',
            cbar=True,
            
            
            xticklabels=['Pred: se queda','Pred: se va'],
            yticklabels=['Real: se queda','Real: se va']
)

plt.xlabel('Predicción del modelo')
plt.ylabel('Valor real')
plt.title('Matriz de Confusión')
#plt.show()











#===== FASE 2: MODELO DE ABANDONO =====
'''

results = pd.DataFrame(grid.cv_results_)

plt.figure()
plt.scatter(results["param_model__n_estimators"], results["mean_test_score"])
plt.xlabel("Número de árboles")
plt.ylabel("Score")
plt.title("Score vs n_estimators") '''
















#plt.savefig('residuals_analysis.png')
#print("Gráfica de residuos guardada como 'residuals_analysis.png'")

# Predicción completa
df["S_pred"] = pipeline_reg.predict(X_reg) #se agrega una nueva columna al DataFrame con las predicciones de salario
#estimado para toda la base de datos,

# Regla de negocio
df["Credit_Limit"] = (df["S_pred"] * 0.25) + (df["CreditScore"] * 10) #se crea una nueva columna "Credit_Limit" que 
#combina el salario predicho (S_pred) y el puntaje crediticio (CreditScore)

'''en esta fase: Se generó un límite de crédito ($L$) personalizado combinando 
el salario predicho y el puntaje crediticio.'''


'''==========================================================
   RETO FINAL — MATRIZ INTELIGENCIA COMERCIAL
   =========================================================='''

print("\n===== MATRIZ FINAL =====")

df["VIP_Status"] = df["Cluster"].apply( #se crea una nueva columna "VIP_Status" que clasifica a los clientes como 
    #"VIP" o "Regular" según su cluster.
    lambda x: "VIP" if x == vip_cluster else "Regular" #si el cluster del cliente es el mismo que el cluster 
    #identificado como VIP, se le asigna "VIP", de lo contrario se le asigna "Regular".
)

def estrategia(row): #se define una función que asigna una estrategia comercial a cada cliente según su 
    #probabilidad de abandono y su estatus VIP.
    if row["Churn_Probability"] > 0.6: #si la probabilidad de abandono es mayor al 60%, 
        #se asigna la estrategia de "RETENCION INMEDIATA".
        return "RETENCION INMEDIATA" #esta estrategia implica acciones urgentes para retener al cliente, como ofertas personalizadas,
    elif row["VIP_Status"] == "VIP" and row["Churn_Probability"] < 0.3: #si el cliente es VIP y tiene una
        # baja probabilidad de abandono (menos del 30%),
        return "OFERTA EXCLUSIVA" #se le asigna la estrategia de "OFERTA EXCLUSIVA", 
    #que podría incluir beneficios especiales para mantener su lealtad.
    else:
        return "FIDELIZACION ESTANDAR" #si el cliente no cumple ninguna de las condiciones anteriores, 
    #se le asigna la estrategia de "FIDELIZACION ESTANDAR",

df["Tactical_Guideline"] = df.apply(estrategia, axis=1) #se aplica la función "estrategia" a cada fila del DataFrame
#para generar una nueva columna "Tactical_Guideline" que contiene la estrategia comercial recomendada para cada cliente.

# Exportación
df.to_csv("final_intelligence_matrix.csv", index=False) #se exporta el DataFrame completo a un archivo CSV llamado 
#"final_intelligence_matrix.csv" sin incluir el índice de las filas.

print("\nArchivo generado: final_intelligence_matrix.csv")
print("\nProceso completado con éxito.")
plt.show()

'''Matriz de Inteligencia: Se exportó un archivo final donde cada cliente tiene una 
estrategia asignada: Retención Inmediata, Oferta de Exclusividad o Fidelización Estándar.'''

