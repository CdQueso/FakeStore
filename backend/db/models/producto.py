from sqlalchemy import Column, Integer, String, Float
from db.schemas.client import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    precio = Column(Float)
    categoria = Column(String(50))
