from requests import Session
from app.models.products import Product


class ProductRepository:
    @staticmethod
    def save(db: Session, data: dict) -> Product:
        return Product.save_to_db(db, data)