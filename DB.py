from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://postgres:Bio2160cc.1607@localhost/clinical_db", echo=True
)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()
session.close()
