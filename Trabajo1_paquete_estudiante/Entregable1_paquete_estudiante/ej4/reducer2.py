#!/usr/bin/env python3
"""
reducer2.py - Fase REDUCE del JOB 2 de Ej4 (categoria top por cliente).

Hadoop entrega las lineas ordenadas por cliente, asi que todas las
categorias de un mismo cliente llegan juntas (aunque el ORDEN entre
categorias de un mismo cliente no esta garantizado). Mientras el cliente
no cambie, vamos comparando cada categoria contra la mejor vista hasta
el momento y nos quedamos con la de mayor suma. Cuando cambia de cliente,
imprimimos la categoria ganadora del cliente anterior.
"""
import sys

cliente_actual = None
mejor_categoria = None
mejor_suma = None

for linea in sys.stdin:
    linea = linea.strip()
    cliente, valor = linea.split("\t")
    categoria, suma = valor.split(",")
    suma = float(suma)

    if cliente == cliente_actual:
        if suma > mejor_suma:
            mejor_categoria = categoria
            mejor_suma = suma
    else:
        if cliente_actual is not None:
            print(f"{cliente_actual}\t{mejor_categoria},{mejor_suma:.2f}")

        cliente_actual = cliente
        mejor_categoria = categoria
        mejor_suma = suma

# imprimir la categoria ganadora del ultimo cliente acumulado
if cliente_actual is not None:
    print(f"{cliente_actual}\t{mejor_categoria},{mejor_suma:.2f}")
