#!/usr/bin/env bash
# ============================================================
# Trabajo 1 - Ej1: Ventas totales por ciudad
# Automatiza todo el ciclo: copiar archivos, subir a HDFS,
# lanzar el job de MapReduce y mostrar el resultado.
#
# Requisito: el clúster de 4 servicios (namenode, datanode,
# resourcemanager, nodemanager) debe estar arriba
# (docker compose up -d en la carpeta donde está el docker-compose.yml).
#
# Se corre parado DENTRO de la carpeta ej1/, junto a mapper.py y reducer.py.
# ============================================================
set -e   # si cualquier comando falla, el script se detiene (no sigue a ciegas)

echo "==> 1. Copiando datos y scripts al contenedor namenode..."
# docker cp copia archivos de tu máquina hacia DENTRO de un contenedor.
# Aquí van: el csv (que está un nivel arriba, en datos/) y los dos scripts.
docker cp ../datos/transacciones.csv namenode:/tmp/transacciones.csv
docker cp mapper.py                  namenode:/tmp/mapper_ej1.py
docker cp reducer.py                 namenode:/tmp/reducer_ej1.py

echo "==> 2. Subiendo el csv a HDFS..."
# -mkdir -p crea la carpeta de entrada en HDFS (no en el disco normal)
docker exec namenode hdfs dfs -mkdir -p /ej1/entrada
# -put -f sube el archivo del contenedor (/tmp/...) a HDFS; -f sobreescribe si ya existía
docker exec namenode hdfs dfs -put -f /tmp/transacciones.csv /ej1/entrada/
# si la carpeta de salida ya existe de una corrida anterior, Hadoop falla al lanzar
# el job (no sobreescribe solo), así que la borramos primero por si acaso
docker exec namenode hdfs dfs -rm -r -f /ej1/salida

echo "==> 3. Localizando el JAR de Hadoop Streaming..."
# el jar de Hadoop Streaming es el programa "genérico" que sabe cómo tomar
# nuestros scripts de Python y ejecutarlos como mapper/reducer dentro de Hadoop
STREAMING_JAR=$(docker exec namenode bash -c 'ls /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar' | tr -d '\r')
echo "    JAR: $STREAMING_JAR"

echo "==> 4. Lanzando el job de MapReduce..."
docker exec namenode hadoop jar "$STREAMING_JAR" \
  -files /tmp/mapper_ej1.py,/tmp/reducer_ej1.py \
  -mapper "python3 mapper_ej1.py" \
  -reducer "python3 reducer_ej1.py" \
  -input /ej1/entrada/transacciones.csv \
  -output /ej1/salida

echo ""
echo "==> 5. Resultado (ventas totales por ciudad):"
# -cat imprime el contenido del archivo de salida que dejó el reducer en HDFS
docker exec namenode hdfs dfs -cat /ej1/salida/part-00000

echo ""
echo "============================================================"
echo " Job terminado. Ve el detalle del job en YARN:"
echo "   http://localhost:8088   <-- toma la captura aqui para el informe"
echo "============================================================"