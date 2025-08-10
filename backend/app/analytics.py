
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models
import pandas as pd

analytics = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@analytics.get("/analytics/missing")
def missing_report(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    if not students:
        return {"columns": [], "rows": [], "index": []}
    rows = []
    for s in students:
        rec = s.data or {}
        rows.append(rec)
    df = pd.DataFrame(rows).fillna(value=pd.NA)
    bool_df = df.isna().astype(int)
    columns = list(df.columns)
    matrix = bool_df.values.tolist()
    index = [str(i) for i in df.index]
    return {"columns": columns, "rows": matrix, "index": index}
