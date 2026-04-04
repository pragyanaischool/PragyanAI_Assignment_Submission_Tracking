# modules/submission.py

import streamlit as st
from datetime import datetime
import uuid

from config.settings import SUBMISSIONS_FILE, UPLOAD_DIR, ALLOWED_FILE_TYPES
from database.db_manager import insert_row
from database.validators import validate_submission, validate_file


# ==============================
# 📁 SAVE FILE
# ==============================

def save_uploaded_file(file, usn, test_id):
    if file is None:
        return None

    validate_file(file.name, ALLOWED_FILE_TYPES)

    folder_path = f"{UPLOAD_DIR}/{usn}/{test_id}"
    import os
    os.makedirs(folder_path, exist_ok=True)

    #file_path = f"{folder_path}/{file.name}"
    
    file_path = f"{folder}/{uuid.uuid4()}_{file.name}"
    with open(file_path, "wb") as f:
        f.write(file.read())

    return file_path


# ==============================
# 📤 SUBMISSION PAGE
# ==============================

def submission_page(user, test_id):
    st.title(f"📤 Submit Assignment: {test_id}")

    usn = user["USN"]

    st.write("Upload your assignment file or paste your answer below.")

    # File upload
    uploaded_file = st.file_uploader(
        "Upload File (PDF / DOCX / TXT / Image)",
        type=ALLOWED_FILE_TYPES
    )

    # Text input
    text_response = st.text_area("Or paste your answer")

    st.divider()

    if st.button("🚀 Submit"):
        try:
            # Validate
            submission_data = {
                "USN": usn,
                "Assignment_ID": test_id,
                "Mode": "upload",
            }
            validate_submission(submission_data)

            # Save file
            file_path = save_uploaded_file(uploaded_file, usn, test_id)

            # Generate submission ID
            submission_id = str(uuid.uuid4())

            # Insert into DB
            insert_row(SUBMISSIONS_FILE, {
                "Submission_ID": submission_id,
                "USN": usn,
                "Assignment_ID": test_id,
                "Mode": "upload",
                "File_Path": file_path,
                "Text_Response": text_response,
                "Submitted_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "submitted",
            })

            st.success("✅ Submission successful!")

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
