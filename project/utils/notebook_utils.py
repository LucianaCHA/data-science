from IPython.display import display, HTML


def print_colored_separator(
    text: str = "="*60,
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


