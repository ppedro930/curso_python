import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

import matplotlib.pyplot as plt

'''
train_test_split.

es un metodo "barajea los datos en 2 grupos separados.

el grupo de entrenamiento (Train): Este grupo usa el 80% de los datos para que el modelo 
aprenda la relacion matematica.

el grupo de prueba (test): este grupo Usa el 20% de los datos que el modelo NUNCA HA VISTO,
con el fin de evaluarlo.

LinearRegression.

Es la clase del algoritmo matematico, es decir 
la relacion que se esta buscando en este ejemplo

para que sirve? el trabajo de esta clase es encontrar la linea recta
que mejor se ajuste a los datos de entrenamiento (el 80% que se separo antes). intenta reducir 
al maximo la distancia 
entre los puntos reales y la linea que dibuja el algotritmo.
esta linea esta descrita por la siguiente ecuaciion:

y= mx + b

mean_absolute_error (MAE):

QUE ES? es una manera de calificar, es decir que es una metrica de evaluacion

para que sirve? dice en promedio que tanto se equivoco el modelo implementado.
calculando la diferencia absoluta entre lo que predijo el modelo y el valor real 
|valor_real - valor_modelo|

ejemplo: si el modelo predice que una casa cuesta $100 y en realidad cuesta $105 el error es de 5.
el MAE promedia TODOS ESOS ERRORES y por lo tanto. entre mas bajo
sea el numero que se obtiene del MAE, mejor exactitud tendra el modelo.

error absoluto promedio en español.
Mean absolute error en ingles.
'''
df = pd.read_csv('Telco-Customer-Churn.csv')

print("--- Estructura e informacion del dataset ---")
print(df.info())

print("\n--- Primeros valores de TotalCharges (antes de la conversion) ---")
print(df['TotalCharges'].head())

#convertir de str a numerico con pandas
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

print("\n--- despues de la conversion ---")
print(df['TotalCharges'].head())

#ultimo recurso en caso de no lograr inferir datos de manera correcta

nulos = df['TotalCharges'].isnull().sum()
print(f"\n--- Valores nulos encontrados en TotalCharges son: {nulos} ---")

df = df.dropna(subset=['TotalCharges'])

print(f"\n--- Nuevos valores nulos en TotalCharges son: {df['TotalCharges'].dtype} ---")
print(f"\n--- datos nulos despues de la eliminacion es: {df['TotalCharges'].isnull().sum()} ---")

X = df[['tenure']]
y = df['TotalCharges']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

'''
dado a que nuestro algoritmo de prediccion se basa en la regresion lineal entonces
X= las columnas x de entrada para el algoritmo
y= la columna objetivo, es decir los valores que el algoritmo intentara predecir.

test_size = 0.2 es como decirle al modelo "separa el 20% de las filas X para evaluar el modelo"
el otro 80% es para entrenar al modelo.

Normalmente se recomienda trabajar el 10% al 20% para datos de entrenamiento. (0.2 * 100 = 20)

random_state=42 su funcion es como ramdom.see(42) sirve para la reproducibilidad, 
del sistema. es decir que cada vez que se ejecute el codigo, se obtendra la misma separacion de datos.

la salida de la funcion:
la funcion devuelve 4 paquetes de datos, en este caso se encuadran las siguientes variables.
x_train: las entradas para que el modelo aprenda, (el 80% de los datos)
x_test: las entradas para que el modelo valide la informacion, (el 80% de los datos)
y_train: son las respuestas correctas para que el modelo tenga mejor exactitud (el 80% de los datos)
y_test: son las respuestas correctas de la evaluacion, normalmente se compara con la 
prediccion que hizo el modelo:

analogia del examen: (variables de entrenamiento)
X_train = los datos para estudiar el examen (80%)
X_test = los datos del examen, es decir las preguntas del examen (20%)
y_train= las respuestas correctas para estudiar el examen (80%)
y_test= las respuestas correctas del examen (20%)
'''
modelo_prediccion_1 = LinearRegression()
modelo_prediccion_1.fit(X_train, y_train)

prediccion_1= modelo_prediccion_1.predict(X_test)

