from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlretrieve
from sqlalchemy import create_engine, DateTime
from dotenv import load_dotenv
import pandas as pd
import os
import re
import requests
import json
import shutil

load_dotenv()

CONNECTION_STRING = os.getenv("CONNECTION_STRING")
ENGINE = create_engine(CONNECTION_STRING)

SESSION = requests.Session()
FETCHING_DATE = datetime.today().strftime("%Y-%m-%d")
BASE_DIR = "data"

def fetch_url(url):
    response = SESSION.get(url, timeout=5)
    response.raise_for_status()
    return response

# SUNSPOT NUMBERS
DATA_SUNSPOTS = [
    {
        "source": "swpc", "format": "json", "name": "observed_solar_cycle",
        "url": "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json",
        "parsing_options": {
            "col_names": [
                "time_tag", "ssn", "smoothed_ssn", "observed_swpc_ssn",
                "smoothed_swpc_ssn", "f10.7", "smoothed_f10.7"
            ],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "json", "name": "predicted_solar_cycle",
        "url": "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json",
        "parsing_options": {
            "col_names": [
                "time_tag", "predicted_ssn", "high25_ssn", "high_ssn",
                "high75_ssn", "low25_ssn", "low_ssn", "low75_ssn",
                "predicted_f10.7", "high25_f10.7", "high_f10.7",
                "high75_f10.7", "low25_f10.7", "low_f10.7", "low75_f10.7"
            ],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "json", "name": "daily_solar_cycle",
        "url": "https://services.swpc.noaa.gov/json/solar-cycle/swpc_observed_ssn.json",
        "parsing_options": {
            "col_names": ["Obsdate", "swpc_ssn"],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "sidc", "format": "csv", "name": "daily_sunspot_number",
        "url": "https://www.sidc.be/SILSO/INFO/sndtotcsv.php",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "fractional_year",
                "daily_total_ssn", "daily_std_dev", "observations", "definitive"
            ],
            "delimiter": ";", "comment": None
        }
    }, {
        "source": "sidc", "folder": "plots", "format": "png", "name": "daily_sunspot_plot",
        "url": "https://www.sidc.be/SILSO/IMAGES/GRAPHICS/wolfjmms.png",
        "parsing_options": None
    }, {
        "source": "sidc", "format": "csv", "name": "monthly_sunspot_number",
        "url":"https://www.sidc.be/SILSO/INFO/snmtotcsv.php",
        "parsing_options": {
            "col_names": [
                "year", "month", "fractional_year",
                "monthly_mean_total_ssn", "monthly_std_dev",
                "observations", "definitive"
            ],
            "delimiter": ";", "comment": None
        }
    }, {
        "source": "sidc", "format": "csv", "name": "daily_estimated_sunspot_number",
        "url":"https://www.sidc.be/SILSO/DATA/EISN/EISN_current.csv",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "decimal_date", "estimated_ssn",
                "estimated_std_dev", "stations_calculated", "stations_available"
            ],
            "delimiter": ",", "comment": None
        }
    }, {
        "source": "sidc", "folder": "plots", "format": "png", "name": "monthly_sunspot_plot",
        "url": "https://www.sidc.be/SILSO/DATA/EISN/EISNcurrent.png",
        "parsing_options": None
    }
]

