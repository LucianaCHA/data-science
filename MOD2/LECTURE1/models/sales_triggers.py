from models.sales import Sale
from utils.postgres_utils import run_non_select_query


class SalesTriggers(Sale):
    @classmethod
    def create_stock_update_trigger(cls):
        query_function = """
        CREATE OR REPLACE FUNCTION update_stock_after_sale()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE products
            SET stock = stock - NEW.quantity
            WHERE id = NEW.product_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """

        query_trigger = f"""
        CREATE TRIGGER trg_update_stock_after_sale
        AFTER INSERT ON {cls.table}
        FOR EACH ROW
        EXECUTE FUNCTION update_stock_after_sale();
        """

        try:
            run_non_select_query(query_function)
            run_non_select_query(query_trigger)
            print(f"[{cls.__name__}] Trigger created successfully.")
        except Exception as e:
            print(f"[{cls.__name__}] Error creating trigger: {e}")
            raise
