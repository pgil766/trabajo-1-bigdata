#!/usr/bin/env python3
"""
reducer.py - Fase REDUCE del Ej2 (ticket promedio por categoria).

Hadoop entrega las lineas ordenadas por clave (categoria), asi que todas
las lineas de "ropa" llegan juntas, luego todas las de "electronica", etc.

Para cada categoria acumulamos DOS cosas por separado: la suma de montos
y la cantidad de compras (el "1" que emitio el mapper junto al monto).
Cuando cambia la categoria, calculamos el promedio = suma / cantidad y lo
imprimimos; asi el reducer nunca pierde de vista entre cuantas compras
esta dividiendo.
"""
import sys

categoria_actual = None
suma_actual = 0.0
cantidad_actual = 0

for linea in sys.stdin:
    linea = linea.strip()
    categoria, valor = linea.split("\t")  # deshacer el par clave-valor
    monto_str, uno_str = valor.split(",")  # deshacer el valor compuesto "monto,1"
    monto = float(monto_str)
    uno = int(uno_str)

    if categoria == categoria_actual:
        suma_actual += monto
        cantidad_actual += uno
    else:
        if categoria_actual is not None:
            promedio = suma_actual / cantidad_actual
            print(f"{categoria_actual}\t{promedio:.2f}")

        categoria_actual = categoria
        suma_actual = monto
        cantidad_actual = uno

# imprimir el promedio de la ultima categoria acumulada
if categoria_actual is not None:
    promedio = suma_actual / cantidad_actual
    print(f"{categoria_actual}\t{promedio:.2f}")
