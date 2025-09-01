from bs4 import BeautifulSoup
import requests
from constants import Color, BASE_DIR, FETCHING_DATE, Frequency, DEFAULT_FREQUENCY, Resolution, DEFAULT_RESOLUTION, Corner, DEFAULT_CORNER
from directory import create_directory, delete_directory
import re
import os
import json

SESSION = requests.Session()

def fetch_url(url):
    response = SESSION.get(url, timeout=5)
    response.raise_for_status()
    return response

def retrieve_latest_cme_href_link(url):
    try:
        response = fetch_url(url)
        soup = BeautifulSoup(response.text, "html.parser")
        hrefs = []
        for a in soup("a", href=True):
            if a["href"][:-1].isdigit():
                hrefs.append(a["href"][:-1])
        return f"{url}/{max(hrefs)}"
    except Exception as e: print(f"{Color.FAIL}[Error]{Color.ENDC}", e)

def get_latest_sun_image_url (resolution=DEFAULT_RESOLUTION.value, frequency=DEFAULT_FREQUENCY.value, pfss=False):
    if frequency in [f.value for f in Frequency] and resolution in [r.value for r in Resolution]:
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

def get_latest48h_video_url (resolution=DEFAULT_RESOLUTION.value, frequency=DEFAULT_FREQUENCY.value, corner=DEFAULT_CORNER.value, synoptic=False):
    if corner != DEFAULT_CORNER.value:
        resolution = Resolution.R1024.value
        synoptic = False
    if frequency in [f.value for f in Frequency] and corner in [c.value for c in Corner] and (resolution == Resolution.R512.value or resolution == Resolution.R1024.value):
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

def get_latest_available_cme_movie_url():
    base_cme_url = "https://cdaw.gsfc.nasa.gov/CME_list/daily_movies"
    year_cme_url = retrieve_latest_cme_href_link(base_cme_url)
    year_month_cme_url = retrieve_latest_cme_href_link(year_cme_url)
    year_month_day_cme_url = retrieve_latest_cme_href_link(year_month_cme_url)

    date = year_month_day_cme_url.rsplit("/", 3)
    date = f"{date[1]}-{date[2]}-{date[3]}"

    delete_directory(date)

    return {
        "source": "nasa",
        "format": "url",
        "name": "daily_cme_movie_base_url",
        "url": year_month_day_cme_url,
        "date": date
    }

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
        print(f"{Color.FAIL}[ERROR]{Color.ENDC}", e)

    cme_daily_movie_pages = {
        "source": daily_cme_movie["source"],
        "format": "url",
        "name": "daily_cme_movie_urls",
        "url": daily_cme_movie_pages
    }
    return crawl_daily_cme_movie_frames(cme_daily_movie_pages, date)

def crawl_daily_cme_movie_frames(cme_movie_pages, date):
    cme_movie_frames = []
    matches_json = []

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

                    matching_jfiles["path"] = [os.path.join(cme_movie_pages["source"], f"{date}_{jfile1_folder}"),
                                               os.path.join(cme_movie_pages["source"], f"{date}_{jfile2_folder}")]

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
                    matches_json.append(matching_jfiles)

            cme_movie_frames.append(cme_movie_dict)

        except requests.exceptions.RequestException as e:
            print(f"{Color.FAIL}[ERROR]{Color.ENDC}", e)

    write_matching_jfiles_to_file(matches_json, date)
    return cme_movie_frames

def write_matching_jfiles_to_file(matches_json, date):
    for match in matches_json:
        for path in match["path"]:
            create_directory(path, date)

    with open(os.path.join(BASE_DIR, date, f"matches.json"), "a") as f:
        json.dump(matches_json, f)
