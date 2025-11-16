import pandas as pd
from io import BytesIO

def parse_csv(raw: bytes):
    df = pd.read_csv(BytesIO(raw))
    return df.to_dict(orient="records")
