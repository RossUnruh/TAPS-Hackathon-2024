import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder containing your Excel files
folder_path = r'C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\weather-based-data'


# Set the folder path for saving plots
output_folder = r"C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\weather-based-data\\weather-based-graphs"  # Customize the folder name
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each Excel file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith("_budget.xlsx"):
        # Extract team number from the file name
        file_path = os.path.join(folder_path, file_name)
        team_number = file_name.split("_")[0]
        
        # Read data from the file
        df = pd.read_excel(file_path, sheet_name="Sheet2", skiprows=16)
        
        # Extract columns by position: column O for dates and column V for soil water data
        x_data = df.iloc[:, 14].dropna()  # Column 'O' (Date)
        y_data = df.iloc[:, 21].dropna()  # Column 'V' (Soil Water Data)
        
        # Ensure x_data and y_data have the same length
        min_length = min(len(x_data), len(y_data))
        x_data = x_data[:min_length]
        y_data = y_data[:min_length]

        # Create plot
        plt.figure()
        plt.plot(x_data, y_data, linestyle='-', color='b')
        plt.xlabel('Date')
        plt.ylabel('Soil Available Water')
        plt.title(f"Soil Available Water after Emergence for Team {team_number} (Weather-based)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save the plot with a filename indicating the team
        plot_path = os.path.join(output_folder, f"Soil_Available_Water_Team_{team_number}.png")
        plt.savefig(plot_path)
        plt.close()
        print(f"Plot saved for file: {file_name} at {plot_path}")

