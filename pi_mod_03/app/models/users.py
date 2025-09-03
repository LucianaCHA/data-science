from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql import func
from app.db.base import BaseModel
from sqlalchemy import DateTime
import datetime

from app.models.constants import TableNames, UserColumns


class User(BaseModel):
    __tablename__ = TableNames.USERS

    user_id: Mapped[int] = mapped_column(
        UserColumns.USER_ID, Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        UserColumns.NAME, String(100), nullable=False)
    surname: Mapped[str] = mapped_column(
        UserColumns.SURNAME, String(100), nullable=False
    )
    dni: Mapped[str] = mapped_column(
        UserColumns.DNI, String(20), unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        UserColumns.EMAIL, String(255), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(
        UserColumns.PASSWORD, String(255), nullable=False
    )
    registration_date: Mapped["datetime.datetime"] = mapped_column(
        UserColumns.REGISTRATION_DATE,
        DateTime,
        default=func.current_timestamp(),
        nullable=False,
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=data.get("user_id"),
            name=data.get("name", "").strip(),
            surname=data.get("surname", "").strip(),
            dni=data.get("dni", "").strip(),
            email=data.get("email", "").strip().lower(),
            password=data.get("password", ""),
        )
