#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    File name: Reformat Excel.py
#    Author: Ross Unruh
#    Description:  Reformat .XLSX File and Convert to .CSV
#    Date created: 10/30/2024
#    Python Version: 3.9.16

# Import required modules and classes:
import pandas as pd, arcpy

# Define key environment settings:
arcpy.env.workspace = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\Data" # Path to folder containing excel file.
arcpy.env.overwriteOutput = True

# Load the Excel file, skipping the first row
input_excel = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\Data\24 KSU TAPS Soil texture.xlsx" # Path to excel file.
sheet_name = "data"
df = pd.read_excel(input_excel, sheet_name=sheet_name, skiprows=1)

# Rename columns to remove special characters and spaces
df.columns = df.columns.str.replace(r'[%() ]', '_', regex=True)

# Convert excel file into .csv file.
output_csv = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\Data\output.csv" # Desired path of output
df.to_csv(output_csv, index=False)
print(arcpy.GetMessages())
