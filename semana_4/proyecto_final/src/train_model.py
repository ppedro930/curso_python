import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt




    # RUTAS AUTOMÁTICAS DEL PROYECTO

def main():

    BASE_DIR = Path(__file__).resolve().parent.parent

    PROCESSED_PATH = BASE_DIR / "data" / "processed" #ruta para procesar archivos
    OUTPUT_PATH = BASE_DIR / "data" / "processed" #ruta para guardar archivos

    OUTPUT_PATH.mkdir(parents=True, exist_ok=True) #crea cluster si no existe



    # CARGAR DATA LIMPIA


    airbnb_file = PROCESSED_PATH / "airbnb_clean.csv" # archivo a encontrar solo se va a basar en ese archivo
    df = pd.read_csv(airbnb_file) # archivo a leer 



    # 1️⃣ REGRESIÓN → PREDECIR PRICE


    df_num = df.select_dtypes(include="number") 
    #se crea la variable con df_num anexando la variable del archivo df dandole una clase select_dtypes 
    #  selecionando los datatypes de todas las columnas que sean tipo numerico

    if "price" not in df_num.columns: #si price tipo numerico no esta en columns
        raise Exception("No existe columna numérica 'price'") #devuelve esto

    df_num = df_num.dropna(subset=["price"]).fillna(0) #variable que borra datos nulos 
    #en caso de que los encuentre en la columna price

    X = df_num.drop(columns=["price"]) #en el eje x se borra la columna price
    y = df_num["price"] #en y se mantiene price


    #la funcion train_test_split Divide los datos en entrenamiento (80%) y prueba (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X,              # variables predictoras (preguntas)
        y,              # variable objetivo (respuestas)
        test_size=0.2,  # 20% para pruebas
        random_state=42 # semilla para reproducibilidad
    )

    # X_train → preguntas para entrenar el modelo (80%)
    # y_train → respuestas correctas para entrenar el modelo (80%)

    # X_test → preguntas nuevas que el modelo nunca vio (20%)
    # y_test → respuestas reales para evaluar qué tan bien predice

    ###########################################################################

    # Crear el modelo de regresión lineal
    model = LinearRegression()

    # Entrenar el modelo con el 80% de los datos
    model.fit(X_train, y_train)

    # Hacer predicciones con el 20% de prueba
    pred = model.predict(X_test)

    # Evaluar qué tan bien predijo 
    mae = mean_absolute_error(y_test, pred)  # error promedio absoluto
    r2 = r2_score(y_test, pred)              # qué tanto explica el modelo


    # GUARDAR MÉTRICAS EN /data/clusters/

    metrics_file = OUTPUT_PATH / "model_metrics.txt" 
    #los resultados se guardan en el archivo model_metrics.txt

    with open(metrics_file, "w", encoding="utf-8") as f:
    #la funcion open sirve para traer el archivo 
    #con la variable metrics_file para escribirlo o modificarlo con "w".
        f.write(f"MAE: {mae:.4f}\n") #escribe el resultado de mae con 4 decimales y tipo float
        f.write(f"R2: {r2:.4f}\n") #escribe el resultado de r2 con 4 decimales y tipo float



    # 2️⃣ CLUSTERING KMEANS → 3 CLUSTERS


    cluster_df = df.select_dtypes(include="number").fillna(0)
    #se seleccionan columnas de tipo numerico y quitan las demas
    #fillna remplaza valores vacios por 0

    if cluster_df.shape[1] < 2: #si shape cuenta menos de 2 columnas... da la excepcion
        raise Exception("No hay suficientes columnas numéricas para clustering")

    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    #actua el algoritmo de kmeans agrupando con 
    # n_clusters= 3 grupos de cluster= Económico, Turístico, Oportunidad
    # random_state=42 la semilla aleatoria pero siempre da el mismo resultado con 42
    #si cambia el numero dara tambien el mismo resultado pero tradicionalmente se usa el 42
    # n_init=10 intenta el algoritmo 10 veces con diferentes centros iniciales
    #y se queda con el mejor resultado.

    df["cluster"] = kmeans.fit_predict(cluster_df)
    #df["cluster"] se crea esa nueva columna luego con
    # la variable kmeans se usa la funcion .fit_predict 
    # para entrena el modelo y asigna un grupo con (cluster_df) a cada fila,
    # aca se Asigna la etiqueta del cluster df["cluster"] (0, 1, 2) como una nueva columna en tu DataFrame (csv)



    # 3️⃣ GUARDAR CSV CON CLUSTERS


    clustered_file = OUTPUT_PATH / "airbnb_clustered.csv"
    #guarda el archivo ya procesado en su ruta indicada especificando nombrey formato

    df.to_csv(clustered_file, index=False, encoding="utf-8-sig")

    # df = el DataFrame actual (ya con columnas de cluster, price limpios etc.)
    #.to_csv(...) funcion de pandas para guardar csv
    #index=False... Por defecto, pandas guarda una columna extra al principio con los 
    # números de fila (0, 1, 2...). Al poner False, se evita que esa columna innecesaria se guarde en tu archivo.
    ############################################################
    # 4️⃣ GUARDAR GRÁFICA AUTOMÁTICA



    cols = ["price","availability_365"]
    # se toman las 2 primeras columnas numericas para hacer la representacion grafica
    plt.figure(figsize=(10,6)) # Definir el tamaño de la figura para que sea legible

    plt.scatter( #grafico de dispersion
        cluster_df[cols[0]], # eje x (price)
        cluster_df[cols[1]], # eje y (availability_365)
        c=df["cluster"],    # color del cluster
        cmap='viridis',     # Paleta de colores 
        alpha=0.4,          # Transparencia para ver puntos encimados
        edgecolors='w'      # Borde blanco en los puntos para separarlos
    )

    plt.xlabel(cols[0]) # etiqueta x
    plt.ylabel(cols[1]) # etiqueta y
    plt.title('analisis de Clusters: precio vs disponibilidad por cada 365 dias')

    # 4. Agregar una barra de colores para saber qué cluster es cuál
    plt.colorbar(label='Cluster ID')

    # 5. Mostrar la cuadrícula para facilitar la lectura de valores
    plt.grid(True, linestyle='--', alpha=0.5)


    plot_file = OUTPUT_PATH / "cluster_analysis.png" #se asigna ruta y nombre donde se va a guardar

    plt.savefig(plot_file) #  se guarda en la ruta asignada con su nombre

    plt.close() #finaliza la ejecucion

if __name__ == "__main__":
    main()