import utils.postgres_utils as postgres_utils
from models.base import BaseModel

class Sale(BaseModel):
    table = "sales"
    fields = [ "customer_id", "product_id","sale_date", "quantity", "total" ]

    @classmethod
    def delete_by_customer(cls, customer_id):
        cls._delete_with_transaction("DELETE FROM sales WHERE customer_id = %s;", (customer_id,), f"customer ID {customer_id}")

    @classmethod
    def delete_by_product(cls, product_id):
        cls._delete_with_transaction("DELETE FROM sales WHERE product_id = %s;", (product_id,), f"product ID {product_id}")

    @classmethod
    def delete_by_id(cls, sale_id):
        cls._delete_with_transaction("DELETE FROM sales WHERE id = %s;", (sale_id,), f"sale ID {sale_id}")

    @classmethod
    def _delete_with_transaction(cls, query, params, description):
        try:
            postgres_utils.run_non_select_query("BEGIN;")
            postgres_utils.run_non_select_query(query, params)
            postgres_utils.run_non_select_query("COMMIT;")
            print(f"Deleted sales for {description}.")
        except Exception as e:
            postgres_utils.run_non_select_query("ROLLBACK;")
            print(f"Error deleting sales for {description}: {e}")
            raise