'''
modelo_prediccion_1 = LinearRegression()

crea una instancia vacia. basicamente es como comprar un instrumento de medicion nuevo 
pero vacio

modelo_prediccion_1.fit(X_train, y_train)

este metodo busca que "el modelo" aprenda. se le pasan las entradas y las respuestas
- como lo hace? aplica el metodo de minimos cuadrados ordinarios,
buscando la linea recta (y = mx + b) que minimice el error de los puntos.


prediccion_1= modelo_prediccion_1.predict(X_test)

con este metodo se pone a prueba el modelo, es decir que el modelo toma los datos de X_test
aplica la formula matematica que encontro y arroja un resultado.
devuelve una lista con las predicciones que el
modelo cree que es la respuesta correcta

'''
error = mean_absolute_error(y_test, prediccion_1)

print("\n--- Resultado de la prediccion 1  ---")
print(f"error promedio (MAE): ${error:.2f}")
print(f"interpretacion: por cada mes extra el cliente paga aproximadamente")
print(f": {modelo_prediccion_1.coef_[0]} mas")

'''
error = mean_absolute_error(y_test, prediccion_1)

con este metodo se calcula el error mediante la formula |valor real - valor estimado|

los argumentos de la funcion es 
y_test: es el valor real

prediccion_1: es el valor que calculo el modelo (valor estimado)

lo que hace: toma la diferencia absoluta del error de cada uno de los clientes de prueba
y saca el promedio.

manera de interpretarlo:
salio 877.36, esto significa que el modelo en promedio se equivoca 877.36 lo cual 
indica que se su precio real es de 100, el modelo se puede equivocar 877.36 hacia arriba o hacia abajo

modelo_prediccion_1.coef_[0]

con este metodo se accede a la pendiente (m) de la ecuacion de la recta
y = mx + b

lo cual indica de manera matematica que cuando la tasa de cambio:

cuando cambia y (dinero) cuando aumenta x en una unidad.
el coeficiente tiene un valor en este ejercicio de 76.18, lo cual quiere decir que por cada mes que pasa 
la cuenta sube un total de 76.18 pesos.

porque [0]?
porque modelo.coef_ es una lista. como en este ejemplo
se usa una variable para decidir (Tenure) solo hay una oendiente que esta en la pocision 0 de la lista

sis e hubieran usado 2 variables, se tendria coef_[0] y coef_[1]

'''

comparativa = pd.DataFrame({
    'Valor real': y_test,
    'Valor prediccion': prediccion_1,
    'Error': y_test - prediccion_1

})

#print("\n--- comparativa entre valor real y valor prediccion ---")
#print(comparativa.head())

#plt.figure(figsize=(10, 6))

#plt.scatter(prediccion_1, comparativa['Error'], alpha=0.5)
#plt.axhline(y=0, color='red', linestyle='--')
#plt.title('Grafico de residuos. que tan feo es el error?')
#plt.xlabel('predicciones')
#plt.ylabel('Error')
#plt.show()


x_monthly = df[['MonthlyCharges']]
y_1 = df['TotalCharges']

x_monthly_train, x_monthly_test, y_1_train, y_1_test = train_test_split(x_monthly, y_1, test_size=0.2, random_state=42)

modelo_monthly = LinearRegression()
modelo_monthly.fit(x_monthly_train, y_1_train)

prediccion_2 = modelo_monthly.predict(x_monthly_test)
error_monthly = mean_absolute_error(y_1_test, prediccion_2)

comparativa_monthly = pd.DataFrame({

    'Real': y_1_test,
    'Prediccion': prediccion_2,
    'Error': y_1_test - prediccion_2

})

plt.figure(figsize=(10, 6))
plt.scatter(prediccion_2, comparativa_monthly['Error'], alpha=0.5)
plt.axhline(y=0, color='red', linestyle='--')
plt.title('Grafico de residuos para MonthlyCharges que tan feo es el error?')
plt.xlabel(f"Predicciones")
plt.ylabel('Error')
plt.show() #mientras mas sean las predicciones mas se va a notar el error, 
#es decir que si el modelo predice 1000, y el valor real es 500, el error es de 500, 
# lo cual es un error grande. pero si el modelo predice 550, y el valor real es 500, 
# el error es de 50, lo cual es un error pequeño. por lo tanto mientras mas se aleje 
# la prediccion del valor real, mas grande sera el error.
#pero si en la prediccion los resultados no se alejan de 0 entonces el error es pequeño, lo cual es bueno.

print("\n--- analisis de los monthly charges ---")
print(comparativa_monthly.head())
