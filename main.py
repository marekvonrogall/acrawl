from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()

def fetch_url(url):
    response = session.get(url, timeout=5)
    response.raise_for_status()
    return response

# SUNSPOT NUMBERS
swpc_json_observed_solar_cycle = {
    "source": "swpc",
    "format": "json",
    "name": "observed_solar_cycle",
    "url": "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
}
swpc_json_predicted_solar_cycle = {
    "source": "swpc",
    "format": "json",
    "name": "predicted_solar_cycle",
    "url": "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json"
}
swpc_json_daily_solar_cycle = {
    "source": "swpc",
    "format": "json",
    "name": "daily_solar_cycle",
    "url": "https://services.swpc.noaa.gov/json/solar-cycle/swpc_observed_ssn.json"
}
sidc_csv_daily_sunspot_number = {
    "source": "sidc",
    "format": "csv",
    "name": "daily_sunspot_number",
    "url": "https://www.sidc.be/SILSO/INFO/sndtotcsv.php" #schauen ob es nicht evtl. das php runterlädt anstatt dem csv
}
sidc_png_daily_sunspot_plot = {
    "source": "sidc",
    "format": "png",
    "name": "daily_sunspot_plot",
    "url": "https://www.sidc.be/SILSO/IMAGES/GRAPHICS/wolfjmms.png"
}
sidc_csv_monthly_sunspot_number = {
    "source": "sidc",
    "format": "csv",
    "name": "monthly_sunspot_number",
    "url":"https://www.sidc.be/SILSO/DATA/EISN/EISN_current.csv"
}
sidc_png_monthly_sunspot_plot = {
    "source": "sidc",
    "format": "png",
    "name": "monthly_sunspot_plot",
    "url": "https://www.sidc.be/SILSO/DATA/EISN/EISNcurrent.png"
}

# KP-INDEX
swpc_json_week_kpindex = {
    "source": "swpc",
    "format": "json",
    "name": "week_kp-index",
    "url": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
}
swpc_txt_month_kpindex = {
    "source": "swpc",
    "format": "txt",
    "name": "month_kp-index",
    "url": "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt"
}
gfz_txt_month_kpindex = {
    "source": "gfz",
    "format": "txt",
    "name": "month_kp-ap-index",
    "url": "https://kp.gfz.de/app/files/Kp_ap_nowcast.txt"
}
gfz_txt_month_kpindex_detailed = {
    "source": "gfz",
    "format": "txt",
    "name": "month_kp-ap-index-detailed",
    "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_nowcast.txt"
}
gfz_txt_century_kpindex = {
    "source": "gfz",
    "format": "txt",
    "name": "century_kp-ap-index",
    "url": "https://kp.gfz.de/app/files/Kp_ap_since_1932.txt"
}
gfz_txt_century_kpindex_detailed = {
    "source": "gfz",
    "format": "txt",
    "name": "century_kp-ap-index-detailed",
    "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt"
}

# DAILY SUN IMAGES
dict_frequencies = {
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
default_frequency = dict_frequencies.get("AIA 171 Å")

dict_resolutions = {
    "512x512px": "512",
    "1024x1024px": "1024",
    "2048x2048px": "2048",
    "4096x4096px": "4096",
}
default_resolution = dict_resolutions.get("1024x1024px")

def GetLatestSunImageUrl (resolution=default_resolution, frequency=default_frequency, pfss=False):
    if frequency in dict_frequencies.values() and resolution in dict_resolutions.values():
        str_pfss = "pfss" if pfss else ""
        return f"https://sdo.gsfc.nasa.gov/assets/img/latest/latest_{resolution}_{frequency}{str_pfss}.jpg"
    else: return None

def GetLatest48hVideoUrl (frequency=default_frequency):
    if frequency in dict_frequencies.values():
        return f"https://sdo.gsfc.nasa.gov/data/latest48.php?q={frequency}"
    else: return None

# CME
nasa_html_cme_catalog = {
    "source": "nasa",
    "format": "html",
    "name": "cme_catalog_html",
    "url": "https://cdaw.gsfc.nasa.gov/CME_list/"
}

nasa_txt_cme_catalog = {
    "source": "nasa",
    "format": "txt",
    "name": "cme_catalog_text",
    "url": "https://cdaw.gsfc.nasa.gov/CME_list/UNIVERSAL_ver2/text_ver/"
}

def GetDailyCMEMovieUrl(date=datetime.today()):
    date = date.strftime("%Y/%m/%d")
    return f"https://cdaw.gsfc.nasa.gov/CME_list/daily_movies/{date}"

def CrawlDailyCMEMoviePage(date=datetime.today()):
    daily_cme_movie_url = GetDailyCMEMovieUrl(date)
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
    return daily_cme_movie_pages

def CrawlDailyCMEMovieFrames(cme_movie_pages):
    cme_movie_frames = []

    for page in cme_movie_pages:
        cme_movie_dict = {"page": page, "jfiles1": [], "jfiles2": []}
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
                        cme_movie_dict["jfiles1"].append(url)
                    elif jfiles_name == "jfiles2":
                        cme_movie_dict["jfiles2"].append(url)

                cme_movie_frames.append(cme_movie_dict)

        except requests.exceptions.RequestException as e:
            print(e)

    return cme_movie_frames

if __name__ == '__main__':
    print(GetLatestSunImageUrl(dict_resolutions.get("1024x1024px"), dict_frequencies.get("AIA 211 Å"), True))
    print(GetLatestSunImageUrl("512", "0193", True))
    print(GetLatestSunImageUrl(frequency=dict_frequencies.get("AIA 1700 Å")))
    print(GetLatest48hVideoUrl())
    cme_daily_movie_pages = CrawlDailyCMEMoviePage(datetime.strptime("Aug 17 2025", "%b %d %Y"))
    print(CrawlDailyCMEMovieFrames(cme_daily_movie_pages))
