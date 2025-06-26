from models.base import BaseModel

class Customer(BaseModel):
    table = "customers"
    fields = ["name", "email", "registration_date"]