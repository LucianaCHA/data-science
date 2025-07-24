from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from app.db.base import BaseModel
from app.models.constants import TableNames, PaymentMethodColumns


class PaymentMethod(BaseModel):
    __tablename__ = TableNames.PAYMENT_METHODS

    payment_method_id: Mapped[int] = mapped_column(
        PaymentMethodColumns.PAYMENT_METHOD_ID, primary_key=True
    )
    name: Mapped[str] = mapped_column(
        PaymentMethodColumns.NAME, String(100), nullable=False
    )
    description: Mapped[str] = mapped_column(
        PaymentMethodColumns.DESCRIPTION, String(255), nullable=True
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            payment_method_id=data.get("payment_method_id"),
            name=data.get("name", "").strip(),
            description=data.get("description", "").strip(),
        )
