import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

USE_STORAGE = "mongo"

# Get values ONLY from environment variables
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
MONGO_SCHEMA_REG = os.getenv("MONGO_SCHEMA_REG")

ARCHIVE_DIR = os.getenv("ARCHIVE_DIR")
