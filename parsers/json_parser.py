import json

def parse_json(raw: bytes):
    try:
        data = json.loads(raw)
    except Exception:
        data = json.loads(raw.decode("utf-8"))

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    return [{"value": data}]
