from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from db.schemas.client import get_db
from db.models.user import Usuario
from db.schemas.schema import UsuarioResponse, UsuarioCreate

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
# openssl rand -hex 32
SECRET = "a6207e2215500bdce86c944b0161b4d4db12cb1d941f720bee3adc7c1bc2eb47"

router = APIRouter(prefix="/users")

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=list[UsuarioResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(Usuario).all()


@router.get("/{id}", response_model=list[UsuarioResponse])
async def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuarion no encontrado")
    return user


@router.post("/", response_model=UsuarioResponse)
async def post_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    nuevo = Usuario(**user.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
