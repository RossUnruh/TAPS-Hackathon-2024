# KState Hackathon 2024 - Water Intelligence Dashboard for Sustainable Agriculture 

This dashboard provides data analysis and visualizations from Kansas State University TAPS (Testing Ag Performance Solutions) Project—an interactive farm management competition with 34 participating teams. The purpose of this dashboard is to support farmers and competitors by highlighting trends and insights from their plots, guiding more effective and sustainable management decisions.

## Dashboard Overview 

The dashboard is organized into six primary tabs, each focusing on different aspects of data analysis:

1. **TAPS Management**
2. **Environmental Parameters**
3. **Spatial Analysis**
4. **Soil Moisture Sensor-based SW Management**
5. **Weather-based SW Management**
6. **Satellite-based SW Management**

Each tab serves a specific role in helping participants assess various management, environmental, and soil moisture parameters within their plots.

## Tab Descriptions 

### TAPS Management 

The TAPS Management tab uses data from the "management" folder in the datasets directory to display key management decisions for each team. Information provided includes:

- Planting Dates
- Seeding Rates
- Nitrogen Fertilizer Applications
- Irrigation Events

These management details are displayed in team-specific plots, allowing participants to visualize and evaluate resource usage and decision-making strategies.

### Environmental Parameters 

This tab incorporates Kansas Mesonet data from the Colby station to track weather trends during the 2024 corn-growing season, providing insights into:

- Temperature
- Precipitation
- Relative Humidity
- Evapotranspiration 

Monitoring these environmental parameters helps teams understand weather impacts on their plots and adjust their management practices accordingly.

### Spatial Analysis 

The Spatial Analysis tab creates soil textural prediction surface maps using interpolation methods of Kriging and Inverse Distance Weighted (IDW). IDW uses point data (data which includes X and Y coordinates) to predict the value of the Z field (the value connected to the X and Y coordinates, e.g., Silt (%)) across a defined extent, such as a field boundary. In this case, there were 10 soil sampling locations used to predict the texture across the entire TAPS boundary.

Also, the Spatial Analysis tab utilizes satellite imagery from Planet Labs to present variations in NDVI (Normalized Difference Vegetation Index) throughout the growing season.

This section includes:

- NDVI Maps for observing vegetation health and growth
- Soil Texture Prediction Maps using Kriging and Inverse Distance Weighted (IDW) interpolation methods

### Soil Moisture Sensor-based SW Management  

This tab presents soil moisture data from Sentek soil moisture sensors, calculating daily soil moisture storage within a 90 cm soil profile. It also calculates available water using field capacity (FC) and permanent wilting point (PWP) for the relevant soil textural class. The visualizations allow users to track moisture variation based on sensor readings and assess available water levels over time.

### Weather-based SW Management 

This tab leverages basic weather data from the Colby Mesonet station to calculate reference evaporation (ET₀) using the FAO 56 Penman-Monteith equation. ET₀ values are integrated with the “K-State KANSCHED” model, which uses additional inputs such as crop emergence date, root zone depth, and field capacity and permanent wilting point for the relevant textural class. The model combines irrigation events, rainfall, and other data to estimate daily soil water availability and visualize volumetric water content.

### Satellite-based SW Management  

The NDVI-based soil moisture tab provides spatial maps developed from Planet Labs satellite imagery using ArcPy. For each available image date, NIR and Red Bands are processed with the “Raster Calculator” tool to create NDVI maps. NDVI values for each plot are extracted, and crop coefficients are calculated using the formulas:

- `fc = 1.26 × NDVI – 0.18`
- `Kcbrf = 1.13 × fc + 0.14`

Where `fc` represents vegetation fractional cover, and `Kcbrf` is the reflectance-based crop coefficient. These insights into vegetation health guide crop water usage decisions.

### Neutron Probe Soil Moisture Data 

This additional tab displays soil moisture variation by plot, based on data from neutron probes. This information allows competitors to compare moisture levels within the soil profile, gaining insights into the efficiency of irrigation and soil retention strategies.

## Conclusion

The **KState Hackathon 2024 - Water Intelligence Dashboard for Sustainable Agriculture** offers a comprehensive view of management, environmental, and soil moisture trends across the TAPS plots. By providing real-time insights, this dashboard equips participants to monitor and adapt their strategies for improved productivity and sustainability.
