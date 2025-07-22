from sqlalchemy import TIMESTAMP, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.db.base import BaseModel
from app.models.constants import TableNames, CartColumns, UserColumns, ProductColumns
from app.models.users import User
from app.models.products import Product
import datetime


class Cart(BaseModel):
    __tablename__ = TableNames.CART
    __table_args__ = (
        CheckConstraint(f"{CartColumns.QUANTITY} > 0", name="quantity_positive"),
    )

    cart_id: Mapped[int] = mapped_column(CartColumns.CART_ID, primary_key=True)
    quantity: Mapped[int] = mapped_column(
        CartColumns.QUANTITY, Integer, nullable=False)
    added_at: Mapped[str] = mapped_column(
        CartColumns.ADDED_AT, TIMESTAMP, nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        ProductColumns.PRODUCT_ID,
        ForeignKey("Productos.ProductoID"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        UserColumns.USER_ID, ForeignKey("Usuarios.UsuarioID"), nullable=False
    )

    user: Mapped["User"] = relationship("User", backref="cart")
    product: Mapped["Product"] = relationship("Product", backref="cart")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            cart_id=data.get("cart_id"),
            quantity=data.get("quantity"),
            added_at=data.get("added_at", datetime.datetime.now()),
            product_id=data.get("product_id"),
            user_id=data.get("user_id"),
        )
