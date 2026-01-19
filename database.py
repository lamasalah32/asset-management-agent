from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import os

DATABASE_URL = "sqlite:///./data/assets.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#------------------
MEMORY_DB_PATH = "/app/data/agent_memory.db"

os.makedirs(os.path.dirname(MEMORY_DB_PATH), exist_ok=True)

sqlite_conn = sqlite3.connect(
    MEMORY_DB_PATH,
    check_same_thread=False
)

checkpointer = SqliteSaver(sqlite_conn)
checkpointer.setup()

