# List of bands and their corresponding indices
import arcpy, os, pandas as pd
arcpy.env.overwriteOutput = True
from arcpy.sa import Raster
input_directory = r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all\Output files"  
output_directory = r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all\Output files\Raster to points to polygons"  # Directory to save NDVI rasters
plots = r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all\Output files\2024_Colby_TAPS_Harvest_Area.shp"  # Path to your polygon shapefile
gdb_path = os.path.join(output_directory, "NDVI_Summary.gdb")
# output_excel = os.path.join(output_directory, "NDVI_Summary.xlsx")

if not arcpy.Exists(gdb_path):
    arcpy.CreateFileGDB_management(output_directory, "NDVI_Summary.gdb")
# plots = arcpy.FeatureClassToGeodatabase_conversion(r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all\Output files\2024_Colby_TAPS_Harvest_Area.shp", gdb_path)
# Update the path for the plots dataset within the geodatabase
# plots = os.path.join(gdb_path, "2024_Colby_TAPS_Harvest_Area")

# Load the shapefile into the geodatabase if not already there
if not arcpy.Exists(plots):
    arcpy.FeatureClassToGeodatabase_conversion(r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all\Output files\2024_Colby_TAPS_Harvest_Area.shp", gdb_path)

# List to store paths of all ndvi_points feature classes
ndvi_points_list = []

# Convert each NDVI raster to points and collect them in a list
for ndvi_file in os.listdir(input_directory):
    if ndvi_file.endswith("_NDVI.tif"):
        date_str = ndvi_file[:8]  # Extract date from file name
        ndvi_raster_path = os.path.join(input_directory, ndvi_file)

        # Ensure valid name for the output feature class
        ndvi_points = os.path.join(gdb_path, f"NDVI_{date_str}_points")
        
        # Convert NDVI raster to points
        try:
            arcpy.RasterToPoint_conversion(ndvi_raster_path, ndvi_points, "Value")
            ndvi_points_list.append(ndvi_points)  # Add to list
            print(f"Converted {ndvi_file} to points.")
        
        except arcpy.ExecuteError as e:
            print(f"Error for {ndvi_file}: {e}")
# Prepare an Excel writer for output
excel_path = os.path.join(output_directory, "NDVI_Summary.xlsx")
with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
    # Loop through each set of points and summarize within polygons
    for ndvi_points in ndvi_points_list:
        date_str = os.path.basename(ndvi_points)[:13]  # Extract date from points feature class name
        summarized_output = os.path.join(gdb_path, f"{date_str}_NDVI_Summary")

        try:
        # Use Summarize Within to calculate mean NDVI values within each plot polygon
            arcpy.analysis.SummarizeWithin(
                in_polygons=plots,
                in_sum_features=ndvi_points,
                out_feature_class=summarized_output,
                keep_all_polygons="KEEP_ALL",
                sum_fields=[["grid_code", "MEAN"]],
                sum_shape="NO_SHAPE_SUM"
            )
            print(f"Calculated mean NDVI for {date_str} within each plot.")

            fields = [field.name for field in arcpy.ListFields(summarized_output) if field.type != "Geometry"]
            data = [row for row in arcpy.da.SearchCursor(summarized_output, fields)]
            df = pd.DataFrame(data, columns=fields)

            # Write each DataFrame to a separate sheet in the Excel file
            df.to_excel(writer, sheet_name=date_str, index=False)
            print(f"Saved summary for {date_str} to Excel sheet.")

        except arcpy.ExecuteError as e:
            print(f"Summarize Within error for {date_str}: {e}")


print("Processing complete. Summarized tables are saved in:", gdb_path)




# for raster_file in os.listdir(input_directory):
#     if raster_file.endswith("AnalyticMS_SR_8b_clip.tif"):
#         # Extract date part of the file name (first 8 characters)
#         date_str = raster_file[:8]

#         # Full path of the input raster Extract red and NIR bands
#         input_image = os.path.join(input_directory, raster_file)
#         for band_name, band_index in bands.items():
#             output_tif = f"{output_directory}/{date_str}_{band_name}.tif"
#             arcpy.MakeRasterLayer_management(input_image, f"{band_name}_layer", f"Band_{band_index}", band_index=band_index)
#             arcpy.CopyRaster_management(f"{band_name}_layer", output_tif, "", "", "", "NONE", "NONE", "")
#             print(f"Saved {band_name} band to {output_tif}")
            
#         print(f"Saved Red and NIR bands for {date_str}.")

#         # Calculation of NDVI Raster
#         for file in os.listdir(output_directory):
#             if file.endswith("_red.tif"):  # Only consider red band files to get unique dates
#                 date_str2 = file.split('_')[0]  # Extract date part (e.g., '20240426' from '20240426_red.tif')

#                 # Define file paths for red and NIR bands based on the date from the output directory
#                 red_band_path = os.path.join(output_directory, f"{date_str2}_red.tif")
#                 nir_band_path = os.path.join(output_directory, f"{date_str2}_nir.tif")

#                 if os.path.exists(red_band_path) and os.path.exists(nir_band_path):
#                     # Define the output path for NDVI raster
#                     ndvi_output_path = os.path.join(output_directory, f"{date_str2}_NDVI.tif")
            
#                     # Calculate NDVI = (NIR - Red) / (NIR + Red)
#                     red_raster = Raster(red_band_path)
#                     nir_raster = Raster(nir_band_path)
#                     ndvi_raster = (nir_raster - red_raster) / (nir_raster + red_raster)
            
#                     # Save the NDVI raster
#                     ndvi_raster.save(ndvi_output_path)
#                     print(f"Calculated and saved NDVI for {date_str2} to {ndvi_output_path}")
#                 else:
#                     print(f"Missing NIR or Red band for {date_str2}. Skipping NDVI calculation.")
        

#         # Delete Red and NIR Files
#         for file in os.listdir(output_directory):
#             file_path = os.path.join(output_directory, file)
#             if file.endswith("_red.tif") or file.endswith("_nir.tif"):  # Delete red and NIR bands
#                 arcpy.Delete_management(file_path)
#                 print(f"Deleted {file_path}")
            