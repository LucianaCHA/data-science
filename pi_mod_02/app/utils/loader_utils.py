from enum import StrEnum, IntEnum, auto
import re

from app.models.constants import TableNames


class LoaderSQLFilePaths(StrEnum):
    USERS = "/app/scripts/db/data/users.sql"
    CATEGORIES = "/app/scripts/db/data/categories.sql"
    PRODUCTS = "/app/scripts/db/data/products.sql"
    ORDERS = "/app/scripts/db/data/orders.sql"
    ORDERS_DETAIL = "/app/scripts/db/data/orders_detail.sql"
    DELIVERY_ADDRESS = "/app/scripts/db/data/delivery_address.sql"
    CART = "/app/scripts/db/data/cart.sql"
    PAYMENT_METHODS = "/app/scripts/db/data/payment_methods.sql"
    ORDERS_PAYMENT_METHODS = "/app/scripts/db/data/orders_payment_methods.sql"
    REVIEWS = "/app/scripts/db/data/product_reviews.sql"
    PAYMENT_HISTORY = "/app/scripts/db/data/payment_history.sql"


class LoaderTablesPriority(IntEnum):
    USERS = 1
    CATEGORIES = 2
    PRODUCTS = 3
    ORDERS = 4
    ORDER_DETAIL = 5
    DELIVERY_ADDRESS = 6
    CART = 7
    PAYMENT_METHODS = 8
    ORDERS_PAYMENT_METHODS = 9
    REVIEWS = 10
    PAYMENT_HISTORY = 11


class LoaderInsertFormat(StrEnum):
    SINGLE_LINE = auto()
    MULTI_LINE = auto()


class LoaderRegexPatterns:
    _formats = {
        LoaderInsertFormat.SINGLE_LINE: r"INSERT INTO {table_name} .*?VALUES \((.*?)\);",
        LoaderInsertFormat.MULTI_LINE: (
            r"INSERT INTO {table_name}\s*\((.*?)\)\s*VALUES\s*((?:\([^)]+\),?\s*)+);"
        ),
    }

    _table_patterns = {
        TableNames.USERS: LoaderInsertFormat.SINGLE_LINE,
        TableNames.ORDERS: LoaderInsertFormat.SINGLE_LINE,
        TableNames.ORDER_DETAILS: LoaderInsertFormat.SINGLE_LINE,
        TableNames.CATEGORIES: LoaderInsertFormat.MULTI_LINE,
        TableNames.PRODUCTS: LoaderInsertFormat.MULTI_LINE,
        TableNames.DELIVERY_ADDRESS: LoaderInsertFormat.SINGLE_LINE,
        TableNames.CART: LoaderInsertFormat.SINGLE_LINE,
        TableNames.PAYMENT_METHODS: LoaderInsertFormat.MULTI_LINE,
        TableNames.ORDERS_PAYMENT_METHODS: LoaderInsertFormat.SINGLE_LINE,
        TableNames.REVIEWS: LoaderInsertFormat.SINGLE_LINE,
        TableNames.PAYMENT_HISTORY: LoaderInsertFormat.SINGLE_LINE,
    }

    _compiled_patterns: dict[str, tuple[re.Pattern, LoaderInsertFormat]] = {}

    @classmethod
    def get(cls, table_name: TableNames) -> tuple[re.Pattern, LoaderInsertFormat]:
        if table_name not in cls._compiled_patterns:
            insert_format = cls._table_patterns.get(table_name)
            if not insert_format:
                raise ValueError(f"No regex pattern defined for table '{table_name}'")

            pattern = cls._formats[insert_format].format(table_name=table_name)
            flags = re.IGNORECASE | (
                re.DOTALL if insert_format == LoaderInsertFormat.MULTI_LINE else 0
            )

            compiled = re.compile(pattern, flags)
            cls._compiled_patterns[table_name] = (compiled, insert_format)

        return cls._compiled_patterns[table_name]
