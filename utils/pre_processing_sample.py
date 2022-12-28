import pandas as pd
import pickle
from datetime import datetime, timedelta


def load_pickle(path: str) -> pickle:
    """Loading pickle path given.

    Args:
        path (str): Pick path

    Returns:
        pickle: pickle loaded
    """
    with open(path, 'rb') as pkl_file:
        return pickle.load(pkl_file)

# Load necessary pickles
encoder = load_pickle('research/pkls/onehot_encoder.pkl')
scaler = load_pickle('research/pkls/min_max_scaler.pkl')
model = load_pickle('research/pkls/gradient_model.pkl')

# List of features name need onehot encoding
one_hot_features = ['name', 'color', "glass_type", "fuel_type", "car_type", 
                    "license_type", "lime_type", "payment_method", "display_purpose"]

# Dictionary of possible words of ex owner value
ex_owner_dict = {
    'zero': ['0', '٠', 'صفر', 'صفرض', 'صفرر', 'لا شيء ','Zero','O'],
    'ones' : ['1', 'أولى', 'اولى', 'اولا', 'واحد', 'اول', 'ياولى', 'اوله', 'انا','اولي', 'واله', 'ولا', 'واحدة', 'أولئ', 'ولى',
            'أولي', 'اولئ', 'اولة', 'اةلي', '١', 'ا'],
    'two' : ['2', 'تانيه', 'ثني', 'تاني', 'ثاتيه', 'تانية', 'ثاني', 'ثانبه', 'تانبه', 'ثانيا',
            'يانيه', 'ثانية', 'ثانيه', 'اثنان', '٢'],
    'three' : ['3', 'ثالثة', 'ثالثه', 'تالثه', 'تالته', 'ثالث', 'التالته', '٣'],
    'four'  : ['4', 'اربعه', 'رابعه', 'اربعة', 'رابعة','٤'],
    'five'  : ['5', 'خامسة', 'خامسه', 'خامساً', 'خمسة', 'خمسه', '٥']
}


def get_start_end_date(ads_duration:int) -> tuple[datetime.date, datetime.date]:
    """Extract start and end date ads based on ads duration given.

    Args:
        ads_duration (int): The duration of the ads in days

    Returns:
        tuple[datetime.date, datetime.date]: start and end date of ads as a tuple
    """
    ads_start_date = datetime.now()
    ads_end_date = (ads_start_date + timedelta(days=ads_duration)).date()
    return (ads_start_date.date(), ads_end_date)


def get_quarter_date(date:list) -> pd.Series:
    """Convert from date to quarter relevent.

    Args:
        date (list): contains date data.

    Returns:
        pd.Series: Contains quarter data with possible value (1,2,3,4)
    """
    quarter = [(item.month-1)//3+1 for item in date]
    return quarter


def get_passengers_number(passengers:str) -> int:
    """Calculate the number of passengers from equation

    Args:
        passengers (str): number of passenger in format (n1+n2)

    Returns:
        _int_: number of passenger
    """
    sum_digit:int = 0

    for char in passengers:
        if char.isdigit():
            int_char = int(char)
            sum_digit = sum_digit + int_char
    
    return sum_digit


def get_ex_owner_number(ex_owner:str) -> int:
    """Takes the user value of ex owner and find whether the
    value contains in ex_owner_dict, will return the number if it exisit.

    Args:
        ex_owner (str): contains ex owner of car

    Returns:
        int: number of ex owner from 0 to 5
    """
    for item in ex_owner.split(' '):
        for ex_owner_id in ex_owner_dict.keys():
            if item in ex_owner_dict.get(ex_owner_id):
                return int(ex_owner_dict.get(ex_owner_id)[0])
    return 0


def get_speedometer_number(car_speedometer:str) -> int:
    for item in car_speedometer.split(' '): 
        if item.isdigit():
            if len(item) <= 3:
                item = int(item) * 1000
            return int(item)
    return 0


def get_company_name(name:str) -> str:
    """Extracts the company name from the given name.

    Args:
        name (str): The name of the car

    Returns:
        str: The company name
    """
    company = name.split(' ')[0]
    return company


def encoding(sample:list) -> list:
    """Encodes the given sample using one-hot encoding.

    Args:
        sample (list): The sample to be encoded

    Returns:
        list: The encoded sample
    """
    to_onehot = pd.DataFrame(sample, columns=one_hot_features)
    
    sample_encoded = encoder.transform(to_onehot)
    return list(sample_encoded.values[0])


def min_max_scaler(sample:list) -> list:
    """Scales the given sample using min-max scaling.

    Args:
        sample (list): The sample to be scaled

    Returns:
        list: The scaled sample
    """
    sample_scaled = scaler.transform(sample)
    return sample_scaled


def pridict_price(sample:list) -> float:
    """Predicts the price of the given sample using a trained model.

    Args:
        sample (list): The sample for which the price is to be predicted

    Returns:
        float: The predicted price
    """
    sample = pd.DataFrame([sample])
    price = model.predict(sample)
    return price
