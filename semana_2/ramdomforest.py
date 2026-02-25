import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

df = pd.read_csv('Telco-Customer-Churn.csv')

# 2. LIMPIEZA
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df = df.dropna()

eje_x = df.drop(['customerID', 'Churn'], axis=1)
eje_y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

# 3. DEFINICIÓN DE COLUMNAS
columnas_numericas = ['tenure', 'MonthlyCharges', 'TotalCharges']
columnas_cat = eje_x.select_dtypes(include=['object', 'string']).columns.to_list()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), columnas_numericas),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), columnas_cat)
    ]
)

pipeline_rf = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42,class_weight='balanced'))
])

'''
el parametro handle_unknown='ignore', funciona para el siguiente caso: 

imagina que te llega un nuevo dato que el modelo no conoce,  entonces el modelo se romperia al 
no saber como tratar ese dato.
por lo que este parametro rellena con 0 la informacion desconocida lo cual se debe tomar 
en cuenta ya que en cantidades grandes 
puede afectar la prediccion del modelo.

por otro ,lado, el parametro (class_weight='balanced') funciona de la siguiente manera:

Primero se asegura de balancear con la misma importancia todos los datos mediante una formula 
matematica esto lo bace por medio de ponderaciones, es decir, que castiga al modelo si se equivoca al 
predecir la variable con menos datos disponobles en la etapa de entrenamiento.

'''

x_train, x_test, y_train, y_test = train_test_split(eje_x, eje_y, test_size=0.2, random_state=42)

print("------------- buscando los mejores parametros ------------------")

#aca con la variable param_grid es para crear un diccionario con los parametros que se le van a pasar al modelo de 
# entrenamiento para que el modelo pruebe con esas combinaciones y encuentre la mejor combinacion de parametros para 
# el modelo de random forest.

param_grid = {
    'classifier__n_estimators': [50, 1000],
    'classifier__max_depth': [ 10],
    'classifier__min_samples_split': [2, 100]
}
'''
nota: si min_samples_split es mayor que el numero de muestras es un error 
porque el random forest no hara nada





*************************************************************************************************

'''
'''
1.- classifier__n_estimators: es el numero de arboles 
como los argumentos son 50m y 100, le estamos diciendo que pruebe
con 50 arboles y luego con 100.

2.-'classifier__max_depth' = profundidad maxima del arbol, 
este argumento le dice cuantas preguntas se le deben hacer a los arboles.
ejplo

se tiene el valor de None = Dejarlos crecer libremente hasta que encuentran la respuesta
en otras palabras se le pide que haga las preguntas necesariaas

el valor de 20 le dice que haga solo 20 preguntas como maximo para encontrar la respuesta.
el valor de 10 le dice que haga 10 preguntas como maximo.

3.-'classifier__min_samples_split': minimo (min) de muestras (samples) para dividir (split)
nos dice el limite de datos que puede tener una pregunta.
ejplo si una pregunta tiene 5 datos entonces el arbol solo hara una nueva pregunta.
recordar que las preguntas son las ramas del arbol


'''

grid_search = GridSearchCV( #1.-GridSearchCV,  se crea esa variable grid_search y se le da esta funcion ya que es la que se encarga de
    # ejecutar las pruebas para encontrar a los mejores 
#parametros para el algoritmo de random forest.
    estimator=pipeline_rf, #2.-estimator: el valor de este parametro es el modelo que se va a entrenar
    param_grid=param_grid, #3.-param_grid = son las reglas que le  va a colocar al modelo de entrenamiento, por lo cual
    #no se duplica la variable ya que se le especifica que aca se debe ejecutar el diccionario creado anteriormente
    # con la misma variable.
    cv=3,  #se divide en numero de partes para para entrenarlos entre ellos ejplo
#entrena con 2 partes evalua con la 3 parte luego rota y vuelve hacer lo mismo con 
#partes diferentes.
    scoring = 'f1', #5.-scoring = el criterio de evaluacion.
    n_jobs=-1) #6.- n_jobs = le dice cuantos nucleos de la computadora se pueden usar para este entrenamiento.

grid_search.fit(x_train, y_train)  #la tipica del entrenamiento y guardarlo en grid_search-best_params_

#despues de realizar los entrenamientos, el objetivo grid_search se queda guardado con la mejor
#combinacion de los parametros que se le pasaron a traves de param_grid.

print(f"------------- mejores parametros encontrados {grid_search.best_params_} ------------------")

