from requests import Session
from app.models.order_payment_methods import OrderPaymentMethod


class OrderPaymentMethodRepository:
    @staticmethod
    def save(db: Session, data: dict) -> OrderPaymentMethod:
        return OrderPaymentMethod.save_to_db(db, data)