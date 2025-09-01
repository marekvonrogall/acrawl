from constants import BASE_DIR, FETCHING_DATE, Color
from directory import create_directory
import matplotlib.pyplot as plt
import pandas as pd
import os

def analyze_data(normalized_data):
    data_map = {d['name']: d['data_frame'] for d in normalized_data}
    start_date = pd.Timestamp.today() - pd.Timedelta(days=8)
    outfile_dir = os.path.join("swpc", "plots")
    outfile_path = os.path.join(BASE_DIR, FETCHING_DATE, outfile_dir, "ssn_mxflares.png")
    create_directory(outfile_dir)

    df_solar = data_map['daily_solar_cycle']
    df_solar['datetime'] = pd.to_datetime(df_solar['datetime']).dt.tz_localize(None)
    df_solar = df_solar[df_solar['datetime'] >= start_date]
    df_solar.set_index('datetime', inplace=True)

    flare_frames = []
    for flare_name in ['xray_flares_week_primary', 'xray_flares_week_secondary']: flare_frames.append(data_map[flare_name])
    df_flares = pd.concat(flare_frames)
    df_flares['datetime'] = pd.to_datetime(df_flares['datetime']).dt.tz_localize(None)
    df_flares = df_flares[(df_flares['datetime'] >= start_date) & (df_flares['max_class'].str.startswith(('M', 'X')))]
    flare_dates = df_flares['datetime'].dt.normalize().drop_duplicates()
    flare_dates_filtered = flare_dates[flare_dates.isin(df_solar.index)]

    plt.figure(figsize=(12, 6))
    plt.plot(df_solar.index, df_solar['swpc_ssn'], label='SWPC SSN')
    plt.scatter(flare_dates_filtered, df_solar.loc[flare_dates_filtered, 'swpc_ssn'], color='purple', label='M/X Flares', zorder=5)
    plt.title('Sunspot Number with highlighted M/X-Flares (past week)')
    plt.xlabel('Date')
    plt.ylabel('Sunspot Number')
    plt.grid(True)
    plt.legend()
    plt.savefig(outfile_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"{Color.OKBLUE}[DONE]{Color.ENDC} Matplotlib: Saved SSN M/X-Flare plot - {outfile_path}")

