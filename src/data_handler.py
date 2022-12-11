from dataclasses import dataclass, field
import json
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, './utils')
import pre_processing_sample as PSP
import os
oldpwd = os.getcwd()
os.chdir('research')
features_metadata = open('metadata/features_metadata.txt')
features_metadata = json.load(features_metadata)


@dataclass
class Sample:
    name: str
    model: int
    color: str
    motor_power: float
    car_type: str
    car_license: str
    lime_type: str
    fuel_type: str
    glass: str
    displayed: str
    payment_method: str
    ads_duration:int
    # additional_info: str = field(default="No additional")
    passengers: str = field(repr=False, default= str(features_metadata['passengers'].get('Handled_NaN')))
    # drive: str = None
    car_speedometer: float = field(default=features_metadata['car_speedometer'].get('default_value'))
    ex_owners: str = None
    price: float = None
    
        
    def __post_init__(self):
        self.ads_start_date, self.ads_end_date = PSP.get_start_end_date(self.ads_duration)
        self.ads_start_date, self.ads_end_date = PSP.get_quarter_date([self.ads_start_date, self.ads_end_date])
        self.passengers = PSP.get_passengers_number(self.passengers)
        self.ex_owners = PSP.get_ex_owner_number(self.ex_owners)
        self.car_speedometer = PSP.get_speedometer_number(str(self.car_speedometer))
        self.name = PSP.get_company_name(self.name)
        self.motor_power, self.car_speedometer = PSP.min_max_scaler([[self.motor_power, self.car_speedometer]])[0]
        
        self.onehot_values, self.onehot_columns = PSP.onehot_encoding([[self.name, self.color, self.glass, self.fuel_type, self.car_type, 
                                                  self.car_license, self.lime_type, self.payment_method, self.displayed]])
        
        self.data_ready:list = [self.model, self.motor_power, self.car_speedometer, self.passengers, self.ex_owners,
                                          self.ads_start_date, self.ads_end_date]+ self.onehot_values
        self.price = PSP.pridict_price(self.data_ready, self.onehot_columns)
