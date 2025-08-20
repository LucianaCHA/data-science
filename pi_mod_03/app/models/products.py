from sqlalchemy import String, Integer, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.db.base import BaseModel
from decimal import Decimal

from app.models.constants import CategoryColumns, TableNames, ProductColumns
from app.models.categories import Category


class Product(BaseModel):

    __tablename__ = TableNames.PRODUCTS

    __table_args__ = (
        CheckConstraint(
            f"{ProductColumns.STOCK} >= 0", name="stock_non_negative"),
        CheckConstraint(
            f"{ProductColumns.PRICE} >= 0", name="price_non_negative"),
    )

    product_id: Mapped[int] = mapped_column(
        ProductColumns.PRODUCT_ID, primary_key=True)
    name: Mapped[str] = mapped_column(ProductColumns.NAME, String(255))
    description: Mapped[str] = mapped_column(
        ProductColumns.DESCRIPTION, String)
    price: Mapped[Decimal] = mapped_column(ProductColumns.PRICE, Numeric)
    stock: Mapped[int] = mapped_column(ProductColumns.STOCK, Integer)
    category_id: Mapped[int] = mapped_column(
        CategoryColumns.CATEGORY_ID,
        ForeignKey("Categorias.CategoriaID"),
        nullable=False,
    )
    category: Mapped["Category"] = relationship("Category", backref="products")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            product_id=data.get("product_id"),
            name=data.get("name", "").strip(),
            description=data.get("description", "").strip(),
            price=Decimal(data.get("price", 0)),
            stock=data.get("stock", 0),
            category_id=data.get("category_id"),
        )
