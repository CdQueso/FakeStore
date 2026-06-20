from sqlalchemy import Column, Integer, String, Float
from db.schemas.client import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    nickname = Column(String(100))
    email = Column(String(50))
    password = Column(String(50))
