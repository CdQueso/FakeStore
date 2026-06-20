from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Ajustá estos valores a tu SQL Server
SERVER = "DESKTOP-SQ7ICBB\SQLEXPRESS"
DATABASE = "FakeStore"

CONNECTION_STRING = (
    f"mssql+pyodbc://{SERVER}/{DATABASE}"
    f"?driver=ODBC+Driver+17+for+SQL+Server"
    f"&trusted_connection=yes"  # usa tu usuario de Windows
)

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


# Dependencia para las rutas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
