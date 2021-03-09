"""This script does unit and integration tests for the model training process."""

#Importing 3rd-party libraries
import pandas as pd
import pytest

#Importing the data and functions that will be tested
from hw5_script import DATA_PATH, data_cleaning, feature_engineering

#Reading the data
ulabox_data = pd.read_csv(DATA_PATH)

### --- Unit Testing ---

#Expected values from the unit tests
EXPECTED_DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
EXPECTED_HOURS = ['00h', '01h', '02h', '03h', '04h', '05h', '06h', '07h', '08h', '09h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h', '21h', '22h', '23h']

#Output from the data_cleaning function
ulabox_data = data_cleaning(ulabox_data)

#Output of the unique column values in 'weekday' and 'hour'
output_days = sorted(ulabox_data['weekday'].unique())
output_hours = sorted(ulabox_data['hour'].unique())

def test_weekday():
    """This function tests if the 'weekday' column has the correct values after running the data_cleaning function."""

    #The ouptut_days must be the same as the EXPECTED_DAYS
    assert output_days == sorted(EXPECTED_DAYS)

def test_hour():
    """This function tests if the 'hour' column has the correct values after running the data_cleaning function."""

    #The ouptut_days must be the same as the EXPECTED_HOURS
    assert output_hours == sorted(EXPECTED_HOURS)


### --- Integration Testing ---

#Output from the feature_engineering function
ulabox_data = feature_engineering(ulabox_data)

def test_feature_range():
    """This function tests if all the values range from 0 to 1 after running the feature_engineering function."""

    #The values for all the columns must have a minimum >= 0 and maximum <= 1
    assert all(ulabox_data.min() >= 0) and all(ulabox_data.max() <= 1)
