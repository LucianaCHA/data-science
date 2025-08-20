from sqlalchemy import String, ForeignKey, Numeric, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.base import BaseModel
from app.models.constants import TableNames, OrderColumns, UserColumns
from app.models.users import User


class Order(BaseModel):
    __tablename__ = TableNames.ORDERS

    order_id: Mapped[int] = mapped_column(
        OrderColumns.ORDER_ID, primary_key=True, autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        UserColumns.USER_ID, ForeignKey("Usuarios.UsuarioID"), nullable=False
    )

    user: Mapped["User"] = relationship("User", backref="orders")

    order_date: Mapped[str] = mapped_column(
        OrderColumns.ORDER_DATE, TIMESTAMP, nullable=False
    )
    total: Mapped[float] = mapped_column(
        OrderColumns.TOTAL, Numeric(10, 2), nullable=False
    )
    status: Mapped[str] = mapped_column(
        OrderColumns.STATUS, String(50), default="Pendiente"
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            order_id=data.get("order_id"),
            user_id=data.get("user_id"),
            order_date=data.get("order_date"),
            total=data.get("total", 0.0),
            status=data.get("status", "Pendiente"),
        )
