from requests import Session
from app.models.delivery_addresses import DeliveryAddress


class DeliveryAddressRepository:
    @staticmethod
    def save(db: Session, data: dict) -> DeliveryAddress:
        return DeliveryAddress.save_to_db(db, data)
