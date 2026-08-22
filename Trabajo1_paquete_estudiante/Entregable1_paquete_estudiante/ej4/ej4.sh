#!/usr/bin/env bash
# ============================================================
# Trabajo 1 - Ej4: Categoria en la que mas gasta cada cliente
# (2 jobs de MapReduce ENCADENADOS: la salida del job 1 es la
# entrada del job 2).
#
# Requisito: el cluster de 4 servicios (namenode, datanode,
# resourcemanager, nodemanager) debe estar arriba
# (docker compose up -d en la carpeta donde esta el docker-compose.yml).
#
# Se corre parado DENTRO de la carpeta ej4/, junto a los 4 scripts .py.
# ============================================================
set -e   # si cualquier comando falla, el script se detiene (no sigue a ciegas);
         # esto garantiza que el job 2 nunca arranca si el job 1 fallo.

echo "==> 1. Copiando datos y scripts al contenedor namenode..."
docker cp ../datos/transacciones.csv namenode:/tmp/transacciones.csv
docker cp mapper1.py                 namenode:/tmp/mapper1_ej4.py
docker cp reducer1.py                namenode:/tmp/reducer1_ej4.py
docker cp mapper2.py                 namenode:/tmp/mapper2_ej4.py
docker cp reducer2.py                namenode:/tmp/reducer2_ej4.py

echo "==> 2. Subiendo el csv a HDFS..."
docker exec namenode hdfs dfs -mkdir -p /ej4/entrada
docker exec namenode hdfs dfs -put -f /tmp/transacciones.csv /ej4/entrada/
# borramos ambas salidas por si quedaron de una corrida anterior
docker exec namenode hdfs dfs -rm -r -f /ej4/salida1
docker exec namenode hdfs dfs -rm -r -f /ej4/salida2

echo "==> 3. Localizando el JAR de Hadoop Streaming..."
STREAMING_JAR=$(docker exec namenode bash -c 'ls /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-*.jar' | tr -d '\r')
echo "    JAR: $STREAMING_JAR"

echo "==> 4. Lanzando JOB 1 (gasto total por cliente y categoria)..."
# entrada: el csv original -> salida: /ej4/salida1 (cliente,categoria <TAB> suma)
docker exec namenode hadoop jar "$STREAMING_JAR" \
  -files /tmp/mapper1_ej4.py,/tmp/reducer1_ej4.py \
  -mapper "python3 mapper1_ej4.py" \
  -reducer "python3 reducer1_ej4.py" \
  -input /ej4/entrada/transacciones.csv \
  -output /ej4/salida1

echo ""
echo "==> 5. Lanzando JOB 2 (categoria en la que mas gasta cada cliente)..."
# la ENTRADA de este job es la SALIDA del job 1 (no el csv original);
# como el script tiene "set -e" y los comandos van en orden, este job
# solo se lanza si el job 1 ya termino bien.
docker exec namenode hadoop jar "$STREAMING_JAR" \
  -files /tmp/mapper2_ej4.py,/tmp/reducer2_ej4.py \
  -mapper "python3 mapper2_ej4.py" \
  -reducer "python3 reducer2_ej4.py" \
  -input /ej4/salida1 \
  -output /ej4/salida2

echo ""
echo "==> 6. Resultado (categoria en la que mas gasta cada cliente):"
docker exec namenode hdfs dfs -cat /ej4/salida2/part-00000

echo ""
echo "============================================================"
echo " Jobs terminados. Ve el detalle de AMBOS jobs en YARN:"
echo "   http://localhost:8088   <-- toma la captura aqui para el informe"
echo "============================================================"
