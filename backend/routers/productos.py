from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.schemas.client import get_db
from db.models.producto import Producto
from db.schemas.schema import ProductoResponse

router = APIRouter(
    prefix="/productos",
    tags=["productos"],
    responses={404: {"message": "No Encontrado"}},
)


class ProductoCreate(BaseModel):
    nombre: str
    precio: int
    categoria: str


@router.get("/", response_model=list[ProductoResponse])
def get_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@router.get("/{id}", response_model=ProductoResponse)
def get_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.post("/", response_model=ProductoResponse)
def agregar(product: ProductoCreate, db: Session = Depends(get_db)):
    nuevo = Producto(
        nombre=product.nombre, precio=product.precio, categoria=product.categoria
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.put("/{id}", response_model=ProductoResponse)
def actualizar(id: int, product: ProductoCreate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto.nombre = product.nombre
    producto.precio = product.precio
    producto.categoria = product.categoria
    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto)
    db.commit()
    return {"ok": "Producto eliminado"}
