# agents/session_tracker_agent.py

from database.db_manager import insert_row
from config.settings import TEST_SESSIONS_FILE, QUESTION_LOGS_FILE
from datetime import datetime


def log_test_session(session_id, usn, test_id, start_time, end_time):
    total_time = (end_time - start_time).total_seconds()

    insert_row(TEST_SESSIONS_FILE, {
        "Session_ID": session_id,
        "USN": usn,
        "Assignment_ID": test_id,
        "Start_Time": start_time,
        "End_Time": end_time,
        "Total_Time": total_time,
        "Completed": True,
    })


def log_question_interaction(data: dict):
    insert_row(QUESTION_LOGS_FILE, data)
