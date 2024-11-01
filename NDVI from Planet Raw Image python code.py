# List of bands and their corresponding indices
import arcpy
import os
arcpy.env.overwriteOutput = True
from arcpy.sa import Raster
input_directory = r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all"  
output_directory = r"C:\Users\rgvjoshi\Downloads\Hackathon Datasets\Codes\NDVI calculation Planet\Planet dataset all\Output files"  # Directory to save NDVI rasters

# Band indices for Red and NIR bands
bands = {
    "red": 6,
    "nir": 8
}
for raster_file in os.listdir(input_directory):
    if raster_file.endswith("AnalyticMS_SR_8b_clip.tif"):
        # Extract date part of the file name (first 8 characters)
        date_str = raster_file[:8]

        # Full path of the input raster Extract red and NIR bands
        input_image = os.path.join(input_directory, raster_file)
        for band_name, band_index in bands.items():
            output_tif = f"{output_directory}/{date_str}_{band_name}.tif"
            arcpy.MakeRasterLayer_management(input_image, f"{band_name}_layer", f"Band_{band_index}", band_index=band_index)
            arcpy.CopyRaster_management(f"{band_name}_layer", output_tif, "", "", "", "NONE", "NONE", "")
            print(f"Saved {band_name} band to {output_tif}")
            
        print(f"Saved Red and NIR bands for {date_str}.")

        # Calculation of NDVI Raster
        for file in os.listdir(output_directory):
            if file.endswith("_red.tif"):  # Only consider red band files to get unique dates
                date_str2 = file.split('_')[0]  # Extract date part (e.g., '20240426' from '20240426_red.tif')

                # Define file paths for red and NIR bands based on the date from the output directory
                red_band_path = os.path.join(output_directory, f"{date_str2}_red.tif")
                nir_band_path = os.path.join(output_directory, f"{date_str2}_nir.tif")

                if os.path.exists(red_band_path) and os.path.exists(nir_band_path):
                    # Define the output path for NDVI raster
                    ndvi_output_path = os.path.join(output_directory, f"{date_str2}_NDVI.tif")
            
                    # Calculate NDVI = (NIR - Red) / (NIR + Red)
                    red_raster = Raster(red_band_path)
                    nir_raster = Raster(nir_band_path)
                    ndvi_raster = (nir_raster - red_raster) / (nir_raster + red_raster)
            
                    # Save the NDVI raster
                    ndvi_raster.save(ndvi_output_path)
                    print(f"Calculated and saved NDVI for {date_str2} to {ndvi_output_path}")
                else:
                    print(f"Missing NIR or Red band for {date_str2}. Skipping NDVI calculation.")
        

        # Delete Red and NIR Files
        for file in os.listdir(output_directory):
            file_path = os.path.join(output_directory, file)
            if file.endswith("_red.tif") or file.endswith("_nir.tif"):  # Delete red and NIR bands
                arcpy.Delete_management(file_path)
                print(f"Deleted {file_path}")
            
       
print("Processing complete.")
