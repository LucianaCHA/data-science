from sqlalchemy import ForeignKey, Numeric, TIMESTAMP, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel
from app.models.constants import (
    OrderColumns,
    PaymentHistoryColumns,
    TableNames,
)
from app.models.orders import Order
from app.models.payment_methods import PaymentMethod
import datetime
from decimal import Decimal


class PaymentHistory(BaseModel):
    __tablename__ = TableNames.PAYMENT_HISTORY

    payment_id: Mapped[int] = mapped_column(
        PaymentHistoryColumns.PAYMENT_ID, primary_key=True
    )
    order_id: Mapped[int] = mapped_column(
        OrderColumns.ORDER_ID, ForeignKey("Ordenes.OrdenID"), nullable=False
    )
    payment_method_id: Mapped[int] = mapped_column(
        PaymentHistoryColumns.PAYMENT_METHOD_ID,
        ForeignKey("MetodosPago.MetodoPagoID"),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(
        PaymentHistoryColumns.AMOUNT, Numeric(10, 2), nullable=False
    )
    date: Mapped[str] = mapped_column(
        PaymentHistoryColumns.PAYMENT_DATE,
        TIMESTAMP,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        PaymentHistoryColumns.PAYMENT_STATUS,
        String,
        nullable=False,
    )

    order: Mapped["Order"] = relationship("Order", backref="payment_history")
    payment_method: Mapped["PaymentMethod"] = relationship(
        "PaymentMethod", backref="payment_history"
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            payment_id=data.get("payment_id"),
            order_id=data.get("order_id"),
            payment_method_id=data.get("payment_method_id"),
            amount=Decimal(data.get("amount", 0)),
            date=data.get("date", datetime.datetime.now()),
            status=data.get("status", "Procesando"),
        )
