import pandas  as pd

sales_superstore = pd.read_csv("Superstore Sales Dataset.csv")

#print(sales_superstore.info())

#print(sales_superstore.describe())

#print(sales_superstore.describe(include=['object',"string"]))

solo_ventas = sales_superstore[['Sales', 'City', 'Customer Name']]

#print(solo_ventas.head())
#print(solo_ventas.tail())

#print(solo_ventas.describe(include=['object',"string"])) #cualitativa (estadisticas)
#print(solo_ventas.describe()) #cuantitativa (estadisticas)

#print(solo_ventas.loc[30]) #devuelve una serie como excel horizontal
#print(solo_ventas.loc[[30]]) #muestra vertical

#df_2 = pd.DataFrame([[1,2], [4,5], [7,8]],
#index=["cobra", "viper", "sidewinder"],
#columns=["max speed", "shield"]
#)

#print(df_2.loc["max_speed", "shield"]) 

print(sales_superstore.loc[330, 'Product Name'])

print(sales_superstore.loc[330, 'Customer Name'])


