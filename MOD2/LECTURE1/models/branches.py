from models.base import BaseModel

class Branch(BaseModel):
    table = "branches"
    fields = ["name", "location"]

