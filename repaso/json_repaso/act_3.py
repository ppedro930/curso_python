# ==========================================
# 🏢 PASO 1: Definición de Existencias
# ==========================================

inventario_almacen = {
    "laptops": 15,
    "ratones": 40,
    "teclados": 25
}

nuevo_embarque = {
    "laptops": 5,
    "ratones": 10,
    "monitores": 8   # producto nuevo
}

# ==========================================
# 🛡 PASO 2: Actualización Segura con .get()
# ==========================================

for producto, cantidad in nuevo_embarque.items():
    inventario_almacen[producto] = inventario_almacen.get(producto, 0) + cantidad


# ==========================================
# 🔗 PASO 3: Fusión de Precios (Operador | )
# ==========================================

precios_base = {
    "laptops": 15000,
    "ratones": 250,
    "teclados": 500,
    "monitores": 4000
}

actualizacion_precios = {
    "laptops": 15500,  # actualización
    "monitores": 4200  # actualización
}

# El de la derecha tiene prioridad
precios_finales = precios_base | actualizacion_precios


# ==========================================
# 💰 PASO 4: Análisis Financiero
# ==========================================

valor_financiero = {
    producto: inventario_almacen[producto] * precios_finales[producto]
    for producto in inventario_almacen
    if inventario_almacen[producto] * precios_finales[producto] > 1000
}


# ==========================================
# 📑 PASO 5: Salida Profesional
# ==========================================

print("\n📊 REPORTE DE ACTIVOS DE ALTO VALOR")
print("=" * 55)
print(f"{'Producto':<15}{'Stock':<10}{'Precio Unitario':<15}{'Valor Total':<15}")
print("=" * 55)

total_general = 0

for producto, valor in valor_financiero.items():
    stock = inventario_almacen[producto]
    precio = precios_finales[producto]
    total_general += valor

    print(f"{producto:<15}{stock:<10}{precio:<15,.2f}${valor:<15,.2f}")

print("=" * 55)
print(f"{'TOTAL GENERAL:':<40}${total_general:,.2f}")
print("=" * 55)