from requests import Session
from app.models.categories import Category


class CategoryRepository:
    @staticmethod
    def save(db: Session, data: dict) -> Category:
        return Category.save_to_db(db, data)
