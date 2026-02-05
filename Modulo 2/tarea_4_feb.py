import pandas as pd

# Crear un dataframe de ejemplo de 15 filas y 5 columnas
data = {
    "A": range(1, 16),
    "B": range(101, 116),
    "C": range(201, 216),
    "D": range(301, 316),
    "E": range(401, 416)
}

df = pd.DataFrame(data)
print("DataFrame original:")
print(df)



# Slices de renglones y columnas
slice1 = df.loc[0:2, ["A", "B", "C"]]   # primeros 3 renglones
slice2 = df.loc[4:6, ["A", "B", "C"]]   # renglones enmedio
slice3 = df.loc[-4:, ["A", "B", "C"]]   # últimos 4 renglones

# Combinar todos los slices
result = pd.concat([slice1, slice2, slice3])
print("10 renglones de 3 columnas:")
print(result)





# Sin .at
valor1 = slice1["B"].iloc[0]
print("Valor sin .at:", valor1)

# Con .at
valor2 = slice1.at[0, "B"]
print("Valor con .at:", valor2)



