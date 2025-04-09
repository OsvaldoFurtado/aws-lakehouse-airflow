from datetime import datetime
from include.etls.api_etl import extract_jobs_facet_counts, save_data_to_csv, transformations
from include.utils.constants import API_FIELDS, JOBS_API_URL, JOBS_API_HEADER, BASE_LOCAL_PATH
import os

def extract_and_save_local():

    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    day = datetime.now().strftime("%d")
    local_path = f'{BASE_LOCAL_PATH}/year={year}/month={month}/day={day}'
    os.makedirs(local_path, exist_ok=True) 

    # extraction
    dataframes = extract_jobs_facet_counts(JOBS_API_URL, JOBS_API_HEADER, API_FIELDS)
    # transformations
    dataframes["eintrittsdatum"], dataframes["befristung"], dataframes["arbeitszeit"] = transformations(dataframes["eintrittsdatum"], dataframes["befristung"], dataframes["arbeitszeit"])
    # loading to csv
    save_data_to_csv(dataframes, local_path, API_FIELDS)


if __name__ == "__main__":
    extract_and_save_local()