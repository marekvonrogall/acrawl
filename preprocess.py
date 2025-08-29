from constants import BASE_DIR, FETCHING_DATE, Color
import re
import os

def pre_process_file(infile):
    in_filepath = os.path.join(BASE_DIR, FETCHING_DATE, infile["source"], f"{infile["name"]}.{infile["format"]}")
    out_filepath = os.path.join(BASE_DIR, FETCHING_DATE, infile["source"], f"{infile["name"]}_processed.{infile["format"]}")

    print(f"{Color.OKCYAN}[INFO]{Color.ENDC} Pre-processing: {infile["name"]}.{infile["format"]}... ", end='')

    if infile["name"] == "cme_catalog_all":
        outfile = preprocess_cme_catalog_all(infile, in_filepath, out_filepath)
    elif infile["name"] == "daily_estimated_sunspot_number":
        outfile = preprocess_daily_estimated_sunspot_number(infile, in_filepath, out_filepath)
    elif infile["name"] == "month_kp_ap_index_detailed" or infile["name"] == "century_kp_ap_index_detailed":
        outfile = preprocess_kp_ap_index(infile, in_filepath, out_filepath)
    elif infile["name"] == "daily_geomagnetic_data":
        outfile = preprocess_daily_geomagnetic_data(infile, in_filepath, out_filepath)
    else: # file does not need pre-processing
        print(f"{Color.WARNING}(SKIPPED){Color.ENDC}")
        return infile
    print(f"{Color.OKGREEN}(OK){Color.ENDC}")
    return outfile

def preprocess_daily_geomagnetic_data(infile, in_filepath, out_filepath):
    with open(in_filepath) as f:
        lines = [line.strip() for line in f if line.strip()]

    cleaned_lines = []
    for line in lines:
        # Replace sequences like -1-1-1 with space-separated values
        line = re.sub(r'(-?\d)(?=-\d)', r'\1 ', line)
        # Collapse multiple spaces into single space
        line = re.sub(r'\s+', ' ', line)
        # Replace spaces with "|"
        line = line.replace(" ", "|")

        cleaned_lines.append(line)

    with open(out_filepath, "w") as f:
        f.write("\n".join(cleaned_lines))

    outfile = infile.copy()
    outfile["name"] += "_processed"
    return outfile

def preprocess_kp_ap_index(infile, in_filepath, out_filepath):
    with open(in_filepath) as f:
        lines = [line.strip() for line in f if not line.startswith("#") and line.strip()]

    hours = [0, 3, 6, 9, 12, 15, 18, 21]
    new_lines = []
    for line in lines:
        parts = line.split()
        year, month, day = parts[0], parts[1], parts[2]
        days_since_1932, days_mid, Bsr, dB = parts[3], parts[4], parts[5], parts[6]
        Kp = parts[7:15]   # Kp1–Kp8
        ap = parts[15:23]  # ap1–ap8
        Ap, SN, F107_obs, F107_adj, definitive = parts[23], parts[24], parts[25], parts[26], parts[27]

        # expand into 8 rows
        for i in range(8):
            new_line = [
                year, month, day, str(hours[i]),
                days_since_1932, days_mid, Bsr, dB,
                Kp[i], ap[i],
                Ap, SN, F107_obs, F107_adj, definitive
            ]
            new_lines.append(" ".join(new_line))

    with open(out_filepath, "w") as f:
        f.write("\n".join(new_lines))

    outfile = infile.copy()
    outfile["name"] += "_processed"
    return outfile

def preprocess_daily_estimated_sunspot_number(infile, in_filepath, out_filepath):
    with open(in_filepath) as f:
        lines = [line.rstrip(",\n") for line in f]

    with open(out_filepath, "w") as f:
        f.write("\n".join(lines))

    outfile = infile.copy()
    outfile["name"] += "_processed"
    return outfile

def preprocess_cme_catalog_all(infile, in_filepath, out_filepath):
    cleaned = []
    # Der Chatsklave hat gezaubert
    with open(in_filepath, "r") as f:
        for line in f:
            line = line.rstrip("\n")
            # skip headers / separators
            if line.startswith("=") or line.startswith("Date") or line.strip() == "":
                continue
            # fix multiple spaces -> single space
            parts = line.split()
            if len(parts) < 12:
                # skip non-data lines (like "Revised on  2010/11/22")
                continue
            # join first 12 fields, keep remainder as remarks
            fixed = parts[:12] + [" ".join(parts[12:])]
            cleaned.append(" | ".join(fixed))  # use pipe as delimiter

    with open(out_filepath, "w") as f:
        for row in cleaned:
            f.write(row + "\n")
    outfile = infile.copy()
    outfile["name"] += "_processed"
    return outfile
