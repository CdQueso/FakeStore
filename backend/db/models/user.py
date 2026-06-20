from sqlalchemy import Column, Integer, String, Float
from db.schemas.client import Base


class Producto(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    nickname = Column(Float)
    email = Column(String(50))
