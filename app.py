import streamlit as st
from etl_pipeline import process_file, delete_file
import pandas as pd

st.title("🌐 Universal Dynamic ETL Pipeline (MongoDB)")
st.write("Upload ANY unstructured data — JSON, CSV, XML, HTML, TXT — with duplicate prevention + deletion control.")

st.header("📤 Upload Files")
files = st.file_uploader("Upload files", accept_multiple_files=True)

if files:
    results = []
    for f in files:
        try:
            out = process_file(f)
            st.success(f"{f.name}: {out['message']} (Inserted: {out['inserted']})")
            results.append(out)
        except Exception as e:
            st.error(f"Error with {f.name}: {e}")

    if results:
        st.subheader("📄 Run Summary")
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)
        st.download_button("Download Summary CSV", df.to_csv(index=False), "summary.csv")


# -------------------------------------------------------
# Delete File Section
# -------------------------------------------------------

st.header("🗑 Delete File from Database")

delete_hash = st.text_input("Enter File Hash to Delete")

if st.button("Delete File"):
    if delete_hash.strip() == "":
        st.warning("Please enter a file hash.")
    else:
        try:
            result = delete_file(delete_hash)
            st.success(f"Deleted Records: {result['data_records_deleted']}, "
                       f"Registry Removed: {result['registry_deleted']}, "
                       f"Archive Deleted: {result['archive_deleted']}")
        except Exception as e:
            st.error(f"Delete failed: {e}")
