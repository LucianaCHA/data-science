from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from app.db.base import BaseModel
from app.models.constants import (
    TableNames,
    OrderPaymentMethodColumns,
    OrderColumns,
    PaymentMethodColumns,
)
from decimal import Decimal


class OrderPaymentMethod(BaseModel):
    __tablename__ = TableNames.ORDERS_PAYMENT_METHODS
    order_payment_method_id: Mapped[int] = mapped_column(
        OrderPaymentMethodColumns.ORDER_PAYMENT_METHOD_ID, primary_key=True
    )
    amount_paid: Mapped[Numeric] = mapped_column(
        OrderPaymentMethodColumns.AMOUNT_PAID, Numeric(10, 2), nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        OrderColumns.ORDER_ID, ForeignKey("Ordenes.OrdenID"), nullable=False
    )
    payment_method_id: Mapped[int] = mapped_column(
        PaymentMethodColumns.PAYMENT_METHOD_ID,
        ForeignKey("MetodosPago.MetodoPagoID"),
        nullable=False,
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            order_payment_method_id=data.get("order_payment_method_id"),
            amount_paid=Decimal(data.get("amount_paid", 0)),
            order_id=data.get("order_id"),
            payment_method_id=data.get("payment_method_id"),
        )