'''
1.-GridSearchCV, esta funcion es la que se encarga de ejecutar las pruebas para encontrar a los mejores 
parametros para el algoritmo de random forest.




4.-cv = es el numero de veces que va a entrenar al modelo.
en este caso el valor de 3 indica que que se parte del modelo en 3 partes para entrenarlos entre ellos ejplo
entrena con 2 partes evalua con la 3 parte luego rota y vuelve hacer lo mismo con 
partes diferentes.



ejplo, por defecto se usa "accuracy" pero para datos desbalanceados como con los que se
esta trabajando esta medida miente, por lo que 'f1' es la mejor opcion ya que es un eqiuilibrio entre encontrar 
todos los casos positivos y no cometer falsas alarmas.



en este caso -1, indica que use todos los nucleos disponibles.
en la vida real si hay que especificar los nucleos que se pueden usar porque existen
equipos de hasta 100 nucleos y no se pueden usar todos, hay un limite
ejplo
si el equipo tiene 8 nucleos entonces entrenara 8 nucleos en paralelo. un modelo por nucleo.

************************************************************************************************

grid_search.fit(x_train, y_train)

debemos recordar lo siguiente:

2 opciones de arboles (50,100)
3 opciones de profundidad (None, 10, 20)
2 opciones de muestras para dividir (se usa split) (2,5)

por lo que se tiene un total de combinaciones unicas de 2*3*2 =12 posibles combinaciones.

dado que cv=3, cada combinacion se entrena 3 veces

por lo que el numero de entrenamientos es igual a 12*3=36 



basicamente da esta respuesta: "de todas las combinaciones que probe esta es la mejor que
fue evaluada en el F1-score"
'''

best_model = grid_search.best_estimator_
y_pred = best_model.predict(x_test)

print("\n------------- reporte de rendimiento ------------------")
print(classification_report(y_test, y_pred))











#****************************************a partir de aca se cambia los cods






from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Predicciones
y_pred = best_model.predict(x_test)

# Matriz
matrix_confusion = confusion_matrix(y_test, y_pred)

# Graficar con estilo seaborn
fig, ax = plt.subplots(figsize=(6,5))

sns.heatmap(
    matrix_confusion,
    annot=True,
    fmt='d',
    cmap='rocket',
    cbar=True,
    xticklabels=['Pred: se queda', 'Pred: se va'],
    yticklabels=['Real: se queda', 'Real: se va'],
    ax=ax
)

plt.xlabel("Predicción")
plt.ylabel("Valor Real")
plt.title("Matriz de Confusión")
plt.show() 


























fig,ax = plt.subplots(figsize=(8,6))

ConfusionMatrixDisplay.from_estimator(best_model, x_test, y_test, display_labels=['se queda  (0)', 'se va (1)'],
                                       cmap='rocket', ax=ax)
plt.title('Matriz de Confusión - Random Forest')
plt.show() 

'''
lam salida de classification report es la siguiente :

------------- buscando los mejores parametros ------------------
------------- mejores parametros encontrados {'classifier__max_depth': 10, 'classifier__min_samples_split': 2, 'classifier__n_estimators': 100} ------------------

------------- reporte de rendimiento ------------------
              precision    recall  f1-score   support

           0       0.87      0.78      0.82      1033
           1       0.53      0.69      0.60       374

    accuracy                           0.76      1407
   macro avg       0.70      0.73      0.71      1407
weighted avg       0.78      0.76      0.76      1407

presicion:

este parametro indica que tan confiable es el modelo (en este caso Random Forest) para
predecir que el cliente se queda (0) o se va (1) ejplo
predice un 87% (0) cuando un cliente se queda mientras que predice un 53% (1)
cuando un cliente se va.

Recall: es la capacidad del modelo para encontrar todos los casos positivos,  
es decir, cuantos valores acerto ejplo
para los clientes que se quedan acerto un 78%
si se tiene una muestra de 1033 clientes y acerto al 78%
de ellos por lo tanto logro predecir a 805 clientes.

mientras que para los clientes que se van acerto un 69% 
si se tienen 374 clientes, eso quiere decir que logro predecir la salida de 258 clientes.

F1-score es el promedio de las medidad de precision y recall


-------------------------------------------------------------------------------


fig (la figura): es el tamaño de la imagen o el marco donde estara la figura.

ax (los ejes -Axes-) es el dibujo (lineas)

confusionMatrixDisplay.from_estimator: esta funcion se encarga de crear la matriz de 
confusion a partir del modelo entrenado, los datos de prueba y las etiquetas verdaderas.

esta es una  manera mas sencilla de dibujar la matriz de confusion 
esto lo ofrece la libreria de Sckiti-learn
la descripcion de los parametros es la siguiente:

besto:mode: es el modelo que se usara para predecir

x_test, y_test = son los datos que usara la matriz para evaluar internamente la 
funcion que predice y luego la compara.

display_labels: son las etiquetas que se mostraran en la matriz de confusion, 
en este caso se le dio una descripcion a cada clase (se queda 0, se va 1)

cmap: es el mapa de colores que se usara para la matriz de confusion,

ax: es el marco donde se dibujara la matriz de confusion, en este caso se le dio
 un tamaño de 8x6 a la figura y se le asigno a los ejes (ax) para que se dibuje ahi.




'''








