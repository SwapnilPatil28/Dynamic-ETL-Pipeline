import os
from pymongo import MongoClient
from deepdiff import DeepDiff
from config import MONGO_URI, MONGO_DB, MONGO_COLLECTION, ARCHIVE_DIR
from utils import safe_value   # ⛔️ removed old file_hash usage
from schema_registry import get_latest_schema, record_new_schema
from parsers.json_parser import parse_json
from parsers.csv_parser import parse_csv
from parsers.xml_parser import parse_xml
from parsers.html_parser import parse_html
from parsers.text_parser import parse_text

import hashlib
from datetime import datetime


# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def now_iso():
    return datetime.utcnow().isoformat() + Z


# -------------------------------------------------------
# Duplicate Detection
# -------------------------------------------------------

def is_duplicate_file(file_hash):
    client = MongoClient(MONGO_URI)
    coll = client[MONGO_DB]["file_registry"]
    exists = coll.find_one({"hash": file_hash})
    client.close()
    return exists is not None


def store_file_registry(filename, file_hash):
    client = MongoClient(MONGO_URI)
    coll = client[MONGO_DB]["file_registry"]
    coll.insert_one({
        "filename": filename,
        "hash": file_hash,
        "uploaded_at": now_iso()
    })
    client.close()


# -------------------------------------------------------
# File Deletion (for UI delete button)
# -------------------------------------------------------

def delete_file(file_hash):
    client = MongoClient(MONGO_URI)
    coll = client[MONGO_DB][MONGO_COLLECTION]

    # remove ingested records
    deleted_records = coll.delete_many({"_file_hash": file_hash}).deleted_count

    # remove registry entry
    reg = client[MONGO_DB]["file_registry"]
    reg_deleted = reg.delete_many({"hash": file_hash}).deleted_count

    client.close()

    # remove archived file
    archived_deleted = False
    for fname in os.listdir(ARCHIVE_DIR):
        if fname.startswith(file_hash):
            os.remove(os.path.join(ARCHIVE_DIR, fname))
            archived_deleted = True

    return {
        "data_records_deleted": deleted_records,
        "registry_deleted": reg_deleted,
        "archive_deleted": archived_deleted,
    }


# -------------------------------------------------------
# Parsing
# -------------------------------------------------------

def detect_format(filename):
    return filename.lower().split(".")[-1]


def parse_unstructured(filename, raw):
    ext = detect_format(filename)

    if ext == "json":
        return parse_json(raw)
    if ext == "csv":
        return parse_csv(raw)
    if ext == "xml":
        return parse_xml(raw)
    if ext in ["html", "htm"]:
        return parse_html(raw)
    if ext in ["txt", "log"]:
        return parse_text(raw)

    return parse_text(raw)


# -------------------------------------------------------
# Transform (Flatten)
# -------------------------------------------------------

def flatten_dict(d: dict, parent="", sep="."):
    out = {}
    for k, v in d.items():
        key = f"{parent}{sep}{k}" if parent else k

        if isinstance(v, dict):
            out.update(flatten_dict(v, key, sep))

        elif isinstance(v, list):
            for i, item in enumerate(v):
                out.update(flatten_dict({str(i): item}, key, sep))

        else:
            out[key] = safe_value(v)

    return out


def transform(records):
    return [flatten_dict(r) for r in records]


# -------------------------------------------------------
# Load
# -------------------------------------------------------

def load(records, file_hash):
    client = MongoClient(MONGO_URI)
    coll = client[MONGO_DB][MONGO_COLLECTION]

    # add file hash to each record
    for r in records:
        r["_file_hash"] = file_hash

    # Infer schema dynamically
    new_schema = {}
    for r in records:
        for k, v in r.items():
            new_schema[k] = type(v).__name__

    latest = get_latest_schema()
    old_schema = latest["schema"] if latest else None

    diff = DeepDiff(old_schema or {}, new_schema, ignore_order=True) or None
    if diff:
        record_new_schema(new_schema, diff)

    # Insert into DB
    res = coll.insert_many(records)
    return len(res.inserted_ids)


# -------------------------------------------------------
# MAIN ETL FUNCTION
# -------------------------------------------------------

def process_file(uploaded):
    raw = uploaded.read()
    filename = uploaded.name

    # REAL SHA-256 HASH (fix)
    file_hash = hashlib.sha256(raw).hexdigest()

    # Duplicate check
    if is_duplicate_file(file_hash):
        return {
            "filename": filename,
            "hash": file_hash,
            "inserted": 0,
            "message": "Duplicate file detected → Skipped ETL."
        }

    # Parse → Transform → Load
    records = parse_unstructured(filename, raw)
    transformed = transform(records)
    inserted = load(transformed, file_hash)

    # Record successful upload in registry
    store_file_registry(filename, file_hash)

    # Save archive
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    with open(f"{ARCHIVE_DIR}/{file_hash}_{filename}", "wb") as f:
        f.write(raw)

    return {
        "filename": filename,
        "hash": file_hash,
        "inserted": inserted,
        "message": "File processed successfully"
    }
