original = [1,2,3]
#copia_falsa = original
#copia_falsa.append(100)
print(f"Original: {original}")

copia_real = original.copy()
copia_real.append(200)
print(f"Copia real: {copia_real} y Original: {original}")

copia_slice = original[:] # -> los : indican desde donde hasta donde se tomaran valores de la lista original
copia_slice.append(300)
print(f"Copia slice: {copia_slice} y Original: {original}")

