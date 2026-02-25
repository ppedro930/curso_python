import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

import matplotlib.pyplot as plt

df = pd.read_csv('Telco-Customer-Churn.csv')

print("--- informacion original datos por default ---")
print(df.info())

print("\n--- Primeros valores de TotalCharges (antes de la conversion) ---")
print(df['TotalCharges'].head())

'''luego hay que convertirlos a float ya que aparecen como cadena string y asi no va a reconocer los datos'''

#convertir de str a numerico con pandas
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

print("\n--- despues de la conversion ---")
print(df['TotalCharges'].head())

nulos = df['TotalCharges'].isnull().sum()
print(f"\n--- Valores nulos encontrados en TotalCharges son: {nulos} ---")

df = df.dropna(subset=['TotalCharges'])

print(f"\n--- Nuevos valores nulos en TotalCharges son: {df['TotalCharges'].dtype} ---")
print(f"\n--- datos nulos despues de la eliminacion es: {df['TotalCharges'].isnull().sum()} ---")


'''ya teniendo estos datos ya convertidos ahora sedefinen las variables
en este caso x se le define la variable del dataframe MonthlyCharges en vertical y en 
la letra y TotalCharges en horizontal para que lo grafique'''

X_multi = df[['MonthlyCharges', 'tenure']]
y_multi = df['TotalCharges'] 

'''ahora se definen la division de los datos en x y la letra y especificando 2 variables para cada uno
 obviamente una con train y la otra como test como parte de la prueba a realizar'''

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42) 

X_train, X_test, y_train, y_test = train_test_split(X_multi, y_multi, test_size=0.1, random_state=42)

#ahora con la funcion train_test_split se colocan
# las variables de cada campo del dataframe 
# especificando que el 0.8 es equivalente al 80% para pruebas
# y El otro 80% se usa para entrenamiento

# random_state = 42
# Es la semilla aleatoria que controla cómo se mezclan los datos. es decir, 
# que garantiza resultados reproducibles

modelo_prediccion_1 = LinearRegression()
'''
LinearRegression es un modelo de machine learning de regresión 
que sirve para predecir valores numéricos continuos, es decir que puede predecir ventas
el precio de una casa, salarios etc
'''

modelo_prediccion_1.fit(X_train, y_train)

'''ahora Qué hace .fit()? es un metodo que entrena el modelo:

este analiza X_train ( que son las variables de entrada)

luego lo compara con y_train (valor real que debería predecir)

todo esto en base a la formula y = mx + b'''


prediccion_1= modelo_prediccion_1.predict(X_test)

'''ahora lo que hace .predict() : este usa el modelo ya entrenado para hacer predicciones 
Toma datos nuevos (X_test) y calcula los valores que el modelo cree que son los correctos. (es decir que 
aun asi puede equivocarse, pero trata de ser lo mas preciso posible)'''

error = mean_absolute_error(y_test, prediccion_1)

''' mean_absolute_error es una métrica para evaluar qué tan bueno es el modelo de machine learning.
mide qué tan lejos se equivoca tu modelo en promedio, sin importar si el error es positivo o negativo.
es decir que compara valores reales con los valores predichos por el modelo 
calculandolo sobre la formula MAE=n1∑|y_real-y_predicho|'''

print("\n--- Resultado de la prediccion 1  ---")
print(f"error promedio (MAE): ${error:.2f}")


print(f"interpretacion: en promedio, el modelo se equivoca por aproximadamente ${error:.2f} al predecir TotalCharges basado en MonthlyCharges.")


'''el {error:.2f} es formato de salida, solo se usa. para mostrar un número con solo 2 decimales.'''

print(f": {modelo_prediccion_1.coef_[0]} mas")

'''modelo_prediccion_1 es el modelo entrenado con linearRegression 
y .coef_ es un atributo del modelo que guarda los pesos (coeficientes) 
aprendidos durante el entrenamiento.'''

comparativa = pd.DataFrame({
    'Valor real': y_test,
    'Valor prediccion': prediccion_1,
    'Error': y_test - prediccion_1

})

'''pd.DataFrame lo que hace es crear un DataFrame de pandas con 3 columnas.
las cuales se especifican con valor real prediccion y error 

'Valor real': y_test
Son los valores verdaderos
Lo que realmente pasó en los datos

'Valor prediccion': prediccion_1
Son los valores que predijo el modelo
La salida del algoritmo

'Error': y_test - prediccion_1
Es la diferencia entre lo real y lo predicho'''

x_monthly = df[['MonthlyCharges', 'tenure']] # era esteeeeee
y_1 = df['TotalCharges']

''' nuevamente especificamos los campos tal cual en x y letra y pero
se esta intentando explicar el TotalCharges solo 
a partir del cargo mensual, cuando en realidad:

TotalCharges ≈ MonthlyCharges x tiempo (tenure)

Eso ya nos dice algo importante: falta una variable clave, así que el error no puede ser pequeño'''

