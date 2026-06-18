from pydantic import BaseModel


class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    categoria: str


class ProductoResponse(ProductoCreate):
    id: int

    class Config:
        from_attributes = True
