import warnings
from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import re

warnings.simplefilter(action='ignore', category=FutureWarning)

def initialize_df():
    '''Create the necessary dataframes for extracting features
    from the files.
    '''
    global features

    features = {
        'name': None,
        'model': None,
        'price': None,
        'color': None,
        'fuel_type': None,
        'origin_car': None,
        'car_license': None,
        'lime_type': None,
        'glass': None,
        'motor_power': None,
        'car_speedometer': None,
        'passengers': None,
        'payment_method': None,
        'displayed': None,
        'ex_owners': None,
        'additional_info': None,
        'insurance_third': None,
        'supplementary_body': None,
        'total': None,
        'ads_status': None,
        'ads_start_data': None,
        'ads_end_data': None,
        }


# Create dataframe to add the data collected
data = pd.DataFrame()

for path in Path('data/').glob('*.txt'):
    initialize_df()
    with path.open(encoding='utf-8') as file_path:
        # create BeautifulSoup object for file by html parser
        soup = BeautifulSoup(file_path, "html.parser")

        # Extracting name value to features dictionary
        features['name'] = soup.find('h3', class_=None).text
