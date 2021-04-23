"""This script does unit and integration tests for the model scoring process."""

#Importing pytest library.
import pytest

#Importing the data and functions that will be tested.
from final import INPUT_JSON, SCALER_URL, WEEKDAYS, HOURS, read_input, input_conversion, feature_engineering

#Reading the input JSON file.
input_spec = read_input(INPUT_JSON)

### --- Unit Testing ---

#Expected values from the unit tests.
EXPECTED_WEEKDAYS = ['weekday_Mon', 'weekday_Tue', 'weekday_Wed', 'weekday_Thu', 'weekday_Fri', 'weekday_Sat', 'weekday_Sun']
EXPECTED_HOURS = ['hour_00h', 'hour_01h', 'hour_02h', 'hour_03h', 'hour_04h', 'hour_05h', 'hour_06h', 'hour_07h', 'hour_08h', 'hour_09h', 'hour_10h', 'hour_11h', 
                  'hour_12h', 'hour_13h', 'hour_14h', 'hour_15h', 'hour_16h', 'hour_17h', 'hour_18h', 'hour_19h', 'hour_20h', 'hour_21h', 'hour_22h', 'hour_23h']

#Result from the input_conversion function.
total_items, discount, weekday, hour = input_conversion(input_spec, SCALER_URL)

def test_weekday():
    """This function tests if the "weekday" value is appropriate after running the input_conversion function."""

    #The "weekday" value must be one the EXPECTED_WEEKDAYS values.
    assert weekday in EXPECTED_WEEKDAYS

def test_hour():
    """This function tests if the "hour" value is appropriate after running the input_conversion function."""

    #The "hour" value must be one the EXPECTED_HOURS values.
    assert hour in EXPECTED_HOURS

### --- Integration Testing ---

#Result from the feature_engineering function.
input_df = feature_engineering(total_items, discount, weekday, hour, WEEKDAYS, HOURS)

def test_feature_range():
    """This function tests if all the values range from 0 to 1 after running the feature_engineering function."""

    #The values for all the features must have a minimum >= 0 and maximum <= 1
    assert all(input_df.min() >= 0) and all(input_df.max() <= 1)
