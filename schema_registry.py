# schema_registry.py

"""
Schema Registry for Dynamic ETL Pipeline (MongoDB-first)

This module stores and retrieves schema versions from MongoDB.
Each schema entry looks like:

{
  "_id": ObjectId(),
  "version_ts": "<ISO UTC timestamp>",
  "schema": { "field": "type", "field2.sub": "type", ... },
  "diff_from_prev": {...}
}
"""

from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, MONGO_DB, MONGO_SCHEMA_REG
from deepdiff import DeepDiff


def _client():
    return MongoClient(MONGO_URI)


# Convert Python type objects to string type names
def infer_schema(record: dict):
    schema = {}
    for k, v in record.items():
        schema[k] = type(v).__name__
    return schema


def merge_schemas(old: dict, new: dict):
    merged = dict(old or {})
    for k, t in new.items():
        if k not in merged:
            merged[k] = t
        else:
            if merged[k] != t:
                merged[k] = "mixed"
    return merged


def diff_schemas(old: dict, new: dict):
    return DeepDiff(old or {}, new or {}, ignore_order=True) or None


# ⭐ REQUIRED FUNCTION 1
def get_latest_schema():
    client = _client()
    coll = client[MONGO_DB][MONGO_SCHEMA_REG]

    doc = coll.find_one(sort=[("version_ts", -1)])
    client.close()
    return doc


# ⭐ REQUIRED FUNCTION 2
def record_new_schema(schema: dict, diff=None):
    client = _client()
    coll = client[MONGO_DB][MONGO_SCHEMA_REG]

    doc = {
        "version_ts": datetime.utcnow().isoformat() + "Z",
        "schema": schema,
        "diff_from_prev": diff
    }

    coll.insert_one(doc)
    client.close()
