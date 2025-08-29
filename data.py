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
        "source": "swpc", "format": "json", "name": "week_kp_index",
        "url": "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json",
        "parsing_options": {
            "col_names": ["time_tag", "Kp", "a_running", "station_count"],
            "delimiter": None, "comment": None
        }
    }, {
        "source": "swpc", "format": "txt", "name": "daily_geomagnetic_data",
        "url": "https://services.swpc.noaa.gov/text/daily-geomagnetic-indices.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day",
                "Af", "Kf1", "Kf2", "Kf3", "Kf4", "Kf5", "Kf6", "Kf7", "Kf8",
                "Ac", "Kc1", "Kc2", "Kc3", "Kc4", "Kc5", "Kc6", "Kc7", "Kc8",
                "Ap", "Kp1", "Kp2", "Kp3", "Kp4", "Kp5", "Kp6", "Kp7", "Kp8"
            ],
            "delimiter": "|", "comment": "#", "skip_rows": 2
        }
    }, {
        "source": "gfz", "format": "txt", "name": "month_kp_ap_index",
        "url": "https://kp.gfz.de/app/files/Kp_ap_nowcast.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "hour", "mid_hour",
                "days_since_1932", "days_mid", "Kp", "ap", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "month_kp_ap_index_detailed",
        "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_nowcast.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "hour", "days_since_1932", "days_mid", "Bsr",
                "dB", "Kp", "ap", "Ap_day", "SN", "F107_obs", "F107_adj", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "century_kp_ap_index",
        "url": "https://kp.gfz.de/app/files/Kp_ap_since_1932.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "hour", "mid_hour",
                "days_since_1932", "days_mid", "Kp", "ap", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }, {
        "source": "gfz", "format": "txt", "name": "century_kp_ap_index_detailed",
        "url": "https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt",
        "parsing_options": {
            "col_names": [
                "year", "month", "day", "hour", "days_since_1932", "days_mid", "Bsr",
                "dB", "Kp", "ap", "Ap_day", "SN", "F107_obs", "F107_adj", "definitive"
            ],
            "delimiter": "whitespace", "comment": "#"
        }
    }
]

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
