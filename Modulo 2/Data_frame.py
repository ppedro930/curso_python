import pandas as pd

int_values = [1, 2, 3, 4, 5]

text_values = ["alfa", "beta", "gamma", "delta", "epsilon"]

float_values = [0.0, 0.25, 0.5, 0.75, 1.0]

df = pd.DataFrame({

"int_col": int_values,
"text_col": text_values,
"float_col": float_values

}
)

df_2 = pd.DataFrame([[1,2], [4,5], [7,8]],
index=["cobra", "viper", "sidewinder"],
columns=["max speed", "shield"]
)

sales_superstore = pd.read_csv("Superstore Sales Dataset.csv")

#print(f"DataFrame 1:\n{df}")
#print(f"DataFrame 2:\n{df_2}")
#print(f"Sales Superstore DataFrame:\n{sales_superstore.head()}")

numero_de_filas = 50
filas = sales_superstore.head(1)
filas_slice = sales_superstore[:numero_de_filas]

#print(f"Estas son las primeras {numero_de_filas} filas del DataFrame:\n{filas_slice}")

ultimas = sales_superstore.tail(10)
ultimas_slice = sales_superstore[-10:]
ultimas_slice_file = sales_superstore[10:]

print(f"Estas son las últimas 10 filas del DataFrame:\n{ultimas_slice_file}")

