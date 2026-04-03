# utils/helpers.py

import uuid
from datetime import datetime


def generate_id():
    return str(uuid.uuid4())


def current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_get(dictionary, key, default=None):
    return dictionary.get(key, default)
