from constants import BASE_DIR, FETCHING_DATE, Color
from data import DATA_SUNSPOTS, DATA_FLARES, DATA_KP_INDEX, DATA_CME
from preprocess import pre_process_file
import os
import pandas as pd

def parse_file(file):
    if not file.get("parsing_options"):
        return None
    file = pre_process_file(file)

    try:
        filename = os.path.join(BASE_DIR, FETCHING_DATE, file["source"], f"{file["name"]}.{file["format"]}")
        col_names = file["parsing_options"]["col_names"]
        comment = file["parsing_options"]["comment"]

        if file["format"] == "json":
            df = pd.read_json(filename)
            df.columns = col_names
        elif file["format"] == "txt" or file["format"] == "csv":
            delimiter = file["parsing_options"]["delimiter"]
            skip_rows = file["parsing_options"].get("skip_rows", 0)
            if delimiter == "whitespace":
                df = pd.read_csv(
                    filename,
                    sep = r"\s+",
                    names=col_names,
                    comment=comment,
                    engine="python",
                    skiprows=skip_rows
                )
            else:
                df = pd.read_csv(
                    filename,
                    sep=delimiter,
                    names=col_names,
                    comment=comment,
                    skiprows = skip_rows
                )
        else: return None
        file["data_frame"] = df
        return file
    except Exception as e: print(f"{Color.FAIL}[ERROR]{Color.ENDC}", e)
    return None

def parse_data():
    parsed_files = []
    unparsed_files = []
    parsed_file_count = 0

    for unparsed_file in list(DATA_SUNSPOTS) + list(DATA_FLARES) + list(DATA_KP_INDEX) + list(DATA_CME):
        if unparsed_file["parsing_options"]:
            parsed_file = parse_file(unparsed_file)
            if parsed_file:
                parsed_files.append(parsed_file)
                print(f"{Color.OKBLUE}[DONE]{Color.ENDC} Parsed: {parsed_file["name"]}.{parsed_file["format"]}")
                parsed_file_count += 1
                continue
        unparsed_files.append(unparsed_file)

    return parsed_files, unparsed_files
