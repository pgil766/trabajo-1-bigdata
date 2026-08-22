#!/usr/bin/env python3
"""
mapper.py - Fase MAP del Ej1 (ventas totales por ciudad).

Lee el csv de transacciones línea por línea desde stdin (entrada estándar).
Por cada fila válida, extrae la ciudad y el monto, y emite un par
clave-valor: "ciudad<TAB>monto".

Hadoop se encarga de juntar (en el shuffle/sort) todas las líneas que
tengan la misma clave (ciudad) antes de que lleguen al reducer.
"""
import sys

for linea in sys.stdin:
    linea = linea.strip()

    # ignorar líneas vacías (por si acaso)
    if not linea:
        continue

    # el csv separa las columnas por comas:
    # id_tx, id_cliente, fecha, ciudad, categoria, monto
    campos = linea.split(",")

    # saltar la fila de cabecera del csv (donde va el texto "id_tx")
    if campos[0] == "id_tx":
        continue

    ciudad = campos[3]   # posición 3 = columna "ciudad"
    monto = campos[5]    # posición 5 = columna "monto"

    # convertir el monto a número; si algo viene mal formado, se descarta la fila
    try:
        monto = float(monto)
    except ValueError:
        continue

    # emitir clave y valor separados por TAB (formato que Hadoop Streaming espera)
    print(f"{ciudad}\t{monto}")