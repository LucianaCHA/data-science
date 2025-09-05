from app.services.cloud_storage.cloud_storage import GCSService
from app.config import config
from sqlalchemy import create_engine
import pandas as pd

# 1. Definición de queries SQL

sql_average_price_per_neighbourhood_group = """
SELECT
    neighbourhood_group,
    neighbourhood,
    ROUND(AVG(price), 2) AS avg_price
FROM rooms_dim
GROUP BY neighbourhood_group, neighbourhood
ORDER BY avg_price DESC;
"""

sql_most_offered_room_type = """
SELECT
    room_type,
    COUNT(*) AS count
FROM rooms_dim
GROUP BY room_type
ORDER BY count DESC
LIMIT 1;
"""

sql_highest_revenue_room_type = """
SELECT
    room_type,
    ROUND(SUM(price * availability_365), 2) AS estimated_revenue
FROM rooms_dim
GROUP BY room_type
ORDER BY estimated_revenue DESC
LIMIT 1;
"""

top_hosts = """
SELECT
    host_id,
    COUNT(*) AS listings,
    MIN(price) AS min_price,
    MAX(price) AS max_price,
    ROUND(AVG(price), 2) AS avg_price
FROM rooms_dim
GROUP BY host_id
ORDER BY listings DESC
LIMIT 10;
"""

sql_availability_by_neighbourhood_and_room_type = """
SELECT
    neighbourhood_group,
    neighbourhood,
    ROUND(AVG(availability_365), 2) AS avg_availability
FROM rooms_dim
GROUP BY neighbourhood_group, neighbourhood
ORDER BY avg_availability DESC;
"""

sql_availability_by_room_type = """
SELECT
    room_type,
    ROUND(AVG(availability_365), 2) AS avg_availability
FROM rooms_dim
GROUP BY room_type
ORDER BY avg_availability DESC;
"""

reviews_analysis = """
SELECT
    TO_CHAR(last_review, 'YYYY-MM') AS review_month,
    neighbourhood_group,
    COUNT(*) AS reviews
FROM rooms_dim
WHERE last_review IS NOT NULL
GROUP BY review_month, neighbourhood_group
ORDER BY review_month, neighbourhood_group;
"""

sql_active_listings_by_neighbourhood = """
SELECT
    neighbourhood,
    COUNT(*) AS active_listings
FROM rooms_dim
WHERE availability_365 > 0
GROUP BY neighbourhood
ORDER BY active_listings DESC
LIMIT 10;
"""

sql_price_distribution = """
WITH percentiles AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3
    FROM rooms_dim
)
SELECT
    rd.*
FROM rooms_dim rd, percentiles p
WHERE price > (p.q3 + 1.5 * (p.q3 - p.q1))
ORDER BY price DESC;
"""

ocupacion_analysis = """
SELECT
    availability_365,
    SUM(number_of_reviews) AS total_reviews,
    ROUND(AVG(reviews_per_month), 2) AS avg_reviews_per_month
FROM rooms_dim
GROUP BY availability_365
ORDER BY availability_365;
"""


def get_sql_queries():
    return {
        "average_price_per_neighbourhood_group": sql_average_price_per_neighbourhood_group,
        "most_offered_room_type": sql_most_offered_room_type,
        "highest_revenue_room_type": sql_highest_revenue_room_type,
        "top_hosts": top_hosts,
        "availability_by_neighbourhood_and_room_type": sql_availability_by_neighbourhood_and_room_type,
        "availability_by_room_type": sql_availability_by_room_type,
        "reviews_analysis": reviews_analysis,
        "active_listings_by_neighbourhood": sql_active_listings_by_neighbourhood,
        "price_distribution": sql_price_distribution,
        "ocupacion_analysis": ocupacion_analysis,
    }


# 2. Ejecutar queries y devolver resultados como DataFrames

def execute_query(engine, query):
    with engine.connect() as conn:
        return pd.read_sql_query(query, conn)


def return_dataframes(engine):
    queries = get_sql_queries()
    results = {}
    for name, query in queries.items():
        df = execute_query(engine, query)
        results[name] = df
    return results


# 3. Crear HTML con estilo básico y retornar el contenido

def create_html_report(dataframes: dict, output_file="report.html") -> str:
    html = """
    <html>
    <head>
        <title>Airbnb Analytics Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1, h2 { color: #2c3e50; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 40px; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Airbnb Analytics Report</h1>
    """

    for name, df in dataframes.items():
        html += f"<h2>{name.replace('_', ' ').title()}</h2>"
        html += df.to_html(index=False, classes="dataframe", border=0)
        html += "<br><br>"

    html += "</body></html>"

    # Guardar localmente
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    return html


# 4. Subir reporte a GCS

def upload_html_report(dataframes: dict, file_name: str):
    settings = config.Settings()
    gcs = GCSService(bucket_name=settings.GCS_BUCKET)

    html_content = create_html_report(dataframes)
    report_path = f"analytics_reports_html/{file_name.replace('/', '_')}_report.html"

    gcs.upload_file(
        file_content=html_content, file_path=report_path, content_type="text/html"
    )

    print(f"Reporte HTML subido correctamente: gs://{settings.GCS_BUCKET}/{report_path}")


if __name__ == "__main__":
    settings = config.Settings()
    db_url = settings.DB_URL
    engine = create_engine(db_url)

    dataframes = return_dataframes(engine)
    create_html_report(dataframes)
    upload_html_report(dataframes, "airbnb_analytics")
    print("Reporte generado correctamente.")
