from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from db.schemas.client import get_db
from db.models.user import Usuario
from db.schemas.schema import UsuarioResponse, UsuarioCreate

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"message": "No encontrado"}}
)


# @router.get("/", response_model=list[UsuarioResponse])
# async def get_users(db: Session = Depends(get_db)):
#     return db.query(Usuario).all()


# @router.get("/{id}", response_model=list[UsuarioResponse])
# async def get_users(id: int, db: Session = Depends(get_db)):
#     user = db.query(Usuario).filter(Usuario.id == id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="Usuarion no encontrado")
#     return user
crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/", response_model=UsuarioResponse)
async def post_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    hash_pass = crypt.hash(user.password)
    user_data = user.model_dump(exclude={"password"})

    nuevo = Usuario(**user_data, password=hash_pass)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
