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
