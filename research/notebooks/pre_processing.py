import ast
import pandas as pd
from datetime import datetime, timedelta
# coding=utf-8

ex_owner_dict:dict = {
    'zero': ['0', '٠', 'صفر', 'صفرض', 'صفرر', 'لا شيء ','Zero','O'],
    'ones' : ['1', 'أولى', 'اولى', 'اولا', 'واحد', 'اول', 'ياولى', 'اوله', 'انا','اولي', 'واله', 'ولا', 'واحدة', 'أولئ', 'ولى',
              'أولي', 'اولئ', 'اولة', 'اةلي', '١', 'ا'],
    'two' : ['2', 'تانيه', 'ثني', 'تاني', 'ثاتيه', 'تانية', 'ثاني', 'ثانبه', 'تانبه', 'ثانيا',
             'يانيه', 'ثانية', 'ثانيه', 'اثنان', '٢'],
    'three' : ['3', 'ثالثة', 'ثالثه', 'تالثه', 'تالته', 'ثالث', 'التالته', '٣'],
    'four'  : ['4', 'اربعه', 'رابعه', 'اربعة', 'رابعة','٤'],
    'five'  : ['5', 'خامسة', 'خامسه', 'خامساً', 'خمسة', 'خمسه', '٥']
}


def passengers_number(passengers:str) -> int:
    """Calculate the number of passengers from equation

    Args:
        passengers (str): number of passenger in format (n1+n2)

    Returns:
        _int_: number of passenger
    """
    sum_digit:int = 0

    for char in passengers.split():
        if char.isdigit():
            int_char = int(char)
            sum_digit = sum_digit + int_char
    
    return sum_digit


def ex_owner_number(ex_owner:str) -> int:
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


def speedometer_number(car_speedometer:str) -> int:
    """_summary_

    Args:
        car_speedometer (str): _description_

    Returns:
        float: _description_
    """
    for item in car_speedometer.split(' '): 
        if item.isdigit():
            if len(item) <= 3:
                item = int(item) * 1000
            return int(item)


def knn_transform(sample:list) -> list:
    """_summary_

    Args:
        sample (list): _description_

    Returns:
        list: _description_
    """
    result = knn_imputer.transorm(sample) 

    return result


def min_max_scaler(sample:list) -> list:
    pass


def fill_passenger(passengers:pd.Series) -> pd.Series:
    """Fill missing data in the passengers series by mode value.

    Args:
        passengers (pd.Series): contains passengers column
    """
    mode = passengers.mode()[0]
    passengers = passengers.fillna(value=mode)
    return passengers


def outlier_values(feature:pd.Series) -> pd.Series:
    """Finds the upper and lower outliers by IQR Range

    Args:
        feature (pd.Series): contains feature data

    Returns:
        tuple: contains upper outliers and lower outliers
    """
    # Find quartile 1 and 3 of column
    q1, q3 = feature.quantile([0.25, 0.75])

    # Find IQR
    IQR = q3 - q1

    # Find the upper and lower outlier number
    upper_outlier = q3 + IQR * 1.5
    lower_outlier = q1 - IQR * 1.5

    feature.loc[feature > upper_outlier] = upper_outlier
    feature.loc[feature < lower_outlier] = lower_outlier
    
    feature.loc[feature < 0] = 0
    
    return feature


def get_quarter_date(date:pd.Series) -> pd.Series:
    """Convert from date to quarter relevent.

    Args:
        date (list): contains date data.

    Returns:
        pd.Series: Contains quarter data with possible value (1,2,3,4)
    """
    quarter = [item.quarter for item in date]
    return quarter


def str_to_datetime(date:pd.Series) -> pd.Series:
    """Convert date from string type to datetime type.

    Args:
        date (pd.Series): contains date data.

    Returns:
        pd.Series: contains quarer data.
    """
    date = [pd.Timestamp(item) for item in date]
    return date


def get_company_name(name:str):
    company = name.split(' ')[0]
    return company


def get_start_end_date(ads_duration:int):
    today_date = datetime.now()
    ads_start_date = today_date.date()
    ads_end_date = (today_date + timedelta(days=ads_duration)).date()
    return(ads_start_date, ads_end_date)

