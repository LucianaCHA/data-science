from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import BaseModel


class DataLoad(BaseModel):
    __tablename__ = "data_loads_audit"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    status = Column(String, default="successful")
    load_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, file_name, status="successful"):
        self.file_name = file_name
        self.status = status
