import pandas as pd
import numpy as np



# Load datasets
climate_data = pd.read_csv('C:\\Priyanka\\hackthone-kansas\\Water-squad\\colby_climate_1990_2019.csv')
neutron_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\All excel data\\24 KSU_TAPS_Neutron_Tube Readings_VWC.xlsx',
    sheet_name='Sheet1', skiprows=2
)
soil_texture_data = pd.read_excel('C:\\Priyanka\\hackthone-kansas\\Water-squad\\All excel data\\24 KSU TAPS Soil texture.xlsx')

# Load the TAPS Management data
taps_planting = pd.read_excel('C:\\Priyanka\\hackthone-kansas\\Water-squad\\2024_TAPS_management.xlsx', sheet_name='Planting date', skiprows=1)
taps_nitrogen = pd.read_excel('C:\\Priyanka\\hackthone-kansas\\Water-squad\\2024_TAPS_management.xlsx', sheet_name='Nitrogen fertilizer', skiprows=2)
taps_irrigation = pd.read_excel('C:\\Priyanka\\hackthone-kansas\\Water-squad\\2024_TAPS_management.xlsx', sheet_name='Irrigation amounts', skiprows=1)

# Preprocess irrigation data
irrigation_long = taps_irrigation.melt(id_vars=['ID'], var_name='Date', value_name='Irrigation')
irrigation_long['Date'] = pd.to_datetime(irrigation_long['Date'], errors='coerce').dt.date
irrigation_long = irrigation_long.groupby(['ID', 'Date']).agg({'Irrigation': 'sum'}).reset_index()

# Summarize nitrogen data
taps_nitrogen.columns = taps_nitrogen.columns.str.strip()  # Strip spaces from column names
nitrogen_totals = taps_nitrogen.groupby('ID')['Total (lbs/ac)'].sum().reset_index()

# Convert neutron data date column
neutron_data['Date'] = pd.to_datetime(neutron_data['Date'], errors='coerce')
depth_columns = [6, 18, 30, 42, 54, 66, 78, 90, 102, 114]