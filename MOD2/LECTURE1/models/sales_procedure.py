from models.sales import Sale
from utils.postgres_utils import run_non_select_query


class SalesProcedure(Sale):
    update_total_sales_query = """
    CREATE OR REPLACE PROCEDURE sp_sale_registry(
        IN p_customer_id INT,
        IN p_product_id INT,
        IN p_sale_date DATE,
        IN p_quantity INT
    )
    LANGUAGE plpgsql
    AS $$
    DECLARE
        sale_price DECIMAL(10,2);
        sale_total DECIMAL(10,2);
    BEGIN
        -- 1. Buscar el precio del producto
        SELECT price INTO sale_price
        FROM products
        WHERE id = p_product_id;

        -- 2. Calcular el total (cantidad * precio)
        sale_total := sale_price * p_quantity;

        -- 3. Insertar la venta
        INSERT INTO sales (customer_id, product_id, sale_date, quantity, total)
        VALUES (p_customer_id, p_product_id, p_sale_date, p_quantity, sale_total);
    END;
    $$;
    """

    @classmethod
    def create_sale_procedure(cls):
        try:
            run_non_select_query(cls.update_total_sales_query)
            print(f"[{cls.__name__}] Sale procedure created successfully.")
        except Exception as e:
            print(f"[{cls.__name__}] Error creating sale procedure: {e}")
            raise

    @classmethod
    def call_sale_procedure(cls, customer_id, product_id, sale_date, quantity):
        try:
            run_non_select_query(
                "CALL sp_sale_registry(%s, %s, %s, %s);",
                (customer_id, product_id, sale_date, quantity)
            )
            print(f"Sale registered successfully for customer {customer_id} and product {product_id}.")

        except Exception as e:
            print(f"Error registering sale: {e}")
            raise