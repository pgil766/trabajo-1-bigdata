#!/usr/bin/env bash
# ============================================================
# Trabajo 1 - Ej2: Ticket promedio por categoria
# Automatiza todo el ciclo: copiar archivos, subir a HDFS,
# lanzar el job de MapReduce y mostrar el resultado.
#
# Requisito: el cluster de 4 servicios (namenode, datanode,
# resourcemanager, nodemanager) debe estar arriba
# (docker compose up -d en la carpeta donde esta el docker-compose.yml).
#
# Se corre parado DENTRO de la carpeta ej2/, junto a mapper.py y reducer.py.
# ============================================================
set -e   # si cualquier comando falla, el script se detiene (no sigue a ciegas)

echo "==> 1. Copiando datos y scripts al contenedor namenode..."
docker cp ../datos/transacciones.csv namenode:/tmp/transacciones.csv
docker cp mapper.py                  namenode:/tmp/mapper_ej2.py
docker cp reducer.py                 namenode:/tmp/reducer_ej2.py

echo "==> 2. Subiendo el csv a HDFS..."
docker exec namenode hdfs dfs -mkdir -p /ej2/entrada
docker exec namenode hdfs dfs -put -f /tmp/transacciones.csv /ej2/entrada/
# si la carpeta de salida ya existe de una corrida anterior, Hadoop falla al lanzar
# el job (no sobreescribe solo), asi que la borramos primero por si acaso
docker exec namenode hdfs dfs -rm -r -f /ej2/salida

echo "==> 3. Localizando el JAR de Hadoop Streaming..."
STREAMING_JAR=$(docker exec namenode bash -c 'ls /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar' | tr -d '\r')
echo "    JAR: $STREAMING_JAR"

echo "==> 4. Lanzando el job de MapReduce..."
docker exec namenode hadoop jar "$STREAMING_JAR" \
  -files /tmp/mapper_ej2.py,/tmp/reducer_ej2.py \
  -mapper "python3 mapper_ej2.py" \
  -reducer "python3 reducer_ej2.py" \
  -input /ej2/entrada/transacciones.csv \
  -output /ej2/salida

echo ""
echo "==> 5. Resultado (ticket promedio por categoria):"
docker exec namenode hdfs dfs -cat /ej2/salida/part-00000

echo ""
echo "============================================================"
echo " Job terminado. Ve el detalle del job en YARN:"
echo "   http://localhost:8088   <-- toma la captura aqui para el informe"
echo "============================================================"
