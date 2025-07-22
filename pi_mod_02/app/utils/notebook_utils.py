from IPython.display import display, HTML
from . import postgres_utils


def print_colored_separator(
    text: str = "=" * 60,
    color: str = "grey",
    size: str = "14px",
    weight: str = "bold",
):
    return print_colored(text, color, size, weight, tag="h3")


def print_colored(
    text: str,
    color: str = "black",
    size: str = "14px",
    weight: str = "bold",
    tag: str = "span",
):
    """
    Imprime texto con estilo en un notebook Jupyter usando HTML.

    Parámetros:
    - text: str → El texto a mostrar.
    - color: str → Color CSS (ej. 'red', '#ff0000').
    - size: str → Tamaño de fuente (ej. '16px', '1.2em').
    - weight: str → Peso de fuente ('normal', 'bold').
    - tag: str → Etiqueta HTML ('span', 'div', 'h3', etc.).
    """
    html = f"""<{tag} style='color: {color}; font-size: {size};
    font-weight: {weight};'>{text}</{tag}>"""
    display(HTML(html))


def show_table_data(table_name: str):

    print_colored(f"Tabla: {table_name}", "orange")
    data = postgres_utils.run_query(f'SELECT * FROM "{table_name}";')

    print_colored("Datos de tabla", "orange")
    display(data.info())
    print_colored("Primeros valores", "orange")
    display(data.head())


def show_duplicates_and_null_info(table_name: str):
    data = postgres_utils.run_query(f'SELECT * FROM "{table_name}";')
    print_colored("Columnas con nulos (%)", "orange")
    display(data.isnull().mean() * 100)

    print_colored("Duplicados", "orange")
    display(data.duplicated().sum())


def show_table_stats(table_name: str):
    data = postgres_utils.run_query(f'SELECT * FROM "{table_name}";')
    print_colored("Estadísticas de tabla", "orange")
    display(data.describe())
