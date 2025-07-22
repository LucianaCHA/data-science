from requests import Session
from app.models.orders import Order


class OrderRepository:
    @staticmethod
    def save(db: Session, data: dict) -> Order:
        return Order.save_to_db(db, data)
