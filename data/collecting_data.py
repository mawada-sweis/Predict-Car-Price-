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
    global features, maping_description, insurance_features, ads_features

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
    ads_features = ['ads_status', 'ads_start_data', 'ads_end_data']


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


def get_additional(additional_element):
    """Extracting additional feature from file to features dictionary.

    Args:
        additional_element (bs4.element.Tag): contain 'td' element with
            css class 'list-additions'
    """
    additional_value = []
    additional_element = additional_element.findAll('li')

    for row in additional_element:
        value = ''
        value += row.text
        additional_value.append(value)
    additional_value = ','.join(map(str, additional_value))

    features['additional_info'] = additional_value


def get_post_info(post_info_element):
    """Extracting post information features from file to features dictionary.
    it has 3 features: 'ads_status', 'ads_start_data' and 'ads_end_data'

    Args:
        post_info_element (bs4.element.ResultSet): contains the third 'table'
            element with css class 'create_post'
    """
    post_info_element = str(post_info_element.text).split()
    date_with_str = [post_info_element[5], post_info_element[8]]

    features['ads_status'] = post_info_element[2]

    for index in range(len(date_with_str)):
        match = re.search(r'\d{4}-\d{2}-\d{2}', date_with_str[index])
        features[ads_features[index+1]] = match.group()


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

        # Extracting additional value to features dictionary
        get_additional(soup.find('td', class_='list-additions'))

        # Extracting post information values to features dictionary
        get_post_info(soup.findAll('table', class_='create_post')[2])

        # Convert the dictionary to series
        sample = pd.Series(features)

        # Concating the sample series to the dataframe
        data = pd.concat((data, sample), axis=1, ignore_index=True)

# Transpose dataframe
data = data.T
