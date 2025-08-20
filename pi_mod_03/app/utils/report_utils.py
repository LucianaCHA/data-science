from app.utils import plot_utils, postgres_utils, notebook_utils
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def show_top_spenders_chart():

    query = """
    SELECT "UsuarioID", SUM("Total") AS "GastoTotal"
    FROM "Ordenes"
    GROUP BY "UsuarioID"
    ORDER BY "GastoTotal" DESC
    LIMIT 10
    """

    top_spenders_df = postgres_utils.run_query(query)

    plot_utils.plot_top_bar_chart(
        df=top_spenders_df,
        x_column="UsuarioID",
        y_column="GastoTotal",
        plot_title="Top 10 usuarios por gasto total",
        x_label="Usuario ID",
        y_label="Gasto acumulado",
        top_n=10,
        figsize=(20, 8),
    )


def show_high_product_vs_low_stock():
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
    notebook_utils.print_colored(
        "Productos con alto stock y bajas ventas (< 790)", "green"
    )

    return postgres_utils.run_query(query)


def show_top_categories_chart():
    query = """
    SELECT
        p."ProductoID",
        p."Nombre",
        SUM(d."Cantidad") AS total_vendido
    FROM "Productos" p
    RIGHT JOIN "DetalleOrdenes" d ON p."ProductoID" = d."ProductoID"
    GROUP BY p."ProductoID", p."Nombre"
    ORDER BY total_vendido DESC
    LIMIT 10;
    """
    notebook_utils.print_colored("Productos más vendidos por volumen", "green")
    return postgres_utils.run_query(query)


def show_orders_distrbution_chart():

    query = """
    SELECT
        "OrdenID",
        SUM("Cantidad") AS total_items
    FROM "DetalleOrdenes"
    GROUP BY "OrdenID";"""

    data_frame = postgres_utils.run_query(query)

    notebook_utils.print_colored("Distribución de órdenes por monto total", "green")
    plot_utils.plot_histogram_with_outliers(
        df=data_frame,
        column="total_items",
        bins="auto",
        title="Distribución de órdenes por número de ítems",
        color="salmon",
        label_x="Total de ítems por orden",
        label_y="Cantidad de órdenes",
    )


def show_adress_distribution_chart():

    data_frame = postgres_utils.run_query('SELECT * FROM "DireccionesEnvio";')

    province_data = data_frame["Provincia"].value_counts(dropna=False)

    province_data.head(20).sort_values().plot(
        kind="barh", figsize=(8, 6), color="skyblue"
    )

    plt.title("Distribución de direcciones por provincia")
    plt.xlabel("Cantidad de registros")
    plt.ylabel("Provincia")
    plt.tight_layout()
    plt.show()


def show_geographic_sales_distribution_chart():

    orders_distribution_query = """
    SELECT 
        de."Provincia",
        COUNT(o."OrdenID") AS total_ordenes
    FROM "Ordenes" o
    JOIN "DireccionesEnvio" de ON o."UsuarioID" = de."UsuarioID"
    GROUP BY de."Provincia"
    ORDER BY total_ordenes DESC;
    """

    orders_distribution_df = postgres_utils.run_query(orders_distribution_query)

    notebook_utils.print_colored("Distribución de órdenes por provincia", "green")
    plot_utils.plot_top_bar_chart(
        df=orders_distribution_df,
        x_column="Provincia",
        y_column="total_ordenes",
        plot_title="Distribución de órdenes por provincia",
        x_label="Provincia",
        y_label="Cantidad de órdenes",
        top_n=10,
        figsize=(10, 6),
    )


def show_items_per_order_chart():
    query = """
    SELECT 
        o."OrdenID",
        COUNT(d."ProductoID") AS total_items
    FROM "Ordenes" o
    JOIN "DetalleOrdenes" d ON o."OrdenID" = d."OrdenID"
    GROUP BY o."OrdenID"
    ORDER BY total_items DESC;
    """

    items_per_order_df = postgres_utils.run_query(query)

    notebook_utils.print_colored("Cantidad de ítems por orden", "green")
    plot_utils.plot_histogram_with_outliers(
        df=items_per_order_df,
        column="total_items",
        bins="auto",
        title="Distribución de ítems por orden",
        color="salmon",
        label_x="Total de ítems por orden",
        label_y="Cantidad de órdenes",
    )


def show_sales_by_province():

    sales_distribution_query = """
    SELECT
        de."Provincia",
        SUM(o."Total") AS volumen_ventas
    FROM "Ordenes" o
    JOIN "DireccionesEnvio" de ON o."UsuarioID" = de."UsuarioID"
    GROUP BY de."Provincia"
    ORDER BY volumen_ventas DESC;
    """
    sales_distribution_query = postgres_utils.run_query(sales_distribution_query)

    notebook_utils.print_colored("Distribución de ventas por provincia", "green")
    plot_utils.plot_top_bar_chart(
        df=sales_distribution_query,
        x_column="Provincia",
        y_column="volumen_ventas",
        plot_title="Distribución de ventas por provincia",
        x_label="Provincia",
        y_label="Cantidad de ventas",
        top_n=10,
        figsize=(10, 6),
    )


