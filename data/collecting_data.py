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


def get_model(model_element):
    """Extracting model year features from file to features dictionary.

    Args:
        model_element (bs4.element.Tag): contains first 'h5' element
            with no css class.
    """
    for row in model_element:
        subitem = str(row.text).split()
        for item in subitem:
            if(item.isdigit()):
                features['model'] = item
                break

# Create dataframe to add the data collected
data = pd.DataFrame()

for path in Path('data/').glob('*.txt'):
    initialize_df()
    with path.open(encoding='utf-8') as file_path:
        # create BeautifulSoup object for file by html parser
        soup = BeautifulSoup(file_path, "html.parser")

        # Extracting name value to features dictionary
        features['name'] = soup.find('h3', class_=None).text

        # Extracting model value to features dictionary
        get_model(soup.find('h5', class_=None))