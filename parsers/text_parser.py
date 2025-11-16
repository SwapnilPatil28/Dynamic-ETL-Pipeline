def parse_text(raw: bytes):
    text = raw.decode("utf-8", errors="ignore")
    return [{"raw_text": text, "length": len(text)}]
