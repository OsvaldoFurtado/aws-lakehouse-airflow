import requests
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)


def extract_jobs_facet_counts(api_url: str, api_key: str, facet_names: tuple) -> Dict:
    """
    Extracts data from Arbeitsagentur API and returns structured lists to create dataframes
    
    Returns:
        List containing the following lists:
        (befristung_list, externestellenboersen_list, behinderung_list,
         berufsfeld_list, arbeitsort_list, arbeitszeit_list, eintrittsdatum_list)
    """

    import pandas as pd

    #Verify if env vars are set
    if not api_url or not api_key:
        logging.error("Env variables JOBS_API_URL or JOBS_API_HEADER are not set")
        return ([], [], [], [], [], [], [])
    
    headers = {
        "X-API-Key": api_key
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error on sending API request: {str(e)}")
        return ([], [], [], [], [], [], [])
    
    if "facetten" not in data:
        logging.error("API response does not match the expected structure")
        return ([], [], [], [], [], [], [])
    
    facets = data["facetten"]
    
    #processed_lists = []
    dfs = {}
    

    try:
        for facet_name in facet_names:
            facet_data = facets.get(facet_name, {})
            counts = facet_data.get("counts", {})
            facet_list = [{facet_name: key, "count": value} for key, value in counts.items()]
            dfs[facet_name] = pd.DataFrame(facet_list, columns=[facet_name, "count"])
            #processed_lists.append(facet_list)
    except KeyError as e:
        logging.error(f"Invalid Data Structure: {str(e)}")
        return [[], [], [], [], [], [], []]

    return dfs



def transformations(df_eintritt, df_befristung, df_zeit):
    
    #ENTRITTSDATUM TRANSFORMATION
    # Remove first line
    df_eintritt = df_eintritt.iloc[1:].copy()
    
    # Split the date column into start end
    df_eintritt[['start', 'end']] = df_eintritt['eintrittsdatum'].str.split('-', expand=True)
    
    # Extracts the month and year from the start column
    df_eintritt[['start_year', 'start_month', 'start_day']] = df_eintritt['start'].str.split('_', expand=True)
    
    # Create new columns
    df_eintritt['eintrittsmonat'] = df_eintritt['start_month'].astype(int)
    df_eintritt['eintrittsjahr'] = 2000 + df_eintritt['start_year'].astype(int)
    
    # Remove aux columns and order columns
    df_eintritt.drop(columns=['eintrittsdatum','start', 'end', 'start_day', 'start_month', 'start_year'], inplace=True)
    df_eintritt = df_eintritt[['eintrittsjahr', 'eintrittsmonat', 'count']]


    # BEFRISTUNG TRANSFORMATION
    # Mapping values
    mapping = {
        1: 'befristet',
        2: 'unbefristet',
        3: 'oder'
    }
    
    df_befristung['befristung'] = df_befristung['befristung'].astype(int).map(mapping)


    # ARBEITSZEIT TRANSFORMATION
    # Mapping values
    mapping = {
        'vz': 'VOLLZEIT',
        'tz': 'TEILZEIT',
        'snw': 'SCHICHT_NACHTARBEIT_WOCHENENDE',
        'ho': 'HEIM_TELEARBEIT',
        'mj': 'MINIJOB'
    }
    
    df_zeit['arbeitszeit'] = df_zeit['arbeitszeit'].map(mapping)
    
    return df_eintritt, df_befristung, df_zeit



def save_data_to_csv(dataframes: Dict , local_path: str, file_names: tuple):

    for name in file_names:
        file_path = f'{local_path}/{name}.csv'
        dataframes[name].to_csv(file_path, index=False)


    

    
