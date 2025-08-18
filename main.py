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

if __name__ == '__main__':
    pass
