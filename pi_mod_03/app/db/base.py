from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def from_dict(cls, data: dict):
        """
        Create an instance of the model from a dictionary.
        """
        return cls(**data)

    @classmethod
    def save_to_db(cls, db_session, data: dict):
        """
        Saves a model instance to the database.
        """
        instance = cls.from_dict(data)
        db_session.add(instance)
        db_session.commit()
        return instance