x_monthly_train, x_monthly_test, y_1_train, y_1_test = train_test_split(x_monthly, y_1, test_size=0.1, random_state=42)


#ahora con la funcion train_test_split se colocan
# las variables de cada campo del dataframe del monthly en este caso
# especificando que el 0.8 es equivalente al 80% para pruebas
# y El otro 80% se usa para entrenamiento

# random_state = 42
# Es la semilla aleatoria que controla cómo se mezclan los datos. es decir, 
# que garantiza resultados reproducibles

modelo_monthly = LinearRegression()

'''
aca se usa LinearRegression para predecir valores numéricos continuos con 
la variable de entrada MonthlyCharges y la variable de salida TotalCharges, como se menciono antes
'''

modelo_monthly.fit(x_monthly_train, y_1_train)

'''ahora Qué hace .fit()? es un metodo que entrena el modelo:

este analiza x_monthly_train ( que son las variables de entrada)

luego lo compara con y_1_train (valor real que debería predecir)

todo esto en base a la formula y = mx + b'''

prediccion_2 = modelo_monthly.predict(x_monthly_test)
error_monthly = mean_absolute_error(y_1_test, prediccion_2)

'''prediccion_2 es:

“Lo que el modelo piensa que debería ser el TotalCharges para esos clientes”
pero No es real, es una estimación.
y se compara con y_1_test Porque:

y_1_test → valor real

prediccion_2 → valor predicho'''

comparativa_monthly = pd.DataFrame({

    'Real': y_1_test,
    'Prediccion': prediccion_2,
    'Error': y_1_test - prediccion_2

})

'''comparativa_monthly = tabla de comparación
Une valores reales vs predichos
Calcula el error por registro
Es la base de tu análisis del modelo'''

plt.figure(figsize=(10, 6))

'''plt.figure(figsize=(10, 6)) = solo muestra cómo se ve la gráfica. 10 pulgadas de ancho y 6 pulgadas de alto.'''

plt.scatter(prediccion_2, comparativa_monthly['Error'], alpha=0.5)

'''en general
plt.scatter Crea un gráfico de puntos donde:
Cada punto representa una observación
Sirve para ver la relación entre dos variables (si hay patrón, tendencia, ruido, etc.)
alpha=0.5
Controla la transparencia de los puntos
Va de 0 (invisible) a 1 (opaco)
0.5 es ideal cuando hay muchos puntos superpuestos'''

#subplot para que se muestren las 3 en una solaaaaaaaaaaaaaa rectas agrupaciones y gerupos de redes neuronales sencillas

plt.axhline(y=0, color='red', linestyle='--')

'''este comando crea la linea hrizontal en y=0, con color rojo y estilo de linea discontinua'''

plt.title('90% de datos de entrenamiento y 10% de validacion   ---- grafica 1')

'''plt.title Agrega un título al gráfico'''


plt.xlabel(f"Predicciones")

'''plt.xlabel Agrega una etiqueta al eje x'''


plt.ylabel('Error')

plt.xlim(0,5000)
plt.ylim(-5000,5000)

'''es el valor de 0 a 4000 que se le coloca conn el fin de no agrandar la grafica '''

'''plt.ylabel Agrega una etiqueta al eje y'''

plt.show()

'''plt.show() Muestra el gráfico en pantalla'''

print("\n--- analisis de los monthly charges ---")
print(comparativa_monthly.head())

''' comparativa_monthly.head() Muestra las primeras filas de la tabla comparativa_monthly'''











# ===== GRAFICA 80 / 20 ===== graficaaaaaaaaaaa 2
plt.figure(figsize=(10, 6))

plt.scatter(prediccion_2, comparativa_monthly['Error'], alpha=0.5)
plt.axhline(y=0, linestyle='--')

plt.title('80% entrenamiento / 20% validación   --- grafica 2')
plt.xlabel('Predicciones')
plt.ylabel('Error')

plt.xlim(0, 4000)
plt.ylim(-4000, 4000)

plt.show()

X_train_30, X_test_30, y_train_30, y_test_30 = train_test_split(
    x_monthly, y_1, test_size=0.3, random_state=42
)

modelo_30 = LinearRegression()
modelo_30.fit(X_train_30, y_train_30)

prediccion_30 = modelo_30.predict(X_test_30)

comparativa_30 = pd.DataFrame({
    'Real': y_test_30,
    'Prediccion': prediccion_30,
    'Error': y_test_30 - prediccion_30
})






# ===== GRAFICA 70 / 30 ===== graficaaaaaaaaaaaaaaa 3
plt.figure(figsize=(10, 6))

plt.scatter(prediccion_30, comparativa_30['Error'], alpha=0.5)
plt.axhline(y=0, linestyle='--')

plt.title('70% entrenamiento / 30% validación --- grafica 3' )
plt.xlabel('Predicciones')
plt.ylabel('Error')

plt.xlim(0, 4000)
plt.ylim(-4000, 4000)

plt.show()





