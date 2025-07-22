from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from app.db.base import BaseModel
from app.models.constants import TableNames, CategoryColumns


class Category(BaseModel):
    __tablename__ = TableNames.CATEGORIES

    category_id: Mapped[int] = mapped_column(
        CategoryColumns.CATEGORY_ID, primary_key=True)
    name: Mapped[str] = mapped_column(
        CategoryColumns.NAME, String(100), nullable=False)
    description: Mapped[str] = mapped_column(
        CategoryColumns.DESCRIPTION, String(255))

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            category_id=data.get("category_id"),
            name=data.get("name", "").strip(),
            description=data.get("description", "").strip(),
        )
