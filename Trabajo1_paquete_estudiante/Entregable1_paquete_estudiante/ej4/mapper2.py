#!/usr/bin/env python3
"""
mapper2.py - Fase MAP del JOB 2 de Ej4 (categoria top por cliente).

La entrada de este mapper NO es el csv original, sino la SALIDA del job 1:
lineas "cliente,categoria<TAB>suma". Para que el job 2 pueda comparar las
categorias DE UN MISMO CLIENTE entre si, necesitamos reagrupar por cliente
solamente. Este mapper reordena cada linea: separa la clave compuesta en
cliente y categoria, y emite "cliente<TAB>categoria,suma" (ahora la clave
para el shuffle es solo el cliente).
"""
import sys

for linea in sys.stdin:
    linea = linea.strip()

    if not linea:
        continue

    clave, suma = linea.split("\t")       # clave = "cliente,categoria"
    cliente, categoria = clave.split(",")

    # nueva clave = solo el cliente; valor = "categoria,suma"
    print(f"{cliente}\t{categoria},{suma}")
