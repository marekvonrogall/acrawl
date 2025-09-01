from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import DateTime, inspect
from constants import Color
import pandas as pd
import os

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
ENGINE = create_engine(CONNECTION_STRING)

def store_data(normalized_data):
    for item in normalized_data:
        table_name = item["name"].replace("-", "_")
        df = item["data_frame"]

        if df.empty:
            print(f"{Color.FAIL}[ERROR]{Color.ENDC} Dataframe empty: {item['name']}")
            continue

        df.replace([" ------- ", " ------ ", " ----- ", " ---- ", "unk", "Unk", "UNK"], None, inplace=True)

        if item["name"] == "cme_catalog_all_processed":
            for col in df.select_dtypes(include="object").columns:
                df[col] = df[col].str.replace('*', '', regex=False)
                if col != "datetime" and col != "remarks" and col != "central_PA":
                    df[col] = df[col].astype(float)

        if list(df.iloc[0, 1:]) == list(df.columns[1:]):
            df = df.iloc[1:].copy() # Drop the first row
            df.reset_index(drop=True, inplace=True)
            for col in df.columns:
                if col != "datetime":
                    df[col] = pd.to_numeric(df[col], errors='coerce')

        """AVOID SOMETHING LIKE THIS:
        MariaDB [parsed_data]> SELECT * FROM week_kp_index LIMIT 3;
        +---------------------+------+-----------+---------------+
        | datetime            | Kp   | a_running | station_count |
        +---------------------+------+-----------+---------------+
        | NULL                | Kp   | a_running | station_count |
        | 2025-08-19 00:00:00 | 3.00 | 15        | 8             |
        | 2025-08-19 03:00:00 | 2.00 | 7         | 8             |
        +---------------------+------+-----------+---------------+
        3 rows in set (0.000 sec)   
        """

        inspector = inspect(ENGINE)
        if table_name in inspector.get_table_names():
            existing = pd.read_sql(f"SELECT datetime FROM {table_name}", ENGINE)
            df["datetime"] = df["datetime"].dt.tz_localize(None)
            df_new = df[~df["datetime"].isin(existing["datetime"])]
        else: df_new = df;
        df_new.to_sql(name=table_name, con=ENGINE, if_exists='append', index=False, chunksize=5000, dtype={"datetime": DateTime()})
    return
