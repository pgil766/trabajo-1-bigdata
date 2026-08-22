#!/usr/bin/env python3
"""
mapper1.py - Fase MAP del JOB 1 de Ej4 (gasto por cliente y categoria).

Esta consulta ("categoria en la que mas gasta cada cliente") necesita dos
agrupaciones distintas: primero agrupar por (cliente, categoria) para saber
cuanto gasto cada cliente en cada categoria, y despues, entre esas
categorias, quedarse con la de mayor gasto por cliente. Un solo
map-reduce no alcanza porque agrupar por dos niveles distintos (primero
cliente+categoria, luego solo cliente) requiere dos shuffles/sorts
distintos de Hadoop.

Este mapper hace la PRIMERA agrupacion: lee el csv y emite una clave
COMPUESTA "cliente,categoria" junto con el monto de esa compra.
"""
import sys

for linea in sys.stdin:
    linea = linea.strip()

    if not linea:
        continue

    # id_tx, id_cliente, fecha, ciudad, categoria, monto
    campos = linea.split(",")

    if campos[0] == "id_tx":
        continue

    cliente = campos[1]
    categoria = campos[4]
    monto = campos[5]

    try:
        monto = float(monto)
    except ValueError:
        continue

    # clave compuesta "cliente,categoria": agrupa cada combinacion por separado
    print(f"{cliente},{categoria}\t{monto}")
