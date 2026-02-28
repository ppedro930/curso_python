# 🧙‍♂️ 1. Inicialización de Entidades

heroe = {
    "nombre": "Guardián del Código",
    "hp": 120,
    "pociones": 3,
    "danio_base": 25
}

enemigo = {
    "nombre": "Dragón de los Datos Nulos",
    "hp": 150,
    "danio_base": 20
}

# 🔄 2. Ciclo de Combate
turno = 1

while heroe["hp"] > 0 and enemigo["hp"] > 0:

    print(f"\n🔥 --- TURNO {turno} --- 🔥")

    # 1️⃣ Ataque del Héroe
    enemigo["hp"] -= heroe["danio_base"]
    print(f"⚔ {heroe['nombre']} ataca e inflige {heroe['danio_base']} de daño.")
    print(f"🐉 Vida del {enemigo['nombre']}: {max(enemigo['hp'], 0)} HP")

    # 2️⃣ Verificación de Victoria
    if enemigo["hp"] <= 0:
        print(f"\n🏆 ¡El {enemigo['nombre']} ha sido derrotado!")
        print("✨ La Caverna Prohibida ha sido liberada.")
        break

    # 3️⃣ Contraataque del Enemigo
    heroe["hp"] -= enemigo["danio_base"]
    print(f"🔥 {enemigo['nombre']} contraataca e inflige {enemigo['danio_base']} de daño.")
    print(f"🧙‍♂️ Vida del {heroe['nombre']}: {max(heroe['hp'], 0)} HP")

    # 4️⃣ Sistema de Curación Automática
    if heroe["hp"] <= 40 and heroe["pociones"] > 0:
        heroe["pociones"] -= 1
        heroe["hp"] += 30
        print("🧪 ¡Poción utilizada automáticamente!")
        print(f"💚 {heroe['nombre']} recupera 30 HP.")
        print(f"🧴 Pociones restantes: {heroe['pociones']}")
        print(f"🧙‍♂️ Vida actual: {heroe['hp']} HP")

    # 5️⃣ Verificación de Derrota
    if heroe["hp"] <= 0:
        print(f"\n💀 {heroe['nombre']} ha caído en batalla...")
        print("🌑 El Dragón domina los Datos Nulos.")
        break

    turno += 1