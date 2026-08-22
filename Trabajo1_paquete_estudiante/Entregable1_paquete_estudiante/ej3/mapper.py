#!/usr/bin/env python3
"""
mapper.py - Fase MAP del Ej3 (top-3 ciudades con mas ventas).

Es casi identico al mapper de Ej1: lee el csv linea por linea desde
stdin y emite "ciudad<TAB>monto". El truco de este ejercicio no esta
en el mapper sino en como se lanza el reducer (ver ejecutar_ej3.sh).
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

    ciudad = campos[3]
    monto = campos[5]

    try:
        monto = float(monto)
    except ValueError:
        continue

    print(f"{ciudad}\t{monto}")
