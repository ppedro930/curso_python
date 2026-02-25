import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ===============================
# 1. CARGA DE DATOS
# ===============================

'''
seaborn → Es una librería de visualización de datos en Python.

 KMeans, ejecuta el algoritmo de k menas. n_clusters es el numero de cluster que tendra el algoritmo,
pero en el for anterior se esta probando con clusters de 1 a 10 2.- el argumento init='k-means++', 
indicaque el algoritmo colocara los centroides lo mas alejado entre ellos para que el algoritmo convenga. 
la parte de wcss.append(k_means.inertia_) es para agregar a la lista vacia wcss los errores que hay de 
acuerdo con el numero de cluster con el fin de identificar el numero de cluster optimo.

mean es promedio

tienen hasta mañana a las 8:30 am

'''

df = pd.read_csv('Mall_Customers.csv')

# Seleccionamos columnas: Annual Income y Spending Score
eje_x = df.iloc[:, [3, 4]].values

'''iloc significa:
integer location Sirve para seleccionar filas y columnas por posición numérica, no por nombre. 
df.iloc[filas y columnas]

dos puntpos : significa
Todas las filas
Columnas en posición 3 y 4
en Python se empieza desde 0: '''

# ===============================
# 2. ESCALADO
# ===============================

scaler = StandardScaler()
x_scaled = scaler.fit_transform(eje_x)

'''¿Qué es StandardScaler?
StandardScaler es una clase de scikit-learn que sirve para estandarizar (transforma variables para que tenga media (0)
y desviacion estandar (1)) es decir transforma a ese formato los datos numéricos. 
ahora la linea
scaler = StandardScaler() crea el objetivo que va a escalar

ahora fit() Calcula:
La media de cada columna y variable
La desviación estándar de cada columna y variable

que hace la linea?
x_scaled = scaler.fit_transform(eje_x)
Aprende la media y desviación de tus datos
Transforma los datos ... eso lo hace StandardScaler
Devuelve un array escalado
Lo guarda en x_scaled'''

# ===============================
# 3. MÉTODO DEL CODO
# ===============================

wcss = []
for i in range(1, 11):
    k_means = KMeans(n_clusters=i, init='k-means++', random_state=42)
    k_means.fit(x_scaled)
    wcss.append(k_means.inertia_)




'''KMeans es un algoritmo de clustering de scikit-learn que agrupa datos en 
K grupos basándose en distancia (normalmente euclidiana).

wcss = []
que es ?
WCSS = Within-Cluster Sum of Squares
o en español... Suma de distancias cuadradas de cada punto a su centroide
que hace? Crea una lista vacía donde se guardará el WCSS de cada modelo.

En sklearn se obtiene con:
k_means.inertia_

Para qué sirve esto?
Para encontrar el número óptimo de clusters usando el:
📉 Método del Codo (Elbow Method) luego se grafica con plt.show()
y especificar lo demas

for i in range(1, 11):
Prueba valores de K desde 1 hasta 10 clusters.


Aquí se crea el modelo:

n_clusters=i es el número de grupos
init='k-means++' = inicializa centroides inteligentemente (mejor convergencia)
random_state=42 = para que siempre dé el mismo resultado



'''



plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Método del Codo')
plt.xlabel('Número de clusters')
plt.ylabel('WCSS (Inercia)')
plt.show() 

# ===============================
# 4. MODELO FINAL
# ===============================

k_means = KMeans(n_clusters=5, init='k-means++', random_state=42)
y_kmeans = k_means.fit_predict(x_scaled)

# ===============================
# 5. VISUALIZACIÓN DE CLUSTERS
# ===============================

plt.figure(figsize=(10, 7))

for i in range(5):
    plt.scatter(eje_x[y_kmeans == i, 0],
                eje_x[y_kmeans == i, 1],
                s=100,
                label=f'Cluster {i+1}')

centroides_reales = scaler.inverse_transform(k_means.cluster_centers_)

plt.scatter(centroides_reales[:, 0],
            centroides_reales[:, 1],
            s=300,
            c='black',
            marker='X',
            label='Centroides')

plt.title('Segmentación de Clientes')
plt.xlabel('Ingresos anuales (k$)')
plt.ylabel('Spending Score (1-100)')
plt.legend()
plt.show()    #shift + alt + a para comentar

# ===============================
# 6. RESUMEN NUMÉRICO
# ===============================

df['cluster'] = y_kmeans #esta es la variable de entrenamiento con los datos ya analizados a mostrar

'''groupby('cluster') agrupa el DataFrame por la columna 'cluster', lo que permite calcular 
estadísticas para cada grupo de clientes identificado por K-Means.'''

resumen_numerico = df.groupby('cluster')[
    ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
].mean() # mean calcula el promedio de cada columna dentro de cada grupo.

