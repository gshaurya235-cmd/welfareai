"""
WelfareAI - Data Persistence & Historical Store
Manages personnel welfare check-ins with clear labeling of demo/sample records.

CRITICAL NOTICE: Any pre-populated sample records are strictly synthetic DEMO DATA
created solely for prototype evaluation and testing. They do NOT represent real personnel records.
"""

import os
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(DATA_DIR, "checkins.csv")

DEMO_PERSONNEL_ID = "DEMO-CRPF-4829"
DEMO_PERSONNEL_NAME = "Demo Personnel (Sample Profile)"
DEMO_UNIT = "104 Rapid Action BN (Demo)"
DEMO_RANK = "Constable"

def get_demo_historical_records() -> List[Dict[str, Any]]:
    """
    Generates synthetic 14-day history strictly labeled as Sample / Demo Data.
    Designed for prototype evaluation at hackathons like SIH.
    """
    records = []
    # Sample records cover the past 14 days up to yesterday
    now = datetime.now()
    
    # 14-day simulated progression showing recovery after duty fatigue
    sample_timeline = [
        # (days_ago, sleep, duty, workload, night, rest, stress, risk, index)
        (14, 7.5, 8.0, 4, 2, 8, 3, "Low", 88),
        (13, 7.0, 8.5, 5, 2, 8, 4, "Low", 84),
        (12, 6.5, 9.0, 5, 3, 7, 4, "Low", 80),
        (11, 5.5, 11.0, 7, 4, 6, 6, "Moderate", 64),
        (10, 5.0, 12.5, 8, 5, 5, 7, "Moderate", 55),
        (9, 4.2, 14.0, 9, 6, 4, 8, "High", 36),
        (8, 4.0, 13.5, 9, 7, 4, 9, "High", 30),
        (7, 6.0, 8.0, 6, 7, 5, 6, "Moderate", 62), # Decompression rest
        (6, 7.5, 0.0, 2, 7, 6, 3, "Low", 86),      # Rest day
        (5, 7.0, 8.0, 5, 7, 6, 4, "Low", 82),
        (4, 5.5, 11.5, 7, 8, 5, 6, "Moderate", 60),
        (3, 4.8, 13.0, 8, 9, 5, 8, "High", 42),
        (2, 6.5, 9.0, 5, 9, 6, 5, "Moderate", 68),
        (1, 7.0, 8.0, 4, 9, 7, 4, "Low", 81),
    ]

    for days_ago, sleep, duty, wload, night, rest, stress, risk, idx in sample_timeline:
        record_dt = now - timedelta(days=days_ago, hours=1, minutes=30)
        entry_date = record_dt.strftime("%Y-%m-%d")
        timestamp = record_dt.strftime("%Y-%m-%d %H:%M:%S")
        records.append({
            "timestamp": timestamp,
            "date": entry_date,
            "data_source": "Sample / Demo Data",
            "is_demo": True,
            "personnel_id": DEMO_PERSONNEL_ID,
            "personnel_name": DEMO_PERSONNEL_NAME,
            "rank": DEMO_RANK,
            "unit": DEMO_UNIT,
            "sleep_hours": float(sleep),
            "duty_hours": float(duty),
            "workload": int(wload),
            "night_duty_count": int(night),
            "rest_days": int(rest),
            "stress_level": int(stress),
            "risk_level": risk,
            "welfare_index": int(idx),
            "notes": "Simulated evaluation record (Demo Data)"
        })

    return records

def initialize_store_if_needed():
    """Initializes CSV store with clearly marked Demo Data if file does not exist."""
    if not os.path.exists(CSV_FILE_PATH):
        records = get_demo_historical_records()
        df = pd.DataFrame(records)
        df.to_csv(CSV_FILE_PATH, index=False)

def load_checkin_history(personnel_id: str = None) -> pd.DataFrame:
    """Loads all check-in history, optionally filtered by personnel ID."""
    initialize_store_if_needed()
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values(by="timestamp", ascending=False)
        return df
    except Exception as e:
        # Fallback to in-memory demo records
        records = get_demo_historical_records()
        df = pd.DataFrame(records)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df

def save_new_checkin(
    personnel_id: str,
    personnel_name: str,
    rank: str,
    unit: str,
    sleep_hours: float,
    duty_hours: float,
    workload: int,
    night_duty_count: int,
    rest_days: int,
    stress_level: int,
    risk_level: str,
    welfare_index: int,
    notes: str = ""
) -> Dict[str, Any]:
    """Appends a new user check-in record marked as Live Session Entry."""
    initialize_store_if_needed()
    
    now = datetime.now()
    new_record = {
        "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "data_source": "Live User Session",
        "is_demo": False,
        "personnel_id": personnel_id if personnel_id else "USER-001",
        "personnel_name": personnel_name if personnel_name else "Personnel",
        "rank": rank if rank else "Unspecified",
        "unit": unit if unit else "General Duty",
        "sleep_hours": float(sleep_hours),
        "duty_hours": float(duty_hours),
        "workload": int(workload),
        "night_duty_count": int(night_duty_count),
        "rest_days": int(rest_days),
        "stress_level": int(stress_level),
        "risk_level": risk_level,
        "welfare_index": int(welfare_index),
        "notes": notes if notes else "Live check-in entry"
    }

    try:
        if os.path.exists(CSV_FILE_PATH):
            df = pd.read_csv(CSV_FILE_PATH)
            df = pd.concat([pd.DataFrame([new_record]), df], ignore_index=True)
        else:
            df = pd.DataFrame([new_record])
        df.to_csv(CSV_FILE_PATH, index=False)
    except Exception as e:
        print(f"Error saving to CSV: {e}")

    return new_record

def reset_to_sample_data():
    """Resets the CSV store to fresh sample demo data."""
    records = get_demo_historical_records()
    df = pd.DataFrame(records)
    df.to_csv(CSV_FILE_PATH, index=False)
