from parse import parse_data
from normalize import normalize_dates
from database import store_data
from download import fetch_data
from analyze import analyze_data

if __name__ == '__main__':
    fetch_data(get_daily_cme_movie_frames=True)
    parsed_data, _ = parse_data()
    normalized_data = normalize_dates(parsed_data)
    store_data(normalized_data)
    analyze_data(normalized_data)
