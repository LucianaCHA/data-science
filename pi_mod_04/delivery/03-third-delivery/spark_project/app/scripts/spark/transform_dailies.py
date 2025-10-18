from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    from_unixtime,
    to_date,
    lit,
    when,
    input_file_name,
    regexp_extract,
)
import sys

REGEX = r"forecast/([^/]+)/[^/]+\.parquet"


def transform_forecast_data(df):
    df = df.withColumn("city", regexp_extract(input_file_name(), REGEX, 1))

    df = df.withColumn("entry", explode(col("list")))

    df = (
        df.withColumn("timestamp", col("entry.dt").cast("long"))
        .withColumn("datetime", from_unixtime(col("timestamp")))
        .withColumn("date", to_date(col("datetime")))
        .withColumn("temperature", col("entry.main.temp"))
        .withColumn("humidity", col("entry.main.humidity"))
        .withColumn("weather_main", col("entry.weather")[0]["main"])
        .withColumn("weather_desc", col("entry.weather")[0]["description"])
        .withColumn("wind_speed", col("entry.wind.speed"))
        .withColumn("wind_deg", col("entry.wind.deg"))
        .withColumn(
            "is_rainy",
            when(col("weather_main").like("%Rain%"), lit(True)).otherwise(lit(False)),
        )
        .withColumn(
            "is_cloudy",
            when(col("weather_main").like("%Cloud%"), lit(True)).otherwise(lit(False)),
        )
    )

    df = df.select(
        "timestamp",
        "datetime",
        "date",
        "city",
        "temperature",
        "humidity",
        "weather_main",
        "weather_desc",
        "wind_speed",
        "wind_deg",
        "is_rainy",
        "is_cloudy",
    )

    return df


def main(input_root: str, output_root: str):
    spark = (
        SparkSession.builder.appName("Transform Forecast Weather")
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.InstanceProfileCredentialsProvider",
        )
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )

    df = spark.read.option("recursiveFileLookup", "true").parquet(input_root)

    archivos = df.select(input_file_name().alias("archivo")).distinct().collect()
    print("Archivos encontrados y procesados:")
    for f in archivos:
        print(f.archivo)

    transformed_df = transform_forecast_data(df)

    transformed_df.write.mode("append").partitionBy("city", "date").parquet(output_root)

    spark.stop()
    print("Transformación de pronósticos completada.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("transform_dailies.py <input_path> <output_path>")
        sys.exit(1)

    input_root = sys.argv[1]
    output_root = sys.argv[2]
    main(input_root, output_root)
