#!/usr/bin/env python3
"""
mapper.py - Fase MAP del Ej2 (ticket promedio por categoria).

Lee el csv de transacciones linea por linea desde stdin. Por cada fila
valida, extrae la categoria y el monto, y emite "categoria<TAB>monto,1".

El "1" es un contador: cada linea del csv representa UNA compra, asi que
emitir un 1 junto al monto le permite al reducer saber, ademas de la suma,
CUANTAS compras tuvo cada categoria (necesario para promediar: promedio =
suma / cantidad de compras). Si solo emitieramos el monto, el reducer podria
sumar pero nunca sabria entre cuanto dividir esa suma.
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

    categoria = campos[4]  # posicion 4 = columna "categoria"
    monto = campos[5]      # posicion 5 = columna "monto"

    try:
        monto = float(monto)
    except ValueError:
        continue

    # valor compuesto "monto,1": el 1 es el contador de esta compra
    print(f"{categoria}\t{monto},1")
