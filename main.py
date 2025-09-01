from parse import parse_data
from normalize import normalize_dates
from database import store_data
from download import fetch_data, fetch_media, fetch_cme_movies
from analyze import analyze_data

if __name__ == '__main__':
    fetch_data()
    fetch_media()
    cme_date = fetch_cme_movies()
    parsed_data, _ = parse_data()
    normalized_data = normalize_dates(parsed_data)
    store_data(normalized_data)
    analyze_data(normalized_data)
