# database/db_manager.py

import pandas as pd
import os
from typing import Dict, Any


def load_data(file_path: str) -> pd.DataFrame:
    """Load Excel file safely"""
    if not os.path.exists(file_path):
        return pd.DataFrame()
    return pd.read_excel(file_path)


def save_data(df: pd.DataFrame, file_path: str) -> None:
    """Save DataFrame to Excel"""
    df.to_excel(file_path, index=False)


def insert_row(file_path: str, row: Dict[str, Any]) -> None:
    """Insert a new row into Excel"""
    df = load_data(file_path)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    save_data(df, file_path)


def update_row(file_path: str, condition: Dict[str, Any], updates: Dict[str, Any]) -> None:
    """
    Update rows based on condition
    Example:
    condition = {"USN": "1RV21CS001"}
    updates = {"Approved": True}
    """
    df = load_data(file_path)

    if df.empty:
        return

    mask = pd.Series([True] * len(df))

    for col, val in condition.items():
        mask &= df[col] == val

    for col, val in updates.items():
        df.loc[mask, col] = val

    save_data(df, file_path)


def delete_row(file_path: str, condition: Dict[str, Any]) -> None:
    """Delete rows based on condition"""
    df = load_data(file_path)

    if df.empty:
        return

    mask = pd.Series([True] * len(df))

    for col, val in condition.items():
        mask &= df[col] == val

    df = df[~mask]
    save_data(df, file_path)


def get_filtered(file_path: str, condition: Dict[str, Any]) -> pd.DataFrame:
    """Get filtered rows"""
    df = load_data(file_path)

    if df.empty:
        return df

    mask = pd.Series([True] * len(df))

    for col, val in condition.items():
        mask &= df[col] == val

    return df[mask]


def upsert_row(file_path: str, condition: Dict[str, Any], row: Dict[str, Any]) -> None:
    """
    Update if exists, else insert
    """
    df = load_data(file_path)

    if df.empty:
        insert_row(file_path, row)
        return

    mask = pd.Series([True] * len(df))

    for col, val in condition.items():
        mask &= df[col] == val

    if mask.any():
        for col, val in row.items():
            df.loc[mask, col] = val
    else:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    save_data(df, file_path)
