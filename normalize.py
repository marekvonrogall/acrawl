import warnings; warnings.filterwarnings("ignore")
import pandas as pd

def normalize_dates(parsed_data):
    normalized = []

    for item in parsed_data:
        df = item["data_frame"].copy()
        temp_datetime = None

        # year, month, day
        if {"year", "month", "day"}.issubset(df.columns):
            if "hour" in df.columns:
                temp_datetime = pd.to_datetime(df[["year", "month", "day", "hour"]], errors="coerce")
            else:
                temp_datetime = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")

        # year, month (use first day of the month)
        elif {"year", "month"}.issubset(df.columns):
            temp_datetime = pd.to_datetime(df.assign(day=1)[["year", "month", "day"]], errors="coerce")

        # date (+ optional "time")
        elif "date" in df.columns:
            if "time" in df.columns:
                temp_datetime = pd.to_datetime(
                    df["date"].astype(str) + " " + df["time"].astype(str),
                    errors="coerce"
                )
            else:
                temp_datetime = pd.to_datetime(df["date"], errors="coerce")

        # Obsdate
        elif "Obsdate" in df.columns:
            temp_datetime = pd.to_datetime(df["Obsdate"], errors="coerce")

        # time_tag
        elif "time_tag" in df.columns:
            temp_datetime = pd.to_datetime(df["time_tag"], errors="coerce")

        if temp_datetime is not None:
            df.insert(0, "datetime", temp_datetime)

            # drop old date / other bs columns
            removal_columns = ["year", "month", "day", "hour", "time", "date", "Obsdate", "time_tag", "fractional_year", "days_since_1932", "days_mid", "decimal_date"]
            for col in removal_columns:
                if col in df.columns:
                    df = df.drop(columns=[col])

        item["data_frame"] = df
        normalized.append(item)

    return normalized
