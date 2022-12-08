from dataclasses import dataclass

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
    additional_info: str = None
    passengers: str = None
    drive: str = None
    car_speedometer: float = None
    ex_owners: str = None
    price: float = None
    ads_start_data: str = None