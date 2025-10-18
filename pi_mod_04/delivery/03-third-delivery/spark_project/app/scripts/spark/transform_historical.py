from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_unixtime, to_date, lit, when, lower
import sys


def main(input_path: str, output_path: str):
    spark = SparkSession.builder.appName("Transform Historical").getOrCreate()

    df = spark.read.option("multiline", "true").json(input_path)

    df = (
        df.withColumn("timestamp", col("dt"))
        .withColumn("datetime", from_unixtime("dt"))
        .withColumn("date", to_date("datetime"))
        .withColumn("city", lower(col("city_name")))
        .withColumn("temperature", col("main.temp"))
        .withColumn("humidity", col("main.humidity"))
        .withColumn("weather_main", col("weather")[0]["main"])
        .withColumn("weather_desc", col("weather")[0]["description"])
        .withColumn("wind_speed", col("wind.speed"))
        .withColumn("wind_deg", col("wind.deg"))
        .withColumn(
            "is_rainy",
            when(col("weather_main")
                 .like("%Rain%"), lit(True)).otherwise(lit(False)),
        )
        .withColumn(
            "is_cloudy",
            when(col("weather_main")
                 .like("%Cloud%"), lit(True)).otherwise(lit(False)),
        )
        .select(
            "timestamp",
            "datetime",
            "temperature",
            "humidity",
            "weather_main",
            "weather_desc",
            "wind_speed",
            "wind_deg",
            "is_rainy",
            "is_cloudy",
            "city",
            "date",
        )
    )

    print("Esquema final normalizado:")
    df.printSchema()

    print(f"Escribiendo resultado particionado en: {output_path}")
    df.write.mode("overwrite").partitionBy("city", "date").parquet(output_path)

    spark.stop()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("transform_historicals.py <input_path> <output_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
