from urllib.request import urlretrieve
from constants import FETCHING_DATE, Color, BASE_DIR, Frequency, DEFAULT_RESOLUTION, MAX_WORKERS
from data import DATA_SUNSPOTS, DATA_FLARES, DATA_KP_INDEX, DATA_CME
from directory import create_data_directories, delete_directory
from crawl import get_latest_sun_image_url, get_latest48h_video_url, get_daily_cme_movies
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

def fetch_data(delete_previous_data=True):
    if delete_previous_data: delete_directory(FETCHING_DATE)
    download_data(DATA_SUNSPOTS, DATA_FLARES, DATA_KP_INDEX, DATA_CME)

def fetch_media():
    images = []
    videos = []
    for frequency in Frequency:
        images.append(get_latest_sun_image_url(DEFAULT_RESOLUTION.value, frequency.value, False))
        images.append(get_latest_sun_image_url(DEFAULT_RESOLUTION.value, frequency.value, True))
        videos.append(get_latest48h_video_url(frequency=frequency.value))
    download_data(images)
    download_data(videos)

def fetch_cme_movies():
    cme_date, cme_movie_frames = get_daily_cme_movies()
    download_data(cme_movie_frames)
    return cme_date

def download_data(*args, downloaded_data=None, date=FETCHING_DATE):
    tasks = []
    if downloaded_data is None: downloaded_data = set()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for arg in args:
            if isinstance(arg, dict):
                items = [arg]
            elif isinstance(arg, (list, tuple)):
                items = arg
            else:
                raise TypeError

            for data_item in items:
                if not isinstance(data_item["url"], dict) and data_item["url"] in downloaded_data:
                    print(f"{Color.WARNING}[WARNING]{Color.ENDC} Already exists: {data_item["source"]}: \"{data_item["name"]}.{data_item["format"]}\" ({data_item["url"]}) {Color.WARNING}(SKIPPED){Color.ENDC}")
                    continue

                create_data_directories(data_item, date=date)

                if isinstance(data_item["url"], str):
                    if data_item.get("folder"): download_path = os.path.join(BASE_DIR, date, data_item["source"], data_item["folder"], f"{data_item["name"]}.{data_item["format"]}")
                    else: download_path = os.path.join(BASE_DIR, date, data_item["source"], f"{data_item["name"]}.{data_item["format"]}")

                    print(f"{Color.OKCYAN}[INFO]{Color.ENDC} Scheduling: {data_item["source"]}: \"{data_item["name"]}.{data_item["format"]}\" ({data_item["url"]}) - {download_path}")

                    # submit the download task
                    tasks.append(executor.submit(_download_file, data_item["url"], download_path, downloaded_data))

                elif isinstance(data_item["url"], dict) and data_item["url"].get("jfiles1") and data_item["url"].get(
                        "jfiles2"):
                    print(f"{Color.OKCYAN}[INFO]{Color.ENDC}: Task: CME Movie Frames ({data_item["url"]["page"]})")
                    date = data_item["date"]
                    download_data(data_item["url"]["jfiles1"], downloaded_data=downloaded_data, date=date)
                    download_data(data_item["url"]["jfiles2"], downloaded_data=downloaded_data, date=date)

        # wait for all downloads
        for future in as_completed(tasks):
            future.result()

def _download_file(url, path, downloaded_data):
    try:
        urlretrieve(url, path)
        downloaded_data.add(url)
        print(f"{Color.OKBLUE}[DONE]{Color.ENDC} Downloaded: {url} - {path}")
    except Exception as e:
        print(f"{Color.FAIL}[ERROR]{Color.ENDC}", e)
