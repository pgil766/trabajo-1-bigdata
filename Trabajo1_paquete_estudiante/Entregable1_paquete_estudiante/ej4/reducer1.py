#!/usr/bin/env python3
"""
reducer1.py - Fase REDUCE del JOB 1 de Ej4 (gasto por cliente y categoria).

Hadoop entrega las lineas ordenadas por la clave compuesta "cliente,categoria",
asi que todas las compras de un mismo cliente en una misma categoria llegan
juntas. Sumamos el monto mientras la clave no cambie, igual que en Ej1, y al
final emitimos "cliente,categoria<TAB>suma".

Esta salida (cliente,categoria -> suma) es la ENTRADA del job 2: representa
el gasto total de cada cliente en cada categoria, pero todavia no sabemos
cual es la categoria ganadora de cada cliente -eso lo decide el job 2, que
compara entre categorias de un mismo cliente-.
"""
import sys

clave_actual = None
suma_actual = 0.0

for linea in sys.stdin:
    linea = linea.strip()
    clave, monto = linea.split("\t")
    monto = float(monto)

    if clave == clave_actual:
        suma_actual += monto
    else:
        if clave_actual is not None:
            print(f"{clave_actual}\t{suma_actual:.2f}")

        clave_actual = clave
        suma_actual = monto

if clave_actual is not None:
    print(f"{clave_actual}\t{suma_actual:.2f}")
