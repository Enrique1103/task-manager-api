from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:6374postgre@localhost:5432/tasks_BD"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()