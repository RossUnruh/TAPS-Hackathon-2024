import os
import pandas as pd
import matplotlib.pyplot as plt
import glob

# Folder containing your Excel files
folder_path = r'C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\weather-based-data'

# Define the conversion factor from inches to millimeters
inches_to_mm = 25.4

# Folder containing your Excel files
folder_path = r'C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\weather-based-data'


# Set the folder path for saving plots
output_folder = r"C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\weather-based-data\\weather-based-SWM_chart"  # Customize the folder name
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all Excel files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith("_budget.xlsx"):
        filepath = os.path.join(folder_path, filename)
        team_number = filename.split("_")[0]  # Extract team number from file name
        
        # Read data from the Excel file, sheet named 'Budget_'
        try:
            df = pd.read_excel(filepath, sheet_name="Sheet2", header=16)
        except Exception as e:
            print(f"Could not read {filename}: {e}")
            continue

        # Extract data and convert to mm
        dates = df.iloc[:, 14]  # Column O
        sw_fc = df.iloc[:, 16] * inches_to_mm  # Column Q - SW Storage @ FC
        sw_mad = df.iloc[:, 19] * inches_to_mm  # Column T - SW Storage @ MAD
        sw_pwp = df.iloc[:, 17] * inches_to_mm  # Column R - SW Storage @ PWP
        sw_avail = df.iloc[:, 20] * inches_to_mm  # Column U - Available Soil Water

        # Plotting
        plt.figure(figsize=(10, 5))
        plt.plot(dates, sw_fc, label="SW Storage @ FC", color='brown', linewidth=2)
        plt.plot(dates, sw_mad, label="SW Storage @ MAD", color='red', linestyle='--')
        plt.plot(dates, sw_pwp, label="SW Storage @ PWP", color='orange', linestyle=':')
        plt.plot(dates, sw_avail, label="Available Soil Water", color='blue', linestyle='-')

        # Customize plot appearance
        plt.xlabel("Date")
        plt.ylabel("Water Content (mm)")
        team_number = filename.split("_")[0]
        plt.title(f"Soil Available Water for Team {team_number} (Weather-based)")
        plt.legend()
        plt.grid(True)

        # Rotate x-axis labels
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot
        plot_path = os.path.join(output_folder, f"Soil_Available_Water_Team_{team_number}.png")
        plt.savefig(plot_path)
        plt.close()
        
        print(f"Plot saved for file: {filename} at {plot_path}")