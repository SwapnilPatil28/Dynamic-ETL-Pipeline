import hashlib
from datetime import datetime
import pandas as pd

def now_iso():
    return datetime.utcnow().isoformat() + Z

def file_hash(content: bytes):
    h = hashlib.sha256()
    h.update(content)
    return h.hexdigest()

def safe_value(v):
    if isinstance(v, float) and pd.isna(v):
        return None
    return v
