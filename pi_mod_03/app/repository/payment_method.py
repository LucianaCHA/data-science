from requests import Session
from app.models.payment_methods import PaymentMethod


class PaymentMethodRepository:
    @staticmethod
    def save(db: Session, data: dict) -> PaymentMethod:
        return PaymentMethod.save_to_db(db, data)
