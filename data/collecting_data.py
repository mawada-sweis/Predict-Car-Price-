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
    global features, maping_description, insurance_features

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
    maping_description = {
        "لون السيارة": 'color',
        "نوع الوقود": 'fuel_type',
        "أصل السيارة": 'origin_car',
        "عداد السيارة": 'car_speedometer',
        "أصحاب سابقون": 'ex_owners',
        "رخصة السيارة": 'car_license',
        "نوع الجير": 'lime_type',
        "الزجاج": 'glass',
        "قوة الماتور": 'motor_power',
        "عدد الركاب": 'passengers',
        "وسيلة الدفع": 'payment_method',
        "معروضة": 'displayed'
    }
    insurance_features = ['insurance_third', 'supplementary_body', 'total']


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


def get_price(price_element):
    """Extracting price feature from file to features dictionary.
    Args:
        price (bs4.element.Tag): contain 'h5' tag with no css class
    """
    price = str(price_element.text)
    for subitem in price.split():
        if(subitem.isdigit()):
            price = subitem
            break

    features['price'] = int(price)


def get_description(description_element):
    """Extracting description features from file to features dictionary.
    it has 12 features: 'color', 'fuel_type', 'origin_car',
    'car_license', 'lime_type','glass', 'motor_power', 'car_speedometer',
    'passengers', 'payment_method','displayed', 'ex_owners',

    Args:
        description_element (bs4.element.Tag): contain 'table' element
            with css class 'list_ads'
    """

    for arabic_feature in maping_description.keys():
        description = description_element.find(text=arabic_feature)
        features[maping_description[arabic_feature]] = \
            None if description is None \
            else description.next_element.get_text()


def get_insurance(insurance_element):
    """Extracting insurance features from file to features dictionary.
    it has 3 features: 'insurance_third','supplementary_body' and 'total'

    Args:
        insurance_element (bs4.element.ResultSet): contain all 'td' element
            with no css class nor css colspan from the first div element
            has css class 'row'
    """
    count = 0
    for row in insurance_element:
        subitem = str(row.text).split()
        for item in subitem:
            if(item.isdigit()):
                features[insurance_features[count]] = item
                count += 1


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

        # Extracting price value to features dictionary
        get_price(soup.find('h5', class_='post-price'))

        # Extracting description values to features dictionary
        get_description(soup.find('table', class_='list_ads'))

        # Extracting insurance values to features dictionary
        get_insurance(soup.find('div', class_='row').findAll('td',
                      attrs={'class': None, 'colspan': None}))
