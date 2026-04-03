# utils/analytics.py

import pandas as pd


def completion_rate(df_tests, df_sub, usn):
    total = len(df_tests)
    completed = len(df_sub[df_sub["USN"] == usn])

    if total == 0:
        return 0

    return round((completed / total) * 100, 2)


def submission_count(df_sub):
    return df_sub.groupby("USN").size()


def test_participation(df_sub):
    return df_sub.groupby("Assignment_ID").size()
