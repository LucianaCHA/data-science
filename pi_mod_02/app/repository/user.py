from requests import Session
from app.models.users import User


class UserRepository:
    @staticmethod
    def get_by_dni(db: Session, dni: str) -> User:
        return db.query(User).filter_by(dni=dni).first()

    @staticmethod
    def save(db: Session, data: dict) -> User:
        return User.save_to_db(db, data)
        # user = User.from_dict(data)
        # db.add(user)
        # db.commit()
        # return user
