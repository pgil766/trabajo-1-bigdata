#!/usr/bin/env python3
"""
reducer.py - Fase REDUCE del Ej3 (top-3 ciudades con mas ventas).

Para poder elegir el top-3 GLOBAL, este reducer necesita ver el total
acumulado de TODAS las ciudades a la vez antes de decidir cuales son
las 3 mayores. Por eso NO imprimimos nada al detectar un cambio de
clave (como en Ej1): en vez de eso, guardamos el total de cada ciudad
en un diccionario, y solo al final -cuando ya pasaron todas las lineas
por este reducer- ordenamos el diccionario completo y mostramos las 3
ciudades con mayor total.

Esto solo funciona si TODAS las ciudades llegan a este mismo reducer;
si Hadoop repartiera el trabajo entre varios reducers, cada uno veria
solo un subconjunto de ciudades y el top-3 podria salir incompleto o
incorrecto (ver la opcion -numReduceTasks 1 en ejecutar_ej3.sh).
"""
import sys

totales = {}  # ciudad -> suma acumulada

for linea in sys.stdin:
    linea = linea.strip()
    ciudad, monto = linea.split("\t")
    monto = float(monto)

    totales[ciudad] = totales.get(ciudad, 0.0) + monto

# ya vimos todas las ciudades: ordenar de mayor a menor y quedarnos con las 3 primeras
top3 = sorted(totales.items(), key=lambda par: par[1], reverse=True)[:3]

for ciudad, total in top3:
    print(f"{ciudad}\t{total:.2f}")