def show_cart_adding_items_chart():
    query = """
    SELECT
        DATE_TRUNC('day', "FechaAgregado") AS semana,
        COUNT(*) AS total_agregados,
        SUM("Cantidad") AS cantidad_total
    FROM "Carrito"
    GROUP BY semana
    ORDER BY semana;
    """
    notebook_utils.print_colored("Agregados por día", "green")
    df_carritos_diario = postgres_utils.run_query(query)

    # Convertimos a datetime
    df_carritos_diario["semana"] = pd.to_datetime(df_carritos_diario["semana"])

    # Agregamos columna formateada: fecha + día
    df_carritos_diario["fecha_dia"] = df_carritos_diario["semana"].dt.strftime(
        "%Y-%m-%d (%A)"
    )

    # Estilo
    sns.set(style="whitegrid")

    # Creamos figura
    plt.figure(figsize=(18, 6))

    # Gráficos de línea
    sns.lineplot(
        data=df_carritos_diario,
        x="fecha_dia",
        y="total_agregados",
        label="Total Agregados",
        marker="o",
    )
    sns.lineplot(
        data=df_carritos_diario,
        x="fecha_dia",
        y="cantidad_total",
        label="Cantidad Total",
        marker="o",
        linestyle="--",
    )

    # Mostrar etiquetas solo cada 2 días
    xticks = df_carritos_diario["fecha_dia"].tolist()
    plt.xticks(ticks=range(0, len(xticks), 2), labels=xticks[::2], rotation=90)

    # Ajustes
    plt.title("Tendencia diaria de productos agregados al carrito", fontsize=16)
    plt.xlabel("Fecha (Día)")
    plt.ylabel("Cantidad")
    plt.legend()
    plt.tight_layout()

    # Mostrar
    plt.show()


def show_most_sale_and_more_added():
    query = """
    SELECT
        p."ProductoID",
        p."Nombre",
        COALESCE(SUM(v."Cantidad"), 0) AS total_vendido,
        COALESCE(SUM(c.total_agregado), 0) AS total_agregado
    FROM "Productos" p
    LEFT JOIN (
        SELECT d."ProductoID", SUM(d."Cantidad") AS "Cantidad"
        FROM "DetalleOrdenes" d
        GROUP BY d."ProductoID"
        ORDER BY SUM(d."Cantidad") DESC
        LIMIT 10
    ) v ON p."ProductoID" = v."ProductoID"
    LEFT JOIN (
        SELECT c."ProductoID", SUM(c."Cantidad") AS total_agregado
        FROM "Carrito" c
        GROUP BY c."ProductoID"
        ORDER BY SUM(c."Cantidad") DESC
        LIMIT 10
    ) c ON p."ProductoID" = c."ProductoID"
    WHERE v."ProductoID" IS NOT NULL OR c."ProductoID" IS NOT NULL
    GROUP BY p."ProductoID", p."Nombre"
    ORDER BY total_vendido DESC, total_agregado DESC;
    """

    sold_vs_cart = postgres_utils.run_query(query)

    notebook_utils.print_colored(
        "Comparación de productos más vendidos vs más agregados al carrito", "green"
    )

    # Preparar gráfico comparativo con matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    df = sold_vs_cart
    x = np.arange(len(df))  # posiciones en el eje X
    width = 0.35  # ancho de barra

    fig, ax = plt.subplots(figsize=(12, 6))
    bars1 = ax.bar(
        x - width / 2, df["total_vendido"], width, label="Vendidos", color="skyblue"
    )
    bars2 = ax.bar(
        x + width / 2,
        df["total_agregado"],
        width,
        label="Agregados al carrito",
        color="salmon",
    )

    ax.set_xlabel("Producto")
    ax.set_ylabel("Cantidad")
    ax.set_title("Top productos vendidos vs agregados al carrito")
    ax.set_xticks(x)
    ax.set_xticklabels(df["Nombre"], rotation=45, ha="right")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    plt.show()


def show_monthly_sales():
    query = """
    SELECT
        DATE_TRUNC('month', "FechaOrden") AS mes,
        SUM("Total") AS total_recaudado
    FROM "Ordenes"
    GROUP BY mes
    ORDER BY mes;
    """
    notebook_utils.print_colored("Recaudación mensual", "green")
    df_recaudacion_mensual = postgres_utils.run_query(query)

    plot_utils.plot_top_bar_chart(
        df=df_recaudacion_mensual,
        x_column="mes",
        y_column="total_recaudado",
        plot_title="Recaudación mensual",
        x_label="Mes",
        y_label="Total recaudado",
        figsize=(12, 6),
    )


def show_rating_bar_chart():
    query = """
    SELECT
        p."ProductoID",
        p."Nombre",
        AVG(r."Calificacion") AS calificacion_promedio
    FROM "Productos" p
    JOIN "ReseñasProductos" r ON p."ProductoID" = r."ProductoID"
    GROUP BY p."ProductoID", p."Nombre"
    ORDER BY calificacion_promedio DESC
    LIMIT 10;
    """

    notebook_utils.print_colored("Calificaciones promedio de productos", "green")
    df_calificaciones = postgres_utils.run_query(query)

    plot_utils.plot_top_bar_chart(
        df=df_calificaciones,
        x_column="Nombre",
        y_column="calificacion_promedio",
        plot_title="Calificaciones promedio de productos",
        x_label="Producto",
        y_label="Calificación promedio",
        top_n=10,
        figsize=(12, 6),
    )


def show_payment_method_frequency_chart():
    query = """
    SELECT "MetodoPagoID", COUNT(*) AS cantidad
    FROM "HistorialPagos"
    GROUP BY "MetodoPagoID"
    ORDER BY cantidad DESC;
    """
    notebook_utils.print_colored("Frecuencia por MetodoPagoID", "green")
    df_metodos_pago = postgres_utils.run_query(query)

    plot_utils.plot_top_bar_chart(
        df=df_metodos_pago,
        x_column="MetodoPagoID",
        y_column="cantidad",
        plot_title="Frecuencia por MetodoPagoID",
        x_label="MetodoPagoID",
        y_label="Cantidad de Pagos",
        figsize=(10, 6),
    )
