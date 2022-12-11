import pandas as pd
import numpy as np
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


def modify_passengers(passengers:pd.Series) -> pd.Series:
    """Modify given passengers data from string in format(num1+num2) to
    sum of these 2 numbers.

    Args:
        passengers (pd.Series): contains passengers data as strint type.

    Returns:
        pd.Series: passengers data modified as integer type.
    """
    passengers_modified:list = []
    
    for row in passengers:
        sum_digit:int = 0
        row = str(row)
        for char in row.split('+'):
            if char.isdigit():
                int_char = int(char)
                sum_digit = sum_digit + int_char
        if sum_digit == 0 :
            passengers_modified.append(np.NaN)
        else:  
            passengers_modified.append(sum_digit)
    return passengers_modified


def _ex_owner_number(ex_owner:str) -> int:
    """Find whether the value exists in ex_owner_dict, 
        will return the number related if it exisit.

    Args:
        ex_owner (str): contains ex owner of car

    Returns:
        int: number of ex owner from 0 to 5
    """
    for item in ex_owner.split(' '):
        for ex_owner_id in ex_owner_dict.keys():
            if item in ex_owner_dict.get(ex_owner_id):
                return int(ex_owner_dict.get(ex_owner_id)[0])


def modify_ex_owner(ex_owner:pd.Series) -> pd.Series:
    """Modify the value in the given ex owner data that 
        represents the number of ex-owners of the car to 
        a number that indicates this value.

    Args:
        ex_owner (pd.Series): contains ex_owner data as strint type.

    Returns:
        pd.Series: ex_owner data modified as integer type.
    """
    ex_owner_modified = []

    for row in ex_owner:
        if pd.isna(row):
            ex_number = np.NaN
        else:
            ex_number = _ex_owner_number(str(row)) if _ex_owner_number(str(row)) else np.NaN
        
        ex_owner_modified.append(ex_number)
    
    return ex_owner_modified


def _speedometer_number(car_speedometer:str) -> int:
    """Check the type of data and return the number in 
    thousand format. 

    Args:
        car_speedometer (str): car_speedometer data in string format.

    Returns:
        float: car_speedometer number in thousand format.
    """
    for item in car_speedometer.split(' '): 
        if item.isdigit():
            if len(item) <= 3:
                item = int(item) * 1000
            return int(item)


def modify_speedometer(car_speedometer:pd.Series) -> pd.Series:
    """Keeping on the numbers in thousand format,
    Modify the ones, tens and hundreds numbers to thousand format and
    Replace the string value to a numpy NaN value.

    Args:
        car_speedometer (pd.Series): contains car speedometer data.

    Returns:
        pd.Series: car_speedometer data modified as integer type.
    """
    speedometer_modified = []
    for row in car_speedometer:
        if pd.isna(row):
            speedometer_modified.append(np.NaN)
        else:
            speedometer_modified.append(_speedometer_number(str(row)) if _speedometer_number(str(row)) else  np.NaN)
    return speedometer_modified


def str_to_datetime(date:pd.Series) -> pd.Series:
    """Convert date from string type to datetime type.

    Args:
        date (pd.Series): contains date data.

    Returns:
        pd.Series: contains quarer data.
    """
    date = [pd.Timestamp(item) for item in date]
    return date


def fill_passenger(passengers:pd.Series) -> pd.Series:
    """Fill missing data in the passengers series by mode value.

    Args:
        passengers (pd.Series): contains passengers column

    Returns:
        pd.Series: passengers data without missing data
    """
    mode = passengers.mode()[0]
    passengers = passengers.fillna(value=mode)
    return passengers


def outlier_values(feature:pd.Series) -> pd.Series:
    """Change any value above/below the value of the 
    upper/lower outlier to the upper/lower value of the upper/lower outlier.
    Feature must contain numaric value.

    Args:
        feature (pd.Series): contains feature data want to handled its outlier.

    Returns:
        pd.Series: Modified feature (without outlier).
    """
    # Find quartile 1 and 3 of column
    q1, q3 = feature.quantile([0.25, 0.75])

    # Find IQR
    IQR = q3 - q1

    # Find the upper and lower outlier number
    upper_outlier = q3 + IQR * 1.5
    lower_outlier = q1 - IQR * 1.5
    
    # Remove outlier
    feature.loc[feature > upper_outlier] = upper_outlier
    feature.loc[feature < lower_outlier] = lower_outlier
    
    # Remove any negative number
    feature.loc[feature < 0] = 0
    
    return feature


def get_quarter_date(date:pd.Series) -> pd.Series:
    """Extract quarter relevent from date.

    Args:
        date (list): contains date data.

    Returns:
        pd.Series: Contains quarter data with possible value (1,2,3,4)
    """
    quarter = [item.quarter for item in date]
    return quarter


def modify_name(names:pd.Series) -> pd.Series:
    """Extract company name from data given and 
    replace the company name with origin name.

    Args:
        names (pd.Series): contains car name as string type. 

    Returns:
        pd.Series: Modified names data contains company name only.
    """
    for index, row in enumerate(names):
        names.at[index] = row.split(' ')[0]
    return names

