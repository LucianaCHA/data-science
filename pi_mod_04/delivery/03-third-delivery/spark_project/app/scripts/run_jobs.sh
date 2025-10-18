#!/bin/bash
set -e

echo "Ejecutando transformación históricos..."
/opt/spark/bin/spark-submit \
      --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.698 \
      --conf spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.InstanceProfileCredentialsProvider \
      --conf spark.hadoop.fs.s3a.path.style.access=true \
      --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
      /app/scripts/spark/transform_historical.py \
      s3a://lucianacha-pi-mod4/raw/external_data/weather_api/historical/ \
      s3a://lucianacha-pi-mod4/processed/weather_normalized/

echo "Ejecutando transformación diarios..."
/opt/spark/bin/spark-submit \
      --packages org.apache.hadoop:hadoop-aws:3.3.2,com.amazonaws:aws-java-sdk-bundle:1.12.698 \
      --conf spark.hadoop.fs.s3a.aws.credentials.provider=com.amazonaws.auth.InstanceProfileCredentialsProvider \
      --conf spark.hadoop.fs.s3a.path.style.access=true \
      --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
  /app/scripts/spark/transform_dailies.py \
  s3a://lucianacha-pi-mod4/raw/external_data/weather_api/forecast/ \
  s3a://lucianacha-pi-mod4/processed/weather_normalized/

echo "Todos los jobs completados con éxito."
