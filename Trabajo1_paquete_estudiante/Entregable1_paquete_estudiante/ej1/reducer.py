#!/usr/bin/env python3
"""
reducer.py - Fase REDUCE del Ej1 (ventas totales por ciudad).

Hadoop garantiza que, para este reducer, las líneas llegan ORDENADAS
por clave (ciudad). Eso significa que todas las líneas de "Bogota"
llegan juntas y seguidas, luego todas las de "Cali", etc.

Gracias a ese orden, podemos ir sumando el monto mientras la ciudad
no cambie; en cuanto detectamos un cambio de ciudad, imprimimos el
total acumulado de la ciudad anterior y reiniciamos el contador.
"""
import sys

ciudad_actual = None   # ciudad que estamos acumulando en este momento
suma_actual = 0.0       # suma acumulada de esa ciudad

for linea in sys.stdin:
    linea = linea.strip()
    ciudad, monto = linea.split("\t")   # deshacer el par clave-valor del mapper
    monto = float(monto)

    if ciudad == ciudad_actual:
        # seguimos en la misma ciudad: solo sumamos
        suma_actual += monto
    else:
        # cambió de ciudad: primero imprimimos el total de la anterior
        # (excepto la primera vez, cuando ciudad_actual todavía es None)
        if ciudad_actual is not None:
            print(f"{ciudad_actual}\t{suma_actual:.2f}")

        # empezamos a acumular la nueva ciudad
        ciudad_actual = ciudad
        suma_actual = monto

# al salir del for ya no hay más líneas, pero todavía no imprimimos
# el total de la ÚLTIMA ciudad que quedó acumulada; lo hacemos aquí
if ciudad_actual is not None:
    print(f"{ciudad_actual}\t{suma_actual:.2f}")