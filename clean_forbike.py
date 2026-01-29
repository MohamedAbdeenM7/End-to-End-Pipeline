import pandas as pd
import numpy as np


def dash_ready_data():
    # 1️⃣ Load raw data
    df = pd.read_csv("fordgobike-tripdataFor201902.csv")

    # 2️⃣ Rename columns (standardize)
    df = df.rename(columns={
    "duration_sec": "duration_sec",
    "start_time": "start_time",
    "start_station_name": "start_station_name",
    "start_station_latitude": "start_station_latitude",
    "start_station_longitude": "start_station_longitude",
    "user_type": "user_type",
    "member_gender": "member_gender",
    "member_birth_year": "birth_year"
    })

    # 3️⃣ Drop rows with critical missing values
    df = df.dropna(subset=[
    "start_time",
    "duration_sec",
    "start_station_name",
    "start_station_latitude",
    "start_station_longitude"
    ])

    # 4️⃣ Convert start_time to datetime
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")

    # 5️⃣ Remove invalid durations
    df = df[df["duration_sec"] > 0]

    # 6️⃣ Fix gender column
    df["member_gender"] = df["member_gender"].fillna("Other")

    # 7️⃣ Calculate age
    CURRENT_YEAR = 2019
    df["birth_year"] = pd.to_numeric(df["birth_year"], errors="coerce")
    df["age"] = CURRENT_YEAR - df["birth_year"]

    # Remove unrealistic ages
    df = df[(df["age"] >= 18) & (df["age"] <= 80)]

    # 8️⃣ Create age groups
    df["age_group"] = pd.cut(
    df["age"],
    bins=[0, 29, 50, 200],
    labels=["Young", "Adult", "Senior"]
    )

    # 9️⃣ Day of week & month (USED IN DASH)
    df["day_of_week"] = df["start_time"].dt.day_name()
    df["month"] = df["start_time"].dt.strftime("%b")

    # 🔟 Trip ID
    df = df.reset_index(drop=True)
    df["trip_id"] = df.index + 1

    # 1️⃣1️⃣ Keep only required columns
    df = df[
    [
    "trip_id",
    "start_time",
    "duration_sec",
    "start_station_name",
    "start_station_latitude",
    "start_station_longitude",
    "user_type",
    "member_gender",
    "age",
    "age_group",
    "day_of_week",
    "month"
    ]
    ]

    # 1️⃣2️⃣ Save cleaned data
    df.to_csv("cleaned_fordgobike.csv", index=False)

    print("✅ Data cleaning finished. File saved as cleaned_fordgobike.csv")
