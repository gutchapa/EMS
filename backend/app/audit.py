
from app import models
import json

def record_audit(db_session, table_name, operation, changed_by, row_id, before, after):
    entry = models.AuditEntry(
        table_name=table_name,
        operation=operation,
        changed_by=str(changed_by),
        row_id=str(row_id),
        before=before,
        after=after
    )
    db_session.add(entry)
    db_session.commit()
