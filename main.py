from bs4 import BeautifulSoup
from datetime import datetime
from urllib.request import urlretrieve
import pandas as pd
import os
import re
import requests

SESSION = requests.Session()
BASE_DIR = "data"

def fetch_url(url):
    response = SESSION.get(url, timeout=5)
    response.raise_for_status()
    return response

# SUNSPOT NUMBERS
DATA_SUNSPOTS = [
    {
        "source": "swpc", "format": "json", "name": "observed_solar_cycle",
        "url": "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
    }, {
        "source": "swpc", "format": "json", "name": "predicted_solar_cycle",
        "url": "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json"
    }, {
        "source": "swpc", "format": "json", "name": "daily_solar_cycle",
        "url": "https://services.swpc.noaa.gov/json/solar-cycle/swpc_observed_ssn.json"
    }, {
        "source": "sidc", "format": "csv", "name": "daily_sunspot_number",
        "url": "https://www.sidc.be/SILSO/INFO/sndtotcsv.php" # schauen ob es evtl. php anstatt csv runterlädt
    }, {
        "source": "sidc", "format": "png", "name": "daily_sunspot_plot",
        "url": "https://www.sidc.be/SILSO/IMAGES/GRAPHICS/wolfjmms.png"
    }, {
        "source": "sidc", "format": "csv", "name": "monthly_sunspot_number",
        "url":"https://www.sidc.be/SILSO/DATA/EISN/EISN_current.csv"
    }, {
        "source": "sidc", "format": "png", "name": "monthly_sunspot_plot",
        "url": "https://www.sidc.be/SILSO/DATA/EISN/EISNcurrent.png"
    }
]

