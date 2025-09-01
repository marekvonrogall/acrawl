import os
from constants import Color, FETCHING_DATE, BASE_DIR
import shutil

def delete_directory(path):
    path = os.path.join(BASE_DIR, path)
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
            print(f"{Color.OKGREEN}[OK]{Color.ENDC} Directory: Deleted", path)
        except Exception as e:
            print(f"{Color.FAIL}[ERROR]{Color.ENDC}", e)

def create_directory(path, date=FETCHING_DATE):
    path = os.path.join(BASE_DIR, date, path)
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            print(f"{Color.OKGREEN}[OK]{Color.ENDC} Directory: Created", path)
        except Exception as e:
            print(f"{Color.FAIL}[ERROR]{Color.ENDC}", e)

def create_data_directories(*args, date):
    sources = set()
    for data_item in args:
        sources.add(data_item["source"])
        if data_item.get("folder"):
            sources.add(os.path.join(data_item["source"], data_item["folder"]))

    for source in sources:
        create_directory(source, date)
