'''Identificar patrones de comportamiento en 

la base 
de clientes de 
Telco 

transformando datos de facturación y antigüedad en segmentos estratégicos. 

Se utilizará el algoritmo K-Means para agrupar a los usuarios y se interpretarán los perfiles resultantes 

mediante un análisis visual multidimensional para detectar oportunidades de retención o venta.
'''


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

"""pandas: manipulación de datos (DataFrames) .
numpy: operaciones numéricas.
matplotlib: gráficos base (aca es para interpretar los datos brindados a una grafica especifica).
seaborn: gráficos más profesionales y estadísticos.
¿Por qué?
Porque vas a necesitar cargar, limpiar, transformar, modelar y visualizar datos. 
Estas librerías son las herramientas estándar para cada una de esas tareas en Python.
Limpiar datos
Transformarlos
Aplicar modelo
Visualizar resultados

¿Qué hace?
KMeans: algoritmo de clustering. (el clustering es una técnica de aprendizaje no supervisado que 
agrupa datos similares en clusters o grupos. KMeans es uno de los algoritmos más populares para 
realizar clustering, y se basa en la idea de minimizar la distancia entre los puntos de datos y 
el centroide del cluster al que pertenecen.)
StandardScaler: estandariza variables. (es decir convierte los numeros en una 
escala común con media 0 y desviación estándar 1)
¿Por qué?

K-Means funciona con distancias. Si no escalas, una variable grande dominaría a las demás.
 """  #shift + alt + a para comentar


# Configuración visual

#sns.set(style="whitegrid")


# 2. CARGA DE DATOS

df = pd.read_csv('Telco-Customer-Churn.csv') #la tipica de mandar a traer el archivo para saber con que datos se va a trabajar


# 3. LIMPIEZA DE DATOS

# Convertir TotalCharges a numérico
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce') # Convertir a numérico, forzando errores a NaN

# Eliminar valores nulos
df = df.dropna() # Eliminar filas con valores faltantes (NaN) para evitar problemas en el modelo


# 4. SELECCIÓN DE VARIABLES

variables = ['tenure', 'MonthlyCharges', 'TotalCharges']
X = df[variables]

'''Selecciona solo: tenure → antigüedad... MonthlyCharges → facturación mensual... y TotalCharges → facturación acumulada
¿Por qué? Porque tu objetivo es segmentar según: Tiempo del cliente Nivel de gasto Esto está alineado con la estrategia de retención.'''

# 5. ESCALAMIENTO

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

'''¿Qué hace? Calcula media y desviación estándar. Transforma los datos a escala estándar: ¿Por qué?
TotalCharges puede estar en miles tenure en meses MonthlyCharges en decenas Si no escalas → la variable 
más grande domina la distancia.'''

# 6. MÉTODO DEL CODO

wcss = []

'''WCSS = Within Cluster Sum of Squares (aca se usa el metodo del codo para determinar el número óptimo de clusters)
'''

for i in range(1, 11): # este ciclo for Prueba clusters del 1 al 10 la letra i es un valor numerico que va a 
    #descubrir en cada cluster para almacenarlo en la variable n_clusters=i.
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42) #kmeans++ es un método y parametro de inicialización que 
    #mejora la selección de los centroides iniciales, lo que puede conducir a una mejor convergencia y resultados más estables.
    kmeans.fit(X_scaled) #entrena el modelo de KMeans con los datos convertidos (los que se guardaron en la variable x_scaled)  escalados 
    #para el número de clusters especificado por i. (después de entrenar el modelo, esos datos entrenados se guardan en la variable kmeans).
    wcss.append(kmeans.inertia_) #.append guarda (anexa) la suma de errores en la variable kmeans.inertia_ (esto para
    #mostrar qué tan compactos son los clusters).

    '''Parámetros:
n_clusters=i: número de clusters
k-means++: mejor inicialización
random_state=42: reproducibilidad'''

plt.figure(figsize=(8,5)) #tamaño de la grafica, ancho 8 y alto 5 pulgadas
plt.plot(range(1,11), wcss, marker='o') #Grafica el método del codo.
plt.title('Método del Codo') #imprime el titulo en la grafica
plt.xlabel('Número de Clusters') #plt.xlabel es una etiqueta que muestra el texto en el eje x de la grafica
plt.ylabel('WCSS')  #plt.xlabel es una etiqueta que muestra el texto en el eje y de la grafica
#plt.show()


# 7. MODELO FINAL (AJUSTAR k SEGÚN CODO)

k_optimo = 4  # Puedes cambiarlo según el gráfico del codo. Observa dónde la curva se "dobla" o se estabiliza.
#Aquí decides usar 4 clusters (si agregas mas... se van a contabilizar mas colores en la grafica de los clusters).

kmeans = KMeans(n_clusters=k_optimo, init='k-means++', random_state=42)# aca son las variables de el número de clusters, 
# el método de inicialización y la semilla para reproducibilidad.
df['cluster'] = kmeans.fit_predict(X_scaled)

'''nuevamente Entrena el modelo final los datos de x_scaled para guardarlos en kmeans con el número óptimo de clusters 
 (k_optimo) el koptimo muestra los cluster asignados en la grafica clasificandolos por colores y asigna 
las etiquetas de cluster a cada cliente en el DataFrame original.

Asigna cada cliente a un cluster

Ahora cada cliente tiene una etiqueta:
0, 1, 2 o 3 (porque k=4) (porque si agregas mas... se van a contabilizar mas colores en la grafica de los clusters 
y 4 es un numero propicio para mostrar de forma balanceada la grafica).'''


# 8. VISUALIZACIÓN 2D

plt.figure(figsize=(8,6))
sns.scatterplot(
    x=df['tenure'],
    y=df['MonthlyCharges'],
    hue=df['cluster'],
    palette='Set2'
)
plt.title('Segmentación de Clientes Telco') #titulo
plt.xlabel('Antigüedad (tenure)') #titulo del eje x
plt.ylabel('Facturación Mensual') #titulo del eje y
plt.legend(title='Cluster') #leyenda con el titulo cluster para identificar cada color con su cluster correspondiente
#plt.show()


# 9. ANÁLISIS MULTIDIMENSIONAL

sns.pairplot(df, vars=variables, hue='cluster', palette='Set2') #esta hace que aparezcan todas las 9 graficas de dispersión 
# con sus 4 clusters entre las variables seleccionadas (tenure, MonthlyCharges, TotalCharges) coloreadas por cluster, lo que permite analizar
#visualmente las relaciones y diferencias entre los segmentos de clientes en múltiples dimensiones.
#plt.show()


# 10. PERFIL PROMEDIO POR CLUSTER

resumen = df.groupby('cluster')[variables].mean() # Calcula el promedio por grupo de los campos Cluster, 
#tenure, MonthlyCharges, TotalCharges
print("\n===== PERFIL PROMEDIO POR CLUSTER =====\n") #imprime el titulo del resumen
print(resumen) #imprime el resumen con el perfil promedio de cada cluster 
#para las variables seleccionadas (tenure, MonthlyCharges, TotalCharges) 
# lo que permite interpretar las características típicas de cada segmento de clientes.


# 11. TAMAÑO DE CADA CLUSTER

print("\n===== CANTIDAD DE CLIENTES POR CLUSTER =====\n")
print(df['cluster'].value_counts()) #Cuenta cuántos clientes hay en cada cluster y 
#lo imprime, lo que ayuda a entender la distribución 
#de clientes entre los segmentos identificados por K-Means.

# 12. EXPORTAR RESULTADO

df.to_csv('Telco_segmentado.csv', index=False) # Exporta el DataFrame con la segmentación a 
#un nuevo archivo CSV llamado 'Telco_segmentado.csv' sin incluir el índice de filas, 
# lo que permite guardar los resultados para su uso posterior o análisis adicional.

print("\nSegmentación completada y archivo exportado correctamente.")

plt.show()
