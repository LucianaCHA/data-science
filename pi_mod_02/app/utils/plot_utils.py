import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from app.utils import postgres_utils


def plot_boxplot_with_outliers(table, column, step=10, show_outlier_count=True):
    """
    Plots a boxplot of the specified column from a SQL table with IQR-based outlier bounds.

    Parameters:
    - table (str): Name of the table.
    - column (str): Column to analyze.
    - step (int): Step size for x-axis ticks.
    - show_outlier_count (bool): Whether to print number of outliers.
    """
    # Fetch column data from the database
    query = f'SELECT "{column}" FROM "{table}";'
    df = postgres_utils.run_query(query)

    # Use the actual column name from the DataFrame
    actual_col = df.columns[0]

    # Compute IQR and bounds
    Q1 = df[actual_col].quantile(0.25)
    Q3 = df[actual_col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outliers = df[(df[actual_col] < lower_bound) | (df[actual_col] > upper_bound)]

    if show_outlier_count:
        print(f"Number of outliers in '{column}': {len(outliers)}")

    # Plot boxplot
    plt.figure(figsize=(10, 2))
    sns.boxplot(x=df[actual_col])
    plt.title(f"Boxplot of {column}")
    max_val = df[actual_col].max()
    plt.xticks(np.arange(0, int(max_val) + step, step))
    plt.tight_layout()
    plt.show()

    return outliers, lower_bound, upper_bound


def plot_top_bar_chart(
    df,
    x_column: str,
    y_column: str,
    plot_title: str = "plot",
    x_label: str = "",
    y_label: str = "",
    top_n: int = 10,
    figsize=(12, 6),
):
    if df.empty:
        print("⚠️ El DataFrame está vacío. No se puede generar el gráfico.")
        return

    # Ordenar y limitar los datos
    df_sorted = df.sort_values(by=y_column, ascending=False).head(top_n)

    # Crear figura
    plt.figure(figsize=figsize)

    # Gráfico de barras
    sns.barplot(
        data=df_sorted,
        x=x_column,
        y=y_column,
        color="skyblue",
    )

    # Títulos y etiquetas
    plt.title(plot_title, fontsize=18)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    plt.xticks(rotation=45, ha="right", fontsize=12)
    plt.yticks(fontsize=12)

    # Ajuste de layout
    plt.tight_layout()
    plt.show()


def plot_top_spenders(
    df,
    x_column: str,
    y_column: str,
    plot_title: str = "Top Spenders",
    x_label: str = "Spender",
    y_label: str = "Amount Spent",
    top_n: int = 10,
    figsize=(12, 6),
):
    plot_top_bar_chart(
        df,
        x_column=x_column,
        y_column=y_column,
        plot_title=plot_title,
        x_label=x_label,
        y_label=y_label,
        top_n=top_n,
        figsize=figsize,
    )


def plot_high_stock_lowest_sells():
    """
    Muestra productos con alto stock (>=150) y bajas ventas (<500).
    Gráfico de stock con anotación de ventas.
    """
    query = """
    SELECT
    p."ProductoID",
    p."Nombre",
    p."Stock",
    COALESCE(SUM(d."Cantidad"), 0) AS total_vendido
    FROM "Productos" p
    LEFT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
    GROUP BY p."ProductoID", p."Nombre", p."Stock"
    HAVING COALESCE(SUM(d."Cantidad"), 0) < 790
    ORDER BY p."Stock" DESC
    LIMIT 10;
    """
    df = postgres_utils.run_query(query)
    df = df.sort_values(by="Stock", ascending=True)

    plt.figure(figsize=(8, 5))
    bars = plt.barh(df["Nombre"], df["Stock"], color="lightblue")

    for bar, val in zip(bars, df["total_vendido"]):
        plt.text(
            bar.get_width() + 2,
            bar.get_y() + bar.get_height() / 2,
            f"Vendidos: {val}",
            va="center",
            fontsize=9,
            color="gray",
        )

    plt.xlabel("Stock disponible")
    plt.title("Productos con alto stock y bajas ventas")
    plt.tight_layout()
    plt.show()
