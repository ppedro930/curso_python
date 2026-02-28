
historial_bancario = ( # paso 1 se crean los registros llevando el orden de id transaccion...
    ("transaccion1", "09:15", "192.168.1.10", "DEPOSITO", 15000.00), #se crean en tuplas
    ("transaccion2", "11:30", "192.168.1.15", "RETIRO", 2500.00),
    ("transaccion3", "14:20", "10.0.0.5",   "DEPOSITO", 1200.50),
    ("transaccion4", "16:45", "172.16.0.8", "RETIRO", 7500.00)   # Retiro masivo > $5000
)

# Variables de inicialización para el Paso 2
balance_total = 0.0 # esto es para sumar y restar montos y retiros
transacciones_auditadas = () # Tupla vacía para almacenar los registros revisados

# Paso 2: Procesamiento y Desempaquetado "Ninja"
for alias_ciclo_historial_bancario in historial_bancario:
    
    # 1. dentro del ciclo se define cada registro con una variable 
    # colocando como metadatos la hora e ip (solo en el ciclo)
    id_tx, *metadatos, tipo, monto = alias_ciclo_historial_bancario
    #print(alias_ciclo_historial_bancario)
    
    # 2. Cálculo de Balance  condicionales para sumar y restar segun transaccion
    if tipo == "DEPOSITO": #si el tipo equivale al monto de deposito
        balance_total += monto # lo suma
    elif tipo == "RETIRO": # si el tipo equivale a retiro
        balance_total -= monto # lo resta..... peeeero
         
    # 3. Reto de Inmutabilidad (Lógica de auditoría)
    if tipo == "RETIRO" and monto > 5000: #si el retiro es mayor a 5000
        etiqueta_auditoria = (" ALERTA: Retiro masivo",) # las tuplas de un elemento se declaran con coma
    else:
        etiqueta_auditoria = (" Aprobada",) # o puede salir esto si se aprueba
        
    # Concatenación creando una nueva tupla en memoria (la original no se altera)
    tx_revisada = alias_ciclo_historial_bancario + etiqueta_auditoria
    
    # 4. Almacenamiento en la tupla maestra
    transacciones_auditadas += (tx_revisada,)


#  Paso 3: Generación de Reporte Formateado

# 1. Encabezado elegante
print("=" * 85)
print(f"{' REPORTE DE AUDITORÍA BANCARIA INMUTABLE ':^85}")
print("=" * 85)

# Nombres de las columnas alineados
print(f"{'ID':<7} | {'Hora':<7} | {'IP Origen':<15} | {'Tipo':<10} | {'Monto':<12} | {'Estado Auditoría'}")
print("-" * 85)

# 2 y 3. Iteración y Formato de Salida
for tx in transacciones_auditadas:
    # Desempaquetado estándar para imprimir
    id_tx, hora, ip, tipo, monto, estado = tx
    
    # f-strings con alineación y redondeo de decimales (:.2f)
    print(f"{id_tx:<7} | {hora:<7} | {ip:<15} | {tipo:<10} | ${monto:<11.2f} | {estado}")

    

print("-" * 85)

# 4. Balance Final
# Se utiliza el formato :,.2f para incluir comas en los miles y 2 decimales
print(f" BALANCE FINAL DE LA CUENTA: ${balance_total:,.2f}")
print("=" * 85)