# FLARES
DATA_FLARES = [
    {
        "source": "swpc", "format": "json", "name": "xray_flares_latest_primary",
        "url": "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json",
        "parsing_options": {
            "col_names": [
                "time_tag", "satellite", "current_class", "current_ratio", "current_int_xrlong",
                "begin_time", "begin_class", "max_time", "max_class", "max_xrlong", "end_time",
                "max_ratio_time", "max_ratio", "end_class"
            ],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "json", "name": "xray_flares_latest_secondary",
        "url": "https://services.swpc.noaa.gov/json/goes/secondary/xray-flares-latest.json",
        "parsing_options": {
            "col_names": [
                "time_tag", "satellite", "current_class", "current_ratio", "current_int_xrlong",
                "begin_time", "begin_class", "max_time", "max_class", "max_xrlong", "end_time",
                "max_ratio_time", "max_ratio", "end_class"
            ],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "json", "name": "xray_flares_week_primary",
        "url": "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json",
        "parsing_options": {
            "col_names": [
                "time_tag", "begin_time", "begin_class", "max_time", "max_class",
                "max_xrlong", "max_ratio", "max_ratio_time", "current_int_xrlong",
                "end_time", "end_class", "satellite"
            ],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "json", "name": "xray_flares_week_secondary",
        "url": "https://services.swpc.noaa.gov/json/goes/secondary/xray-flares-7-day.json",
        "parsing_options": {
            "col_names": [
                "time_tag", "begin_time", "begin_class", "max_time", "max_class",
                "max_xrlong", "max_ratio", "max_ratio_time", "current_int_xrlong",
                "end_time", "end_class", "satellite"
            ],
            "delimiter": None, "comment": None
        }
    }
]

# KP-INDEX
DATA_KP_INDEX = [
    {
        "source": "swpc", "format": "json", "name": "week_kp-index",
        "url": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json",
        "parsing_options": {
            "col_names": ["time_tag", "Kp", "a_running", "station_count"],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "txt", "name": "month_kp-index",
        "url": "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day",
                "Af", "Kf1", "Kf2", "Kf3", "Kf4", "Kf5", "Kf6", "Kf7", "Kf8",
                "Ac", "Kc1", "Kc2", "Kc3", "Kc4", "Kc5", "Kc6", "Kc7", "Kc8",
                "Ap", "Kp1", "Kp2", "Kp3", "Kp4", "Kp5", "Kp6", "Kp7", "Kp8"
            ],
            "delimiter": "whitespace", "comment": "#", "skip_rows": 2
        }
    }, {
        "source": "gfz", "format": "txt", "name": "month_kp-ap-index",
        "url": "https://kp.gfz.de/app/files/Kp_ap_nowcast.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "start_hour", "mid_hour",
                "days_since_1932", "days_mid", "Kp", "ap", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "month_kp-ap-index-detailed",
        "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_nowcast.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "days_since_1932", "days_mid", "Bsr",
                "dB", "Kp1", "Kp2", "Kp3", "Kp4", "Kp5", "Kp6", "Kp7", "Kp8",
                "ap1", "ap2", "ap3", "ap4", "ap5", "ap6", "ap7", "ap8",
                "Ap", "SN", "F107_obs", "F107_adj", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "century_kp-ap-index",
        "url": "https://kp.gfz.de/app/files/Kp_ap_since_1932.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "start_hour", "mid_hour",
                "days_since_1932", "days_mid", "Kp", "ap", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "century_kp-ap-index-detailed",
        "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "days_since_1932", "days_mid", "Bsr",
                "dB", "Kp1", "Kp2", "Kp3", "Kp4", "Kp5", "Kp6", "Kp7", "Kp8",
                "ap1", "ap2", "ap3", "ap4", "ap5", "ap6", "ap7", "ap8",
                "Ap", "SN", "F107_obs", "F107_adj", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }
]

# DAILY SUN IMAGES / 48h VIDEOS
DICT_FREQUENCIES = {
    "AIA 193 Å": "0193",
    "AIA 304 Å": "0304",
    "AIA 171 Å": "0171",
    "AIA 211 Å": "0211",
    "AIA 131 Å": "0131",
    "AIA 335 Å": "0335",
    "AIA 094 Å": "0094",
    "AIA 1600 Å": "1600",
    "AIA 1700 Å": "1700"
}
DEFAULT_FREQUENCY = DICT_FREQUENCIES.get("AIA 171 Å")

DICT_RESOLUTIONS = {
    "512x512px": "512",
    "1024x1024px": "1024",
    "2048x2048px": "2048",
    "4096x4096px": "4096",
}
DEFAULT_RESOLUTION = DICT_RESOLUTIONS.get("1024x1024px")

DICT_CORNERS = {
    "Full": "",
    "CloseUp": "NC_",
    "North West": "NW_",
    "North East": "NE_",
    "South West": "SW_",
    "South East": "SE_",
}
DEFAULT_CORNER = DICT_CORNERS.get("Full")

def get_latest_sun_image_url (resolution=DEFAULT_RESOLUTION, frequency=DEFAULT_FREQUENCY, pfss=False):
    if frequency in DICT_FREQUENCIES.values() and resolution in DICT_RESOLUTIONS.values():
        str_pfss = "pfss" if pfss else ""
        latest_url = f"https://sdo.gsfc.nasa.gov/assets/img/latest/latest_{resolution}_{frequency}{str_pfss}.jpg"
        filename = f"latest_{FETCHING_DATE}_{resolution}_{frequency}{str_pfss}"

        return {
            "source": "nasa",
            "folder": "imgLatest",
            "format": "jpg",
            "name": filename,
            "url": latest_url
        }
    else: return None

def get_latest48h_video_url (resolution=DEFAULT_RESOLUTION, frequency=DEFAULT_FREQUENCY, corner=DEFAULT_CORNER, synoptic=False):
    if corner != DEFAULT_CORNER:
        resolution = DICT_RESOLUTIONS.get("1024x1024px")
        synoptic = False
    if frequency in DICT_FREQUENCIES.values() and corner in DICT_CORNERS.values() and (resolution == DICT_RESOLUTIONS.get("512x512px") or resolution == DICT_RESOLUTIONS.get("1024x1024px")):
        str_synoptic = "_synoptic" if synoptic else ""
        latest48_url = f"https://sdo.gsfc.nasa.gov/assets/img/latest/mpeg/latest_{resolution}_{corner}{frequency}{str_synoptic}.mp4"
        filename = f"latest48_{FETCHING_DATE}_{resolution}_{corner}{frequency}{str_synoptic}"

        return {
            "source": "nasa",
            "folder": "48hLatest",
            "format": "mp4",
            "name": filename,
            "url": latest48_url
        }
    else: return None

# CME
DATA_CME = [
    {
        "source": "nasa", "format": "html", "name": "cme_catalog_html",
        "url": "https://cdaw.gsfc.nasa.gov/CME_list/",
        "parsing_options": None
    }, {
        "source": "nasa", "format": "html", "name": "cme_catalog_text",
        "url": "https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL_ver2/text_ver/",
        "parsing_options": None
    }, {
        "source": "nasa", "format": "txt", "name": "cme_catalog_all",
        "url": "https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL_ver2/text_ver/univ_all.txt",
        "parsing_options": {
            "col_names": [
                "date", "time", "central_PA", "width", "linear_speed",
                "speed_2nd_initial", "speed_2nd_final", "speed_2nd_20R",
                "acceleration", "mass", "kinetic_energy", "MPA", "remarks"
            ],
            "delimiter": "|", "comment": "=", "skip_rows": 1,
        }
    }
]

def get_latest_available_cme_movie_url():
    base_cme_url = "https://cdaw.gsfc.nasa.gov/CME_list/daily_movies"
    year_cme_url = retrieve_latest_cme_href_link(base_cme_url)
    year_month_cme_url = retrieve_latest_cme_href_link(year_cme_url)
    year_month_day_cme_url = retrieve_latest_cme_href_link(year_month_cme_url)

    date = year_month_day_cme_url.rsplit("/", 3)
    date = f"{date[1]}-{date[2]}-{date[3]}"

    return {
        "source": "nasa",
        "format": "url",
        "name": "daily_cme_movie_base_url",
        "url": year_month_day_cme_url,
        "date": date
    }

def retrieve_latest_cme_href_link(url):
    try:
        response = fetch_url(url)
        soup = BeautifulSoup(response.text, "html.parser")
        hrefs = []
        for a in soup("a", href=True):
            if a["href"][:-1].isdigit():
                hrefs.append(a["href"][:-1])
        return f"{url}/{max(hrefs)}"
    except Exception as e: print("Error", e)

def get_daily_cme_movies():
    daily_cme_movie = get_latest_available_cme_movie_url()
    daily_cme_movie_url = daily_cme_movie["url"]
    daily_cme_movie_pages = []
    date = daily_cme_movie["date"]

    try:
        response = fetch_url(daily_cme_movie_url)
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup("a", href=True):
            url = f"{daily_cme_movie_url}/{a["href"]}"
            if url.endswith(".html"):
                response = fetch_url(url)
                redirect_soup = BeautifulSoup(response.text, "html.parser")
                meta = redirect_soup.find("meta", attrs={"http-equiv": "Refresh"})
                if meta and "content" in meta.attrs:
                    content = meta["content"]
                    redirect_url = content.split("URL=")[1].strip()
                    daily_cme_movie_pages.append(redirect_url)
    except requests.exceptions.RequestException as e:
        print(e)

    cme_daily_movie_pages = {
        "source": daily_cme_movie["source"],
        "format": "url",
        "name": "daily_cme_movie_urls",
        "url": daily_cme_movie_pages
    }
    return crawl_daily_cme_movie_frames(cme_daily_movie_pages, date)

def crawl_daily_cme_movie_frames(cme_movie_pages, date):
    cme_movie_frames = []

    for page in cme_movie_pages["url"]:
        cme_movie_dict = {
            "source": cme_movie_pages["source"],
            "format": "url",
            "name": "daily_cme_movie_frames_url",
            "url": {
                "page": page,
                "jfiles1": [],
                "jfiles2": []
            },
            "date": date
        }

        try:
            response = fetch_url(page)
            soup = BeautifulSoup(response.text, "html.parser")

            for script in soup.find_all("script"):
                text = script.get_text()
                if not text:
                    continue

                pattern = r'(jfiles\d+)\.push\s*\(\s*"([^"]+)"\s*\)'
                matches = re.findall(pattern, text)
                jfile1_frame_count = 0
                jfile2_frame_count = 0

                folders = cme_movie_dict["url"]["page"].split("&")
                jfile1_folder = folders[1].rsplit("=")[1]
                if len(folders) == 2: jfile2_folder = "goesx"
                else: jfile2_folder = folders[2].rsplit("=")[1]

                matching_jfiles = {"url": page, jfile1_folder: [], jfile2_folder: []}

                for jfile_names, url in matches:
                    frame_format = url[-3:]
                    frame_name = url.rsplit("/",1)[1][:-4]

                    matching_jfiles["path"] = os.path.join(cme_movie_pages["source"], f"{date}_{jfile1_folder}")

                    jfile = {
                        "source": cme_movie_dict["source"],
                        "name": frame_name,
                        "format": frame_format,
                        "url": url
                    }

                    if jfile_names == "jfiles1":
                        jfile1_frame_count += 1
                        jfile["folder"] = f"{date}_{jfile1_folder}"
                        cme_movie_dict["url"]["jfiles1"].append(jfile)
                        matching_jfiles[jfile1_folder].append(f"{frame_name}.{frame_format}")
                    elif jfile_names == "jfiles2":
                        jfile2_frame_count += 1
                        jfile["folder"] = f"{date}_{jfile2_folder}"
                        cme_movie_dict["url"]["jfiles2"].append(jfile)
                        matching_jfiles[jfile2_folder].append(f"{frame_name}.{frame_format}")
                if matching_jfiles.get("path"):
                    write_matching_jfiles_to_file(matching_jfiles, date)

            cme_movie_frames.append(cme_movie_dict)

        except requests.exceptions.RequestException as e:
            print(e)

    return cme_movie_frames

def write_matching_jfiles_to_file(matching_jfiles, date):
    create_directory(matching_jfiles["path"], date)
    with open(os.path.join(BASE_DIR, date, f"{matching_jfiles["path"]}/matches.json"), "a") as f:
        json.dump(matching_jfiles, f)

# DATA MAPS
DATA_SUNSPOTS_MAP = {item["name"]: item for item in DATA_SUNSPOTS}
DATA_FLARES_MAP = {item["name"]: item for item in DATA_FLARES}
DATA_KP_INDEX_MAP = {item["name"]: item for item in DATA_KP_INDEX}
DATA_CME_MAP = {item["name"]: item for item in DATA_CME}

# DIRECTORIES
def delete_directory(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print("Successfully deleted directory", path)
        except Exception as e:
            print("Error deleting directory", e)

def create_directory(path, date=FETCHING_DATE):
    path = os.path.join(BASE_DIR, date, path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print("Successfully created directory", path)
        except Exception as e:
            print("Error creating directory", e)

def create_data_directories(*args, date):
    sources = set()
    for data_item in args:
        sources.add(data_item["source"])
        if data_item.get("folder"):
            sources.add(os.path.join(data_item["source"], data_item["folder"]))

    for source in sources:
        create_directory(source, date)

# RETRIEVE DATA
def download_data(*args, downloaded_data=None, date=FETCHING_DATE):
    for arg in args:
        if isinstance(arg, dict):
            items = [arg]
        elif isinstance(arg, (list, tuple)):
            items = arg
        else: raise TypeError

        if downloaded_data is None: downloaded_data = set()
        for data_item in items:
            if not isinstance(data_item["url"], dict) and data_item["url"] in downloaded_data:
                print(f"Skipping \"{data_item["name"]}.{data_item["format"]}\" from {data_item["source"]} ({data_item["url"]}) because it already exists.")
                continue

            create_data_directories(data_item, date=date)

            if isinstance(data_item["url"], str):
                if data_item.get("folder"): download_path = os.path.join(BASE_DIR, date, data_item["source"], data_item["folder"],f"{data_item["name"]}.{data_item["format"]}")
                else: download_path = os.path.join(BASE_DIR, date, data_item["source"], f"{data_item["name"]}.{data_item["format"]}")
                print(f"Downloading \"{data_item["name"]}.{data_item["format"]}\" from {data_item["source"]} ({data_item["url"]}) into {download_path}")
                try:
                    urlretrieve(data_item["url"], download_path)
                    downloaded_data.add(data_item["url"])
                except Exception as e:
                    print(f"Error downloading file: {e}); skipping.")

            elif isinstance(data_item["url"], dict) and data_item["url"].get("jfiles1") and data_item["url"].get("jfiles2"):
                print(f"Downloading CME movie frames from: {data_item['url']['page']}")
                date = data_item["date"]
                download_data(data_item["url"]["jfiles1"], downloaded_data=downloaded_data, date=date)
                download_data(data_item["url"]["jfiles2"], downloaded_data=downloaded_data, date=date)

def fetch_data(delete_previous_data=True, get_daily_cme_movie_frames=True):
    if delete_previous_data: delete_directory(BASE_DIR)
    download_data(DATA_SUNSPOTS, DATA_FLARES, DATA_KP_INDEX, DATA_CME)
    download_data(get_latest_sun_image_url(DICT_RESOLUTIONS.get("1024x1024px"), DICT_FREQUENCIES.get("AIA 211 Å"), True))
    download_data(get_latest48h_video_url(frequency=DICT_FREQUENCIES.get("AIA 094 Å")))
    download_data(get_latest48h_video_url(DICT_RESOLUTIONS.get("512x512px"), DICT_FREQUENCIES.get("AIA 304 Å"), DICT_CORNERS.get("CloseUp"), False))
    if get_daily_cme_movie_frames: download_data(get_daily_cme_movies())

# PARSING
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
    except Exception as e: print(f"Error parsing file: {e}")
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
                print(f"Successfully parsed {parsed_file["name"]}.{parsed_file["format"]}!")
                parsed_file_count += 1
                continue
        unparsed_files.append(unparsed_file)

    return parsed_files, unparsed_files

# PREPROCESSING
def pre_process_file(infile):
    in_filepath = os.path.join(BASE_DIR, FETCHING_DATE, infile["source"], f"{infile["name"]}.{infile["format"]}")
    out_filepath = os.path.join(BASE_DIR, FETCHING_DATE, infile["source"], f"{infile["name"]}_processed.{infile["format"]}")

    if infile["name"] == "cme_catalog_all":
        print(f"Pre-processing {infile["name"]}.{infile["format"]}...")
        outfile = preprocess_cme_catalog_all(infile, in_filepath, out_filepath)
    elif infile["name"] == "daily_estimated_sunspot_number":
        print(f"Pre-processing {infile["name"]}.{infile["format"]}...")
        outfile = preprocess_daily_estimated_sunspot_number(infile, in_filepath, out_filepath)
    else: return infile # file does not need pre-processing

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

# ANALYZING
def analyze_data():
    return None

# STORING
def store_data():
    for item in normalized_data:
        table_name = item["name"].replace("-", "_")
        df = item["data_frame"]

        if list(df.iloc[0, 1:]) == list(df.columns[1:]):
            df = df.iloc[1:]  # Drop the first row
            df.reset_index(drop=True, inplace=True)

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

        df.to_sql(name=table_name, con=ENGINE, if_exists='replace', index=False, chunksize=5000, dtype={"datetime": DateTime()})
    return

def normalize_dates():
    normalized = []

    for item in parsed_data:
        df = item["data_frame"].copy()
        temp_datetime = None

        # year, month, day
        if {"year", "month", "day"}.issubset(df.columns):
            print("year, month, day")
            temp_datetime = pd.to_datetime(df[["year", "month", "day"]], errors="coerce")

        # year, month (use first day of the month)
        elif {"year", "month"}.issubset(df.columns):
            print("year, month")
            temp_datetime = pd.to_datetime(df.assign(day=1)[["year", "month", "day"]], errors="coerce")

        # date (+ optional "time")
        elif "date" in df.columns:
            print("date")
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
            removal_columns = ["year", "month", "day", "time", "date", "Obsdate", "time_tag", "fractional_year", "days_since_1932", "decimal_date"]
            for col in removal_columns:
                if col in df.columns:
                    # print(f"Dropping \"{col}\"...")
                    df = df.drop(columns=[col])

        item["data_frame"] = df
        normalized.append(item)

    return normalized

if __name__ == '__main__':
    fetch_data(get_daily_cme_movie_frames=False)
    parsed_data, _ = parse_data()
    normalized_data = normalize_dates()
    store_data()
    #analyzed_data = analyze_data()
