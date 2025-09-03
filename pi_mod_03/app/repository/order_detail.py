from requests import Session
from app.models.orders_detail import OrderDetail


class OrderDetailRepository:
    @staticmethod
    def save(db: Session, data: dict) -> OrderDetail:
        return OrderDetail.save_to_db(db, data)
