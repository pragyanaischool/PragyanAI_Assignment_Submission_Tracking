# database/migrations.py

import os
import pandas as pd
from datetime import datetime

from config.settings import (
    USERS_FILE,
    ASSIGNMENTS_FILE,
    SUBMISSIONS_FILE,
    TEST_SESSIONS_FILE,
    QUESTION_LOGS_FILE,
    DEFAULT_ADMIN_ID,
    DEFAULT_ADMIN_PASSWORD,
)

from database.schema import (
    USERS_SCHEMA,
    ASSIGNMENTS_SCHEMA,
    SUBMISSIONS_SCHEMA,
    TEST_SESSIONS_SCHEMA,
    QUESTION_LOGS_SCHEMA,
    empty_dataframe,
)


# ==============================
# 📁 CREATE FILE IF NOT EXISTS
# ==============================

def create_file_if_not_exists(file_path, schema):
    """Create Excel file with schema if not exists"""
    if not os.path.exists(file_path):
        df = empty_dataframe(schema)
        df.to_excel(file_path, index=False)
        print(f"Created: {file_path}")


# ==============================
# 👤 CREATE DEFAULT ADMIN
# ==============================

def create_default_admin():
    """Insert default admin if not exists"""
    df = pd.read_excel(USERS_FILE)

    if df.empty or DEFAULT_ADMIN_ID not in df["User_ID"].values:
        admin_data = {
            "User_ID": DEFAULT_ADMIN_ID,
            "Name": "Admin",
            "USN": DEFAULT_ADMIN_ID,
            "Email": "admin@pragyanai.com",
            "Password": DEFAULT_ADMIN_PASSWORD,
            "Role": "admin",
            "Approved": True,
            "Created_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        df = pd.concat([df, pd.DataFrame([admin_data])], ignore_index=True)
        df.to_excel(USERS_FILE, index=False)

        print("Default admin created")


# ==============================
# 🔄 RUN ALL MIGRATIONS
# ==============================

def run_migrations():
    """Initialize all database files"""

    print("Running database migrations...")

    create_file_if_not_exists(USERS_FILE, USERS_SCHEMA)
    create_file_if_not_exists(ASSIGNMENTS_FILE, ASSIGNMENTS_SCHEMA)
    create_file_if_not_exists(SUBMISSIONS_FILE, SUBMISSIONS_SCHEMA)
    create_file_if_not_exists(TEST_SESSIONS_FILE, TEST_SESSIONS_SCHEMA)
    create_file_if_not_exists(QUESTION_LOGS_FILE, QUESTION_LOGS_SCHEMA)

    create_default_admin()

    print("All migrations completed successfully!")


# ==============================
# 🚀 AUTO RUN (OPTIONAL)
# ==============================

if __name__ == "__main__":
    run_migrations()
