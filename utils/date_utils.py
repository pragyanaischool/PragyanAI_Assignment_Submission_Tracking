# utils/date_utils.py

from datetime import datetime


def is_overdue(due_date):
    return datetime.now() > due_date


def days_remaining(due_date):
    return (due_date - datetime.now()).days


def format_date(date):
    return date.strftime("%Y-%m-%d")
