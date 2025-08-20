from sqlalchemy import ForeignKey, Integer, TIMESTAMP, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel
from app.models.constants import (
    ProductReviewColumns,
    ProductColumns,
    TableNames,
    UserColumns,
)
from app.models.users import User
from app.models.products import Product
import datetime


class ProductReview(BaseModel):
    __tablename__ = TableNames.REVIEWS
    __table_args__ = (
        CheckConstraint(
            f"{ProductReviewColumns.RATING} >= 1 AND {ProductReviewColumns.RATING} <= 5",
            name="rating_range",
        ),
    )

    review_id: Mapped[int] = mapped_column(
        ProductReviewColumns.REVIEW_ID, primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ProductColumns.PRODUCT_ID,
        ForeignKey("Productos.ProductoID"),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        UserColumns.USER_ID, ForeignKey("Usuarios.UsuarioID"), nullable=False
    )
    rating: Mapped[int] = mapped_column(
        ProductReviewColumns.RATING,
        Integer,
        nullable=False,
    )
    comment: Mapped[str] = mapped_column(
        ProductReviewColumns.COMMENT, String, nullable=True
    )
    date_created: Mapped[str] = mapped_column(
        ProductReviewColumns.REVIEW_DATE,
        TIMESTAMP,
        nullable=False,
    )

    product: Mapped["Product"] = relationship("Product", backref="reviews")
    user: Mapped["User"] = relationship("User", backref="reviews")

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            review_id=data.get("review_id"),
            product_id=data.get("product_id"),
            user_id=data.get("user_id"),
            rating=data.get("rating", 0),
            comment=data.get("comment", "").strip(),
            date_created=data.get("date_created", datetime.datetime.now()),
        )
