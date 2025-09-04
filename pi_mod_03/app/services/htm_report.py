from jinja2 import Template
from app.services.cloud_storage.cloud_storage import GCSService
from app.config.config import Settings


def generate_html_report(report: dict) -> str:
    """Genera un reporte HTML estilizado a partir del dict de validación."""
    html_template = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Reporte de Validación - {{ file }}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; background: #f0f2f5; }
            h1 { color: #2c3e50; }
            h2 { color: #34495e; }
            .section { background: #fff; border-radius: 8px; padding: 15px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
            table { border-collapse: collapse; width: 100%; margin-top: 10px; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
            th { background-color: #3498db; color: white; }
            .ok { background-color: #2ecc71; color: white; font-weight: bold; padding: 5px 10px; border-radius: 5px; display: inline-block; }
            .fail { background-color: #e74c3c; color: white; font-weight: bold; padding: 5px 10px; border-radius: 5px; display: inline-block; }
            .summary { font-size: 1.1em; margin-bottom: 10px; }
        </style>
    </head>
    <body>
        <h1>Reporte de Validación</h1>
        <p><b>Archivo:</b> {{ file }}</p>
        <p><b>Generado en:</b> {{ timestamp }}</p>

        <div class="section">
            <h2>Resumen General</h2>
            {% if columns_ok and duplicate_ids == 0 and invalid_price == 0 and invalid_coords == 0 %}
                <p class="ok">Todos los controles pasados correctamente</p>
            {% else %}
                <p class="fail">Existen alertas de validación</p>
            {% endif %}
        </div>

        <div class="section">
            <h2>Columnas Faltantes</h2>
            {% if missing_columns %}
                <p class="fail">Columnas faltantes: {{ missing_columns | join(', ') }}</p>
            {% else %}
                <p class="ok">Todas las columnas esperadas están presentes</p>
            {% endif %}
        </div>

        <div class="section">
            <h2>Valores Nulos</h2>
            <table>
                <tr><th>Columna</th><th>Cantidad Nulos</th></tr>
                {% for col, val in nulls.items() %}
                    <tr class="{{ 'fail' if val > 0 else 'ok' }}"><td>{{ col }}</td><td>{{ val }}</td></tr>
                {% endfor %}
            </table>
        </div>

        <div class="section">
            <h2>Tipos Incorrectos</h2>
            {% if type_issues %}
                <table>
                    <tr><th>Columna</th><th>Tipo Detectado</th></tr>
                    {% for col, val in type_issues.items() %}
                        <tr class="fail"><td>{{ col }}</td><td>{{ val }}</td></tr>
                    {% endfor %}
                </table>
            {% else %}
                <p class="ok">Todos los tipos son correctos</p>
            {% endif %}
        </div>

        <div class="section">
            <h2>Duplicados y Coherencia</h2>
            <p><b>IDs Duplicados:</b> {% if duplicate_ids > 0 %}<span class="fail">{{ duplicate_ids }}</span>{% else %}<span class="ok">0</span>{% endif %}</p>
            <p><b>Coordenadas Inválidas:</b> {% if invalid_coords > 0 %}<span class="fail">{{ invalid_coords }}</span>{% else %}<span class="ok">0</span>{% endif %}</p>
            <p><b>Precios Inválidos:</b> {% if invalid_price > 0 %}<span class="fail">{{ invalid_price }}</span>{% else %}<span class="ok">0</span>{% endif %}</p>
        </div>
    </body>
    </html>
    """
    template = Template(html_template)
    return template.render(**report)


def upload_html_report(report: dict, file_name: str):
    settings = Settings()
    gcs = GCSService(bucket_name=settings.GCS_BUCKET)

    html_content = generate_html_report(report)
    report_path = f"reports_html/{file_name.replace('/', '_')}_report.html"

    gcs.upload_file(file_content=html_content, file_path=report_path, content_type="text/html")
    print(f"Reporte HTML subido correctamente: gs://{settings.GCS_BUCKET}/{report_path}")
