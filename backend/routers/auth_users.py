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
ACCESS_TOKEN_DURATION = 30
# openssl rand -hex 32
SECRET = "a6207e2215500bdce86c944b0161b4d4db12cb1d941f720bee3adc7c1bc2eb47"

router = APIRouter(
    prefix="/users", tags=["jwtauth"], responses={404: {"message": "No Encontrado"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="users/login")

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


async def auth_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW.Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    user = db.query(Usuario).filter(Usuario.nombre == username).first()
    if user is None:
        raise exception

    return user


async def current_user(user: Usuario = Depends(auth_user)):
    return user


@router.get("/me", response_model=UsuarioResponse)
async def get_user(user: Usuario = Depends(current_user)):
    return user


@router.post("/login", response_model=Token)
async def login(
    db: Session = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()
):
    user = db.query(Usuario).filter(Usuario.nombre == form.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcta"
        )

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña es incorrecta",
        )

    access_token = {
        "sub": user.nombre,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer",
    }
