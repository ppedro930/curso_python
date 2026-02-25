import pandas as pd


sales_superstore = pd.read_csv("Superstore Sales Dataset.csv")

solo_ventas = sales_superstore[['Sales', 'City', 'Customer Name']]

ventas_altas = solo_ventas['Sales'] > 500


print(ventas_altas)

print("*" * 70)


ventas_altas_filtradas = solo_ventas.loc[ventas_altas]

print(ventas_altas_filtradas)

print("-" * 70)

#la siguiente muestra aquellos clientes con ventas mayores a 500

print(solo_ventas.loc[ventas_altas, 'Customer Name'])

print("-" * 70)

ventas_altas_loc =solo_ventas.loc[solo_ventas['Sales'] > 500, ['Customer Name']]

print(ventas_altas_loc)

solo_ventas.loc[(solo_ventas['Sales'] >=500) & (solo_ventas['City'] == 'Los Angeles'), ['Customer Name', 'City', 'Sales']]

ventas_cliente = solo_ventas.loc[(solo_ventas['Sales'] >=500) & (solo_ventas['Customer Name'] == 'Sylvia Foulston')]

print("*" * 70)

print(ventas_cliente)

ventas_cliente_filtro = solo_ventas.loc[
    (solo_ventas['Sales'] < 500) &
    (solo_ventas['Customer Name'] == 'Brosina Hoffman')
]
print("*" * 70)

print(ventas_cliente_filtro)

*********************************************

df = pd.DataFrame({
    'Category': ['Furniture', 'Furniture', 'Technology'],
    'State': ['Kentucky', 'California', 'Kentucky'],
    'Sales': [600, 300, 800]
})

resultado = df.loc[
    (df['Category'] == 'Furniture') &
    (df['State'] == 'Kentucky') &
    (df['Sales'] > 500)
]

print(resultado)


