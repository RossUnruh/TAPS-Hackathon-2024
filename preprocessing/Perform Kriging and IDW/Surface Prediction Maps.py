#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    File name: Surface Prediction Maps.py
#    Author: Ross Unruh
#    Description:  Create Kriging and IDW Surface Prediction Maps
#    Date created: 10/30/2024
#    Python Version: 3.9.16
#    Available with Spatial Analyst license.
#    Available with 3D Analyst license.

# Import required modules and classes:
import arcpy, time
from arcpy.sa import *

# Set environment settings
arcpy.env.workspace = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\2024 TAPS Hackathon - Water Squad\2024 TAPS Hackathon - Water Squad.gdb"
arcpy.env.extent = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\Data\Map with all plots\2024_Colby_TAPS_Harvest_Area.shp"
arcpy.env.overwriteOutput = True

# Set local variables
in_point_features = r"C:\Users\runru\Desktop\2024 TAPS Hackathon\2024 TAPS Hackathon - Water Squad\2024 TAPS Hackathon - Water Squad.gdb\output_shapefile"
z_field = "Clay____" # Input name of column header for the desired z-field.
kriging_model = "SPHERICAL" # Set the kriging method.

# Create Symbology Reference
#symbologyRef = r"C:\Users\runru\Desktop\Master's\2024 TAPS Hackathon\ArcGIS Pro Project\symbology_reference.lyrx"

#Preform Kriging
outKrig = arcpy.sa.Kriging(in_point_features, z_field, KrigingModelOrdinary(kriging_model))
outKrig.save('{0}_kriged'.format(z_field))
arcpy.GetMessages()

# Preform IDW
outIDW = arcpy.sa.Idw(in_point_features,z_field)
outIDW.save('{0}_IDW'.format(z_field))
