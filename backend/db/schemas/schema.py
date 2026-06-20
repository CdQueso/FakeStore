from pydantic import BaseModel


class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    categoria: str


class ProductoResponse(ProductoCreate):
    id: int

    class Config:
        from_attributes = True


class UsuarioCreate(BaseModel):
    nombre: str
    nickname: str
    email: str
    password: str


class UsuarioResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True
