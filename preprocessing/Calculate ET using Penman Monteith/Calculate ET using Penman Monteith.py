import pandas as pd
import math
# input_directory = r"C:\Users\rgvjoshi\OneDrive - Kansas State University\Desktop\Hackathon Datasets\KanSched\Rough Pennman"  
# output_directory = r"C:\Users\rgvjoshi\OneDrive - Kansas State University\Desktop\Hackathon Datasets\KanSched\Rough Pennman"  # Directory to save NDVI rasters


# Load the data
data = pd.read_csv(r'C:\Users\rgvjoshi\OneDrive - Kansas State University\Desktop\Hackathon Datasets\KanSched\Rough Pennman\colby_station_kansas_mesonet.csv')

# Check if SRAVG is in langleys and convert to MJ/m²/day if necessary
if 'SRAVG' in data.columns:
    data['SRAVG_MJ_m2_day'] = data['SRAVG'] * 0.04184
else:
    raise ValueError("Solar radiation data (SRAVG) is missing from the dataset.")

# Constants
Gsc = 0  # Soil heat flux density, assumed to be zero for daily ET₀
alpha = 0.23  # Albedo for a reference crop
z = 2  # Wind measurement height in meters
Cn = 900  # Constant for daily time step (FAO-recommended)
Cd = 0.34  # Constant for daily time step (FAO-recommended)

# Convert wind speed to the reference height if needed (2m assumed here)
data['u2'] = data['WSPD2MAVG']  # Wind speed at 2 meters

# Calculate ET₀ based on FAO Penman-Monteith equation
def calculate_et0(row):
    T_mean = row['TEMP2MAVG']  # Average temperature (°C)
    RH_mean = row['RELHUM2MAVG']  # Mean relative humidity (%)
    SR = row['SRAVG_MJ_m2_day']  # Solar radiation in MJ/m²/day
    u2 = row['u2']  # Wind speed at 2m height (m/s)

    # Saturation vapor pressure (kPa)
    es = 0.6108 * math.exp((17.27 * T_mean) / (T_mean + 237.3))
    
    # Actual vapor pressure (kPa)
    ea = es * (RH_mean / 100)
    
    # Slope of the saturation vapor pressure curve (kPa/°C)
    delta = (4098 * es) / ((T_mean + 237.3) ** 2)
    
    # Psychrometric constant (kPa/°C)
    P = 101.3 * ((293 - 0.0065 * 2) / 293) ** 5.26  # Atmospheric pressure (kPa)
    gamma = 0.000665 * P
    
    # Net radiation at crop surface (MJ/m²/day)
    Rn = (1 - alpha) * SR - Gsc
    
    # FAO Penman-Monteith ET₀ calculation (mm/day)
    ET0 = ((0.408 * delta * Rn) + (gamma * (Cn / (T_mean + 273)) * u2 * (es - ea))) / (delta + gamma * (1 + Cd * u2))
    
    return ET0

# Apply the function to calculate ET₀ for each row
data['ET0'] = data.apply(calculate_et0, axis=1)

# # Display the first few rows of the resulting dataframe with ET₀ values
# print(data[['Date', 'ET0']].head())

# Save the updated data to a new Excel file
data.to_excel("C:\\Users\\rgvjoshi\\OneDrive - Kansas State University\\Desktop\\Hackathon Datasets\\KanSched\\Rough Pennman\\Rough Pennmanweather_data_with_ET0.xlsx", index=False)
print("ET₀ calculation complete. Results saved to 'Rough Pennmanweather_data_with_ET0.xlsx'.")
