import urllib.parse

from fastapi import Depends, FastAPI, Request
#from pydantic import BaseModel
from sqlalchemy import create_engine, text, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# SQLAlchemy Model
class Sequence(Base):
    __tablename__ = "sequence"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=True, index=True)

def is_sequence_in_db(db: Session, sequence: str) -> bool:
    exists = db.query(Sequence).filter(Sequence.value == sequence).first()
    if exists is None:
        return False
    else:
        return True

def add_sequence_to_db(db: Session, sequence: str):
    sequence = Sequence(value = sequence)
    db.add(sequence)
    db.commit()
    db.refresh(sequence)
    return

def clear_db(db: Session):
    # SQLite has no TRUNCATE option
    #db.execute(text("TRUNCATE TABLE sequence;"))
    db.commit()
    # Crude: Drop table & recreate
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return

# Create Database
Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# FastAPI application
app = FastAPI()

#@app.middleware("http")
#async def modify_description(request: Request, call_next):
#    response = await call_next(request)
#    return response

@app.post("/sequence/{sequence}", status_code=200, status_phrase="Message received")
async def check_sequence(sequence: str, db: Session = Depends(get_db)):
    # URL Decode the String
    sequence = urllib.parse.unquote(sequence)
    # Is string in DB?
    if is_sequence_in_db(db, sequence):
        # We have seen this sequence already
        duplicate = True
    else:
        # New sequence
        duplicate = False
        # Add string to DB
        add_sequence_to_db(db, sequence)
    
    body = {"duplicate": duplicate,
            }
    # RFC2616
    # Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF
    #body = json.dumps(body)
    #return f"HTTP/1.1 200 Message received\r\n\r\n{body}"
    return body

@app.put("/clear", status_code=200, status_phrase="Deduplication history cleared")
async def clear(db: Session = Depends(get_db)):
    # Clear the Database
    clear_db(db)
    # RFC2616
    # Status-Line = HTTP-Version SP Status-Code SP Reason-Phrase CRLF
    #return "HTTP/1.1 200 Deduplication history cleared\r\n"
    return ""
