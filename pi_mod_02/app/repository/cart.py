from requests import Session
from app.models.cart import Cart


class CartRepository:
    @staticmethod
    def save(db: Session, data: dict) -> Cart:
        return Cart.save_to_db(db, data)