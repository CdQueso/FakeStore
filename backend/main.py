from fastapi import FastAPI
from routers import productos, users
from db.schemas.client import Base, engine
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(responses=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(productos.router)
app.include_router(users.router)


@app.get("/")
async def read_root():
    return {"hello": "world"}
