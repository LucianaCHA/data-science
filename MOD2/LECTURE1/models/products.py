


from utils import postgres_utils
from models.base import BaseModel


class Product(BaseModel):
    table = "products"
    fields = ["name", "category", "price", "stock", "branch_id"]

    @classmethod
    def update_product_prices(cls, category, percentage):
        if not category:
            raise ValueError("Category cannot be empty.")
        if not isinstance(percentage, (int, float)):
            raise TypeError("Percentage must be a number.")
        if percentage < 0:
            raise ValueError("Percentage cannot be negative.")

        query = f"""
        UPDATE {cls.table}
        SET price = price * (1 + %s / 100.0)
        WHERE LOWER(category) = LOWER(%s);
        """

        try:
            postgres_utils.run_non_select_query(query, (percentage, category))
        except Exception as error:
            print(f"Error updating prices for category '{category}': {error}")
            raise error