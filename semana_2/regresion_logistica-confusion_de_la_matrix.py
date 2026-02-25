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

'''
la clase oneHotEncoder sirve para transformar las variables string en variables binarias ejemplo la columna genero
puede transformar de  tal manera que 1 sea hombre y 0 mujer y viceversa
la clase StandardScaler, sirve para transformar los valores numericos a 0 y 1 eso quiere decir que si tienes 2 columnas
importantes y una tiene el valor de 7000 y otra el valor de 7 entonces el modelo no piense que el valor de 7000 es mas 
importante por ser mas grande. asi que convierte ambas columnas en valores de 0 o 1

la clase ColumNTransformer permite aplicar diferentes transformaciones a diferentes columnas al mismo 
tiempo

para que sirve? para aplicar StandardScaler a las columnas numericas y oneHotEncoder a las columnas categoricas
la clase pipeline
permite encadenar pasos secuenciales, en otras palabras empaqueta el procesamiento y el modelo en un solo objeto
para que sirve? asegura que los datos de prueba y entrenamiento sufran las mismas transformaciones de manera exacta
asi, se evita de errores comunes o fuga de datos (data leakage)

confusion_Matrix

este es un metodo que genera una tabla que conmpara las predicciones del modelo con la realidad.

muestra los aciertos y errores especificos como:falsos positivos era un si pero el modelo dijo que no ) y falsos 
negativos (el modelo dijo que no pero era un si)
'''
df = pd.read_csv('Telco-Customer-Churn.csv')

df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

X=df.drop(['customerID','Churn'], axis=1) #el axis va escaneando columna por columna y si encuentra la columna que se le indico 
#la elimina del DataFrame en este caso se eliminarian las columnas (customerID y Churn)
# las cuales fueron las indicadas y se guardaria el resultado en la variable X (todas las demas columnas)

y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

columnas_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges']

columnas_categoricas = X.select_dtypes(include=['object', 'string']).columns.tolist()

print(columnas_categoricas)

'''
Genero: Hombre o Mujer

la clase OneHot Encoder creara las siguientes columnas de acuerdo al genero

Es_Hombre y Es_Mujer

1           0

Supongamos que un valorn en el genero es Male de masculino y por lo tanto es un hombre:

Es_Hombre      Es_Mujer
    1             0

Cliente         Gender
Ana             Female
Jose Luis       Male
Karla           Female
Pedro           Male
Belen           Female
Angel           Male

Tabla despues cde aplicar el encoder

Cliente         Es_Hombre       Es_Mujer
Ana                 0               1
Jose luis           1               0
Belen               0               1   
Angel               1               0 
Karla               0               1

El problema de la redundancia.

Si ¿Es_Mujer? es 1 ENTONCES No es hombre
Si ¿Es_Hombre? es 1 ENTONCES No es mujer
Si ¿Es_Mujer? es 0 ENTONCES No es hombre
Si ¿Es_Hombre? es 0 ENTONCES No es mujer

despues de aplicar drop='first', el encoder haria lo siguiente

Cliente         Es_Mujer
Ana                 1
Jose Luis           0
Belen               1
Angel               0
Karla               1



'''

preprocessor = ColumnTransformer(
    transformers=[
        ('numeros', StandardScaler(), columnas_numericas),
        ('categorias',OneHotEncoder(drop='first'), columnas_categoricas)
    ]
)



Pipeline_churn =Pipeline(steps=[
    ('Preprocesamiento', preprocessor),
    ('Clasificacion', LogisticRegression())

]
)


X_train, X_test, y_train, y_test =train_test_split(X,y, test_size=0.2, random_state=42) # el split divide los datos en entrenamiento y 
#prueba, el test_size es el porcentaje de datos que se usaran para la prueba (en este caso el 20%) y el random_state 
# es para asegurar que la división sea reproducible (es decir que cada vez que ejecutes el código obtendrás la misma división de datos).

Pipeline_churn.fit(X_train, y_train)

prediccion = Pipeline_churn.predict(X_test)

print("------------- REPORTE DE CLASIFICACIÓN ------------------")
print(classification_report(y_test,prediccion))

'''macro avg (average) y weighted avg  que significa '''

#macro_av = (10+7) / 2=8.5
#weight_av = (10*70) + (7*2) / 10=84 / 10=8.4

probabilidades = Pipeline_churn.predict_proba(X_test)[:5]
print("\n Probabilidades (se queda, se va)")

print(probabilidades)
matrix_confusion = confusion_matrix(y_test, prediccion)

plt.figure(figsize=(10,6))

ax= sns.heatmap(matrix_confusion, annot=True, fmt='d', cmap='rocket', cbar=True, 
    xticklabels=['Pred: se queda', 'Pred:se va, arriba es el real:se va'],
    yticklabels=['Real:se queda', 'Pred: se queda'])
    
ax.set(xlabel = 'prediccion del modelo',
       ylabel = 'verdad (Datos Reales)',
       title = 'Matriz de confucion del modelo de regresion lineal')

plt.show()


''' segun la grafica dice que supuestamente se iban
194 personas pero en realidad se fueron 118 y predijo que se quedaban 180 cando en realidad 
se quedaron 915'''


prob_fuga = Pipeline_churn.predict_proba(X_test)[:,1]

'''
[:,1] -> es para decirle que devuelva todas las filas y una sola columna (es decir, que me devuelva esa columna con todos sus registros).

en este caso me devuelve todas las filas y la probabilidad de la clase 1 (que se va el cliente ) ya que
es la variable de interes para el negocio

: (dos puntos) -> significa que me dara todas las filas (todos los registros).
'''

lista_marketing = pd.DataFrame({
    'Customer ID':df.loc[X_test.index,'customerID'],
    'Probabilidad de fuga':prob_fuga,
    'Status real': y_test
})

lista_llamadas = lista_marketing[lista_marketing['Probabilidad de fuga'] > 0.3].sort_values(by = 'Probabilidad de fuga',
    ascending=False)

'''.sort_values sirve para ordenar el dataframe de manera ascendente o descendente 

el argumento "by" le indica que use una columna como base para ordenar en este caso se usara como la base
la columna "probabilidad de fuga" para que ordene el DataFrame.

El argumento "ascending" funciona para indicar si lo ordenara de menor a mayor (ascendiente o descendiente)
 en este caso so pone ascending=False para que sea descendiente
'''

print(f"Lista generada, se tiene {len(lista_llamadas)} clientes en riesgo de abandono")
print(lista_llamadas.head(10))