resumen_numerico = np.ceil(resumen_numerico)
resumen_numerico = pd.DataFrame(
    resumen_numerico,
    columns=['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
)

resumen_generico = pd.crosstab(df['cluster'], df['Gender'])

'''pd.crosstab() es una función de pandas que crea una tabla de contingencia (tabla cruzada).
Es decir:
Cuenta cuántas veces ocurre cada combinación entre dos variables. 
en este caso Está cruzando:

Filas que es el cluster
Columnas: solo usa Gender que al encontrarlo
Valores:  busca y verifica la cantidad de registros'''

print("\n--- PROMEDIOS POR GRUPO ---")
print(resumen_numerico)

print("\n--- DISTRIBUCIÓN DE GÉNERO ---")
print(resumen_generico)

# ===============================
# 7. HEATMAP DE PROMEDIOS
# ===============================

plt.figure(figsize=(10, 5))
sns.heatmap(resumen_numerico.T,
            annot=True,
            fmt=".0f",
            cmap="YlGnBu",
            cbar=False)

plt.title('Promedios por grupo')
plt.show()
 
# ===============================
# 8. BOXPLOT CON CUARTILES
# ===============================

mediana = df.groupby('cluster')['Age'].median().sort_index()
cuartil_superior = df.groupby('cluster')['Age'].quantile(0.75).sort_index()
cuartil_inferior = df.groupby('cluster')['Age'].quantile(0.25).sort_index()
extremo_superior = df.groupby('cluster')['Age'].max().sort_index()
extremo_inferior = df.groupby('cluster')['Age'].min().sort_index()

'''
En estas líneas se están calculando las estadísticas que se mostrarán en el boxplot.
Se agrupan los datos por cluster y se trabaja únicamente con la columna 'Age'
para obtener: mediana, cuartil inferior, cuartil superior, valor mínimo y valor máximo.
Estas métricas permiten construir visualmente el diagrama de caja.
'''

plt.figure(figsize=(10, 6))
ax = sns.boxplot(x='cluster', y='Age', data=df, palette='viridis')

for i in range(len(mediana)):

    val_mediana = mediana.iloc[i]
    val_q3 = cuartil_superior.iloc[i]
    val_q1 = cuartil_inferior.iloc[i]
    val_max = extremo_superior.iloc[i]
    val_min = extremo_inferior.iloc[i]

    '''
   Cuando se usa groupby():
se Obtiene una Serie con varios valores.
Cuando se usa .iloc[i]: se
Extrae un solo valor numérico.
Y matplotlib necesita solamente un número individual.
ahora porque iloc? nuevamente... la libreria matplotlib necesita un valor individual 
y por ende necesita números
.iloc[i] extrae ese número necesario...

matplotlib no puede usar toda la Serie, necesita un número para saber dónde escribir el texto.'''

    # Mediana
    ax.text(i, val_mediana,
            f'mediana:{val_mediana:.1f}',
            ha='center',
            va='center',
            fontweight='bold',
            color='white',
            fontsize=11,
            bbox=dict(facecolor='black', alpha=0.5, pad=3))

    # Q3
    ax.text(i, val_q3,
            f'cuartil 3 sup: {val_q3:.1f}',
            ha='center',
            va='bottom',
            color='black',
            fontsize=9,
            fontweight='bold')

    # Q1
    ax.text(i, val_q1,f'cuartil 1 inf: {val_q1:.1f}', ha='center',va='top', color='black', fontsize=9, fontweight='bold')
    
     # Extremo superior (máximo)
    ax.text(i, val_max,
            f'extremo sup: {val_max:.1f}',
            ha='center',
            va='bottom',
            color='black',
            fontsize=8,
            fontweight='bold')

    # Extremo inferior (mínimo)
    ax.text(i, val_min,
            f'Extremo inf: {val_min:.1f}',
            ha='center',
            va='top',
            color='blue',
            fontsize=8,
            fontweight='bold')


plt.title('Distribución de Edad por Grupo')
plt.xlabel('Cluster') # representa el cluster en el eje x
plt.ylabel('Edad')
plt.show()


'''
Aquí se está agregando un texto personalizado dentro del gráfico.
ax.text() coloca una etiqueta en la posición (i, val_min),
donde "i" representa la posición del cluster en el eje X
y "val_min" representa el valor mínimo de edad en el eje Y.

El texto que se muestra es el valor del extremo inferior formateado
con un decimal (.1f).

ha='center' centra el texto horizontalmente respecto al punto.
va='top' alinea el texto por encima del valor mínimo.
color='blue' define el color del texto.
fontsize=8 establece el tamaño de la letra.
fontweight='bold' pone el texto en negrita.

Finalmente, plt.show() se utiliza para mostrar el gráfico en pantalla.
Sin esta línea, el gráfico puede no visualizarse dependiendo del entorno
donde se esté ejecutando el código.
'''