from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import BaseModel
from app.models.constants import (
    DeliveryAddressColumns,
    TableNames,
    UserColumns,
)
from app.models.users import User


class DeliveryAddress(BaseModel):

    __tablename__ = TableNames.DELIVERY_ADDRESS

    address_id: Mapped[int] = mapped_column(
        DeliveryAddressColumns.DELIVERY_ADDRESS_ID, primary_key=True
    )
    street: Mapped[str] = mapped_column(
        DeliveryAddressColumns.STREET, String(100), nullable=False
    )
    city: Mapped[str] = mapped_column(
        DeliveryAddressColumns.CITY, String(100), nullable=False
    )
    department: Mapped[str] = mapped_column(
        DeliveryAddressColumns.DEPARMENT, String(100), nullable=True
    )
    province: Mapped[str] = mapped_column(
        DeliveryAddressColumns.PROVINCE, String(100), nullable=True
    )
    state: Mapped[str] = mapped_column(
        DeliveryAddressColumns.STATE, String(100), nullable=True
    )
    district: Mapped[str] = mapped_column(
        DeliveryAddressColumns.DISTRICT, String(100), nullable=True
    )
    zip_code: Mapped[str] = mapped_column(
        DeliveryAddressColumns.ZIP_CODE, String(20), nullable=True
    )
    country: Mapped[str] = mapped_column(
        DeliveryAddressColumns.COUNTRY, String(100), nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        UserColumns.USER_ID, ForeignKey("Usuarios.UsuarioID"), nullable=False
    )

    user: Mapped["User"] = relationship(
        "User", backref="delivery_addresses", foreign_keys=[user_id]
    )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            address_id=data.get('address_id'),
            user_id=data.get("user_id"),
            street=data.get("street", "").strip(),
            city=data.get("city", "").strip(),
            department=data.get("department", "").strip(),
            province=data.get("province", "").strip(),
            district=data.get("district", "").strip(),
            state=data.get("state", "").strip(),
            zip_code=data.get("zip_code", "").strip(),
            country=data.get("country", "").strip(),
        )
