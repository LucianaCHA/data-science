from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def from_dict(cls, data: dict):
        """
        Método de clase para crear una instancia del modelo a partir de un diccionario.
        """
        return cls(**data)

    @classmethod
    def save_to_db(cls, db_session, data: dict):
        """
        Método de clase para guardar una instancia del modelo en la base de datos.
        """
        instance = cls.from_dict(data)
        db_session.add(instance)
        db_session.commit()
        return instance
