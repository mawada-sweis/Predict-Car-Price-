import json
import os
import sys
import pandas as pd
import pickle
from datetime import datetime, timedelta

def get_start_end_date(ads_duration:int) -> datetime.date:
    """Extract start and end date ads based on ads duration given.

    Args:
        ads_duration (int)

    Returns:
        datetime.date: start and end date of ads
    """
    ads_start_date = datetime.now()
    ads_end_date = (ads_start_date + timedelta(days=ads_duration)).date()
    return (ads_start_date.date(), ads_end_date)


def get_quarter_date(date:list) -> list:
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
    
    for item in ex_owner.split(' '):
        for ex_owner_id in ex_owner_dict.keys():
            if item in ex_owner_dict.get(ex_owner_id):
                return int(ex_owner_dict.get(ex_owner_id)[0])


def get_speedometer_number(car_speedometer:str) -> int:
    for item in car_speedometer.split(' '): 
        if item.isdigit():
            if len(item) <= 3:
                item = int(item) * 1000
            return int(item)


def get_company_name(name:str):
    company = name.split(' ')[0]
    return company


def onehot_encoding(sample:list):
    one_hot_features = ['name', 'color', "glass_type", "fuel_type", "car_type", 
                    "license_type", "lime_type", "payment_method", "display_purpose"]
    to_onehot = pd.DataFrame(sample, columns=one_hot_features)
    
    file = open('pkls/onehot_encoder.pkl', 'rb')
    encoder = pickle.load(file)
    file.close()
    
    sample_encoded = encoder.transform(to_onehot)
    return list(sample_encoded.values[0]), encoder.get_feature_names()

def min_max_scaler(sample:list):
    file = open('pkls/min_max_scaler.pkl', 'rb')
    scaler = pickle.load(file)
    file.close()
    sample_scaled = scaler.transform(sample)
    return sample_scaled


def pridict_price(sample:list, onehot_columns:list):
    file = open('pkls/model.pkl', 'rb')
    model = pickle.load(file)
    file.close()
    sample = pd.DataFrame([sample])
    sample = polynomial_features(sample)
    price = model.predict(sample)
    return price

def polynomial_features(sample):
    file = open('pkls/polynomial_features.pkl', 'rb')
    poly = pickle.load(file)
    file.close()
    
    return poly.transform(sample)
    