# 🌐 Dynamic ETL Pipeline for Unstructured Data (MongoDB)

This project is a **universal, format-agnostic ETL pipeline** that processes unstructured files and converts them into clean, structured records stored in MongoDB.

The system:

* Accepts multiple unstructured file formats
* Detects duplicates using hashing
* Extracts relevant content
* Transforms nested structures into flattened JSON documents
* Loads transformed records into MongoDB
* Tracks schemas over time
* Archives original uploaded files
* Provides a simple Streamlit UI for uploading, processing, and deleting files

The goal is to simulate a **real, flexible ETL pipeline** that adapts to unpredictable incoming data.

---

## 🚀 Features (What the Project ACTUALLY Does)

### ✔ Supports Multiple File Types

* JSON
* CSV
* XML
* HTML
* TXT / LOG
* Unknown formats → handled as plain text

### ✔ Dynamic Schema Tracking

* Every file is parsed and converted to Python dicts
* The system automatically infers field names and data types
* Schema differences are detected with DeepDiff
* Each new schema version is stored in MongoDB

### ✔ Duplicate File Detection

* Each uploaded file is hashed (SHA-256)
* If the same file is uploaded again → **it is skipped**

### ✔ Flattening of Nested Data

All parsed records are normalized into flat key–value pairs so MongoDB can store them efficiently.

**Example:**

```
{
  "user": {
    "name": "Alice",
    "address": { "city": "Mumbai", "pin": 400001 }
  }
}
```

**Flattened:**

```
{
  "user.name": "Alice",
  "user.address.city": "Mumbai",
  "user.address.pin": 400001
}
```

### ✔ MongoDB Storage

Each cleaned record is inserted into MongoDB with `_file_hash` so deletion is possible later.

### ✔ File Archiving

Every uploaded file is saved in:

```
archive/<hash>_<filename>
```

### ✔ Web Interface

The Streamlit UI supports:

* File upload
* Multi-file processing
* Summary table
* CSV export
* Delete-by-hash input

---

## 🧩 Project Structure

```
Dynamic-ETL-Pipeline/
│
├── app.py                    # Streamlit web interface (main entry point)
├── etl_pipeline.py           # Core ETL logic (Extract, Transform, Load)
├── schema_registry.py        # Schema versioning and tracking
├── config.py                 # Configuration management with dotenv
├── utils.py                  # Helper functions (hashing, date, safe values)
├── requirements.txt          # Python dependencies
├── README.md                 
│
├── parsers/                  # Format-specific parsers
│   ├── json_parser.py        # JSON → dict/list
│   ├── csv_parser.py         # CSV → records (via pandas)
│   ├── xml_parser.py         # XML → nested dicts (via lxml)
│   ├── html_parser.py        # HTML → structured content (via BeautifulSoup)
│   ├── text_parser.py        # TXT → raw text with metadata
│   └── __pycache__/          # Python bytecode cache
│
├── sample_data/              # Example files for testing
│   ├── sample.json
│   ├── sample.csv
│   ├── sample.xml
│   ├── sample.html
│   └── sample.txt
│
├── archive/                  # Processed files archived by SHA-256 hash
│   └── <hash>_<filename>     # Auto-generated during processing
│
├── venv/                     # Virtual environment (if created)
├── __pycache__/              # Python bytecode cache
├── .git/                     # Git repository data
└── .gitattributes            # Git configuration
```

---

## 📤 Example Outputs

### 🟢 First Upload

```
sample.json: File processed successfully (Inserted: 2)
sample.csv: File processed successfully (Inserted: 2)
sample.xml: File processed successfully (Inserted: 1)
sample.html: File processed successfully (Inserted: 1)
sample.txt: File processed successfully (Inserted: 1)
```

### Summary Table

| filename    | hash            | inserted | message                     |
| ----------- | --------------- | -------- | --------------------------- |
| sample.json | 81a9fbb7a91c98… | 2        | File processed successfully |
| sample.csv  | c0b2e9d2df72e2… | 2        | File processed successfully |
| sample.xml  | 3d09e6ca812cfb… | 1        | File processed successfully |
| sample.html | 4b7c912e6c847f… | 1        | File processed successfully |
| sample.txt  | 1a6f30dfd9377a… | 1        | File processed successfully |

---

## 🔁 Duplicate Upload Example

```
sample.json: Duplicate file detected → Skipped ETL. (Inserted: 0)
sample.csv: Duplicate file detected → Skipped ETL. (Inserted: 0)
sample.xml: Duplicate file detected → Skipped ETL. (Inserted: 0)
sample.html: Duplicate file detected → Skipped ETL. (Inserted: 0)
sample.txt: Duplicate file detected → Skipped ETL. (Inserted: 0)
```

MongoDB stays clean—no duplicates.

---

## 🗑 File Deletion Example

**Input hash:**

```
90a229a47a1cfb...
```

**Output:**

```
Deleted Records: 2
Registry Removed: 1
Archive Deleted: True
```

---

## 🧠 Why This Project Is Useful

* Handles unpredictable unstructured files
* Creates structured, queryable MongoDB data
* Detects and prevents duplicates
* Tracks schema evolution
* Good learning project for ETL and data pipelines

---

## 👨‍💻 Author

**Swapnil Patil**

## 👨‍💻 Members of the Team

**Harsh Rai**

**Ekansh Melwani**
