
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app import models
import pandas as pd
import io
from app.audit import record_audit

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def df_to_records(df: pd.DataFrame):
    # normalize column names
    df.columns = [str(c).strip() for c in df.columns]
    records = []
    for _, row in df.iterrows():
        rec = {col: (row[col] if not pd.isna(row[col]) else None) for col in df.columns}
        records.append(rec)
    return records

def apply_students(records, db: Session, actor="importer"):
    for r in records:
        sid = str(r.get("student_id") or r.get("id") or r.get("studentid") or "")
        if not sid:
            # skip rows without an id
            continue
        existing = db.query(models.Student).filter(models.Student.student_id == sid).first()
        if existing:
            before = existing.data
            existing.data = r
            db.add(existing)
            db.commit()
            record_audit(db, "students", "UPDATE", actor, sid, before, r)
        else:
            s = models.Student(student_id=sid, data=r)
            db.add(s)
            db.commit()
            record_audit(db, "students", "INSERT", actor, sid, None, r)

@router.post("/upload")
async def upload_excel(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    try:
        df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
    except Exception:
        # try csv
        try:
            df = pd.read_csv(io.BytesIO(contents))
        except Exception:
            raise HTTPException(400, "Invalid file")
    records = df_to_records(df)
    # Dry-run: return counts and sample diff
    n_new = 0; n_update = 0
    for r in records:
        sid = str(r.get("student_id") or r.get("id") or r.get("studentid") or "")
        if not sid:
            continue
        if db.query(models.Student).filter(models.Student.student_id == sid).first():
            n_update += 1
        else:
            n_new += 1
    # For minimal flow, apply immediately using a background task
    background_tasks.add_task(apply_students, records, db, "uploader")
    return {"status": "started", "new": n_new, "updates": n_update}
