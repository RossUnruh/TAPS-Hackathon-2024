#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    File name: Convert CSV to SHP.py
#    Author: Ross Unruh
#    Description:  Reformat .CSV to .SHP
#    Date created: 10/30/2024
#    Python Version: 3.9.16

# Import required modules and classes:
import arcpy

# Set up environment settings
arcpy.env.workspace = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\2024 TAPS Hackathon - Water Squad\2024 TAPS Hackathon - Water Squad.gdb" # Replace with your workspace path
arcpy.env.overwriteOutput = True

# Function to create shapefile from CSV
def create_shapefile_from_csv(input_csv, x_field, y_field, output_shapefile):
    # Step 1: Create an XY event layer from the CSV
    temp_layer = "in_memory\\temp_layer"
    arcpy.MakeXYEventLayer_management(input_csv, x_field, y_field, temp_layer)
    
    # Step 2: Export the event layer to a shapefile, keeping all fields including Z
    arcpy.CopyFeatures_management(temp_layer, output_shapefile)
    
    print(f"Shapefile created at: {output_shapefile}")

# Input CSV file path
input_csv = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\Data\output.csv"  # Path to your uploaded CSV file

# Define column names based on your CSV structure
x_field = "Lng"  # Replace with the X coordinate field name in your CSV
y_field = "Lat"   # Replace with the Y coordinate field name in your CSV

# Output shapefile path
output_shapefile = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\2024 TAPS Hackathon - Water Squad\2024 TAPS Hackathon - Water Squad.gdb\output_shapefile"  # Define output location and name

# Run the shapefile creation function
create_shapefile_from_csv(input_csv, x_field, y_field, output_shapefile)

