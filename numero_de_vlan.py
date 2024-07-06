RANGO_NORMAL = range(1, 1006)
RANGO_EXTENDIDO = range(1006, 4095)

vlan = int(input("Ingrese el número de VLAN: "))

if vlan in RANGO_NORMAL:
    print(f"La VLAN {vlan} pertenece al rango normal.")
elif vlan in RANGO_EXTENDIDO:
    print(f"La VLAN {vlan} pertenece al rango extendido.")
else:
    print(f"La VLAN {vlan} no es válida.")