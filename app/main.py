from typing import Union
from app.models import User
from fastapi import FastAPI
from app.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test")
def test_read_root(db: Session = Depends(get_db)):

    form_exists = (
            db.query(User)
            .filter(
                and_(
                    User.id == 1,
                    User.deleted == 0,
                    User.record_status == 1,
                )
            )
            .first()
        )
    if form_exists:
        return {"Hello": "form_exists"}
    
    return {"Hello": "form_does_not_exists"}
