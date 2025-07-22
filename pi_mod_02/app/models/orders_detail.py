from sqlalchemy import ForeignKey, Integer, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import BaseModel
from app.models.constants import (
    OrderColumns,
    OrderDetailColumns,
    ProductColumns,
    TableNames,
)
from decimal import Decimal


class OrderDetail(BaseModel):

    __tablename__ = TableNames.ORDER_DETAILS
    __table_args__ = (
        CheckConstraint(
            f"{OrderDetailColumns.QUANTITY} > 0", name="quantity_positive"),
        CheckConstraint(
            f"{OrderDetailColumns.UNIT_PRICE} >= 0",
            name="unit_price_non_negative"
        ),
    )

    order_detail_id: Mapped[int] = mapped_column(
        OrderDetailColumns.ORDER_DETAIL_ID, primary_key=True
    )
    order_id: Mapped[int] = mapped_column(
        OrderColumns.ORDER_ID, ForeignKey("Ordenes.OrdenID"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ProductColumns.PRODUCT_ID,
        ForeignKey("Productos.ProductoID"),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        OrderDetailColumns.QUANTITY, Integer, nullable=False
    )
    unit_price: Mapped[Numeric] = mapped_column(
        OrderDetailColumns.UNIT_PRICE, Numeric(10, 2), nullable=False
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            order_detail_id=data.get("order_detail_id"),
            order_id=data.get("order_id"),
            product_id=data.get("product_id"),
            quantity=data.get("quantity", 1),
            unit_price=Decimal(data.get("unit_price", 0)),
        )