# KP-INDEX
DATA_KP_INDEX = [#YYY MM DD hh.h hh._m        days      days_m     Kp   ap D
    {
        "source": "swpc", "format": "json", "name": "week_kp-index",
        "url": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    }, {
        "source": "swpc", "format": "txt", "name": "month_kp-index",
        "url": "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt"
    }, {
        "source": "gfz", "format": "txt", "name": "month_kp-ap-index",
        "url": "https://kp.gfz.de/app/files/Kp_ap_nowcast.txt"
    }, {
        "source": "gfz", "format": "txt", "name": "month_kp-ap-index-detailed",
        "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_nowcast.txt"
    }, {
        "source": "gfz", "format": "txt", "name": "century_kp-ap-index",
        "url": "https://kp.gfz.de/app/files/Kp_ap_since_1932.txt",
        "parsing_options": {
            "col_names": ["year", "month", "day", "start_hour", "mid_hour", "days_since_1932",
            "days_mid", "Kp", "ap", "definitive"], "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "century_kp-ap-index-detailed",
        "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt"
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
        filename = f"latest_{datetime.today().strftime("%Y-%m-%d")}_{resolution}_{frequency}{str_pfss}"

        return {
            "source": "nasa",
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
        filename = f"latest48_{datetime.today().strftime("%Y-%m-%d")}_{resolution}_{corner}{frequency}{str_synoptic}"

        return {
            "source": "nasa",
            "format": "mp4",
            "name": filename,
            "url": latest48_url
        }
    else: return None

# CME
DATA_CME = [
    {
        "source": "nasa", "format": "html", "name": "cme_catalog_html",
        "url": "https://cdaw.gsfc.nasa.gov/CME_list/"
    }, {
        "source": "nasa", "format": "html", "name": "cme_catalog_text",
        "url": "https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL_ver2/text_ver/"
    }
]

def get_daily_cme_movie_url(date=datetime.today()):
    date = date.strftime("%Y/%m/%d")
    return {
        "source": "nasa",
        "format": "url",
        "name": "daily_cme_movie_base_url",
        "url": f"https://cdaw.gsfc.nasa.gov/CME_list/daily_movies/{date}"
    }

def crawl_daily_cme_movie_pages(date=datetime.today()):
    daily_cme_movie = get_daily_cme_movie_url(date)
    daily_cme_movie_url = daily_cme_movie["url"]
    daily_cme_movie_pages = []
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
    return crawl_daily_cme_movie_frames(cme_daily_movie_pages)

def crawl_daily_cme_movie_frames(cme_movie_pages):
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
            }
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

                for jfiles_name, url in matches:
                    if jfiles_name == "jfiles1":
                        cme_movie_dict["url"]["jfiles1"].append(url)
                    elif jfiles_name == "jfiles2":
                        cme_movie_dict["url"]["jfiles2"].append(url)

            cme_movie_frames.append(cme_movie_dict)

        except requests.exceptions.RequestException as e:
            print(e)

    return cme_movie_frames

# DATA MAPS
DATA_SUNSPOTS_MAP = {item["name"]: item for item in DATA_SUNSPOTS}
DATA_KP_INDEX_MAP = {item["name"]: item for item in DATA_KP_INDEX}
DATA_CME = {item["name"]: item for item in DATA_CME}

# DIRECTORIES
def create_data_directories(*args):
    os.makedirs(BASE_DIR, exist_ok=True)

    sources = set()
    for arg in args:
        for data_item in arg:
            sources.add(data_item["source"])

    for source in sources:
        source_dir = os.path.join(BASE_DIR, source)
        os.makedirs(source_dir, exist_ok=True)

def download_data(*args):
    for arg in args:
        if isinstance(arg, dict):
            items = [arg]
        elif isinstance(arg, (list, tuple)):
            items = arg
        else: raise TypeError
        create_data_directories(items)
        for data_item in items:
            print(f"Downloading \"{data_item["name"]}.{data_item["format"]}\" from {data_item["source"]}...")
            urlretrieve(data_item["url"], os.path.join(BASE_DIR, data_item["source"], f"{data_item["name"]}.{data_item["format"]}"))

# PARSING
def parse_file(file):
    if file.get("parsing_options"):
        delimiter = file["parsing_options"]["delimiter"]
        filename = os.path.join(BASE_DIR, file["source"], f"{file["name"]}.{file["format"]}")
        col_names = file["parsing_options"]["col_names"]
        comment = file["parsing_options"]["comment"]

        try:

            if delimiter == "whitespace":
                df = pd.read_csv(
                    filename,
                    sep = r"\s+",
                    names=col_names,
                    comment=comment,
                    engine="python"
                )
            else:
                df = pd.read_csv(
                    filename,
                    sep=delimiter,
                    names=col_names,
                    comment=comment
                )

            file["data_frame"] = df
            return file
        except: pass
    return "This file cannot be parsed."

if __name__ == '__main__':
    #download_data(DATA_SUNSPOTS, DATA_KP_INDEX, DATA_CME)
    #download_data(get_latest_sun_image_url(DICT_RESOLUTIONS.get("1024x1024px"), DICT_FREQUENCIES.get("AIA 211 Å"), True))
    #download_data(get_latest48h_video_url(frequency=DICT_FREQUENCIES.get("AIA 094 Å")))
    #download_data(get_latest48h_video_url(DICT_RESOLUTIONS.get("512x512px"), DICT_FREQUENCIES.get("AIA 304 Å"), DICT_CORNERS.get("CloseUp"), False))
    cme_movie_page_frames = crawl_daily_cme_movie_pages(datetime.strptime("Aug 17 2025", "%b %d %Y"))
    for cme_movie in cme_movie_page_frames:
        print({
            "source": cme_movie["source"],
            "format": cme_movie["format"],
            "name": cme_movie["name"],
            "url": {
                "page": cme_movie["url"]["page"],
                "jfiles1": f"{len(cme_movie["url"]["jfiles1"])} entries",
                "jfiles2": f"{len(cme_movie["url"]["jfiles2"])} entries"
            }
        })

    file_century_kp_ap_index = DATA_KP_INDEX_MAP.get("century_kp-ap-index")
    parsed_file_century_kp_ap_index = parse_file(file_century_kp_ap_index)
    print(parsed_file_century_kp_ap_index["data_frame"].head())
    print(parsed_file_century_kp_ap_index["data_frame"].columns)
