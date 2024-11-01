from dash import dcc, html
from dash.dependencies import Input, Output

# Define the layout for the Overview Tab
overview_tab_layout = dcc.Tab(label="Overview", children=[
    html.Div([
        html.H1("Kansas State University TAPS Dashboard Overview"),
        
        html.P("This dashboard provides data analysis and visualizations from Kansas State University TAPS (Testing Ag Performance Solutions) Project—an interactive farm management competition with 34 participating teams. The purpose of this dashboard is to support farmers and competitors by highlighting trends and insights from their plots, guiding more effective and sustainable management decisions."),
        
        html.H2("Dashboard Overview"),
        html.P("The dashboard is organized into six primary tabs, each focusing on different aspects of data analysis:"),
        
        # List of tabs with links to each one
        html.Ul([
            html.Li(dcc.Link("1. TAPS Management", href='#management-tab')),
            html.Li(dcc.Link("2. Environmental Parameters", href='#environment-analysis-tab')),
            html.Li(dcc.Link("3. Spatial Analysis", href='#spatial-analysis-tab')),
            html.Li(dcc.Link("4. Soil Moisture Sensor-based SW Management", href='#soil-sensor-based-tab')),
            html.Li(dcc.Link("5. Weather-based SW Management", href='#weather-analysis-tab')),
            html.Li(dcc.Link("6. Satellite-based SW Management", href='#ndvi-based-vwc-tab'))
        ]),
        
        html.H2("Tab Descriptions"),
        
        # Detailed descriptions for each tab
        html.H3("1. TAPS Management"),
        html.P("The TAPS Management tab uses data from the 'management' folder in the datasets directory to display key management decisions for each team. Information provided includes:"),
        html.Ul([
            html.Li("Planting Dates"),
            html.Li("Seeding Rates"),
            html.Li("Nitrogen Fertilizer Applications"),
            html.Li("Irrigation Events")
        ]),
        html.P("These management details are displayed in team-specific plots, allowing participants to visualize and evaluate resource usage and decision-making strategies."),
        
        html.H3("2. Environmental Parameters"),
        html.P("This tab incorporates Kansas Mesonet data from the Colby station to track weather trends during the 2024 corn-growing season, providing insights into:"),
        html.Ul([
            html.Li("Temperature"),
            html.Li("Precipitation"),
            html.Li("Relative Humidity"),
            html.Li("Evapotranspiration")
        ]),
        html.P("Monitoring these environmental parameters helps teams understand weather impacts on their plots and adjust their management practices accordingly."),
        
        html.H3("3. Spatial Analysis"),
        html.P("The spatial analysis tab creates soil textural prediction surface maps by using interpolation methods of Kriging and Inverse Distance Weighted (IDW). This section includes:"),
        html.Ul([
            html.Li("NDVI Maps for observing vegetation health and growth"),
            html.Li("Soil Texture Prediction Maps using Kriging and IDW interpolation methods")
        ]),
        
        html.H3("4. Soil Moisture Sensor-based SW Management"),
        html.P("This tab presents soil moisture data from Sentek soil moisture sensors, calculating daily soil moisture storage within a 90 cm soil profile. The visualizations allow users to track moisture variation based on sensor readings and assess available water levels over time."),
        
        html.H3("5. Weather-based SW Management"),
        html.P("This tab leverages basic weather data from the Colby Mesonet station to calculate reference evaporation (ET₀) using the FAO 56 Penman-Monteith equation. The model combines irrigation events, rainfall, and other data to estimate daily soil water availability and visualize volumetric water content."),
        
        html.H3("6. Satellite-based SW Management"),
        html.P("The NDVI-based soil moisture tab provides spatial maps developed from Planet Labs satellite imagery using ArcPy. This includes:"),
        html.Ul([
            html.Li("NDVI Maps"),
            html.Li("Crop coefficients to guide crop water usage decisions")
        ]),
        
        html.H3("7. Neutron Probe Soil Moisture Data"),
        html.P("This additional tab displays soil moisture variation by plot, based on data from neutron probes. This information allows competitors to compare moisture levels within the soil profile, gaining insights into the efficiency of irrigation and soil retention strategies."),
        
        html.H2("Conclusion"),
        html.P("In conclusion, the KState Hackathon 2024 - Water Intelligence Dashboard for Sustainable Agriculture offers a comprehensive view of management, environmental, and soil moisture trends across the TAPS plots. By providing real-time insights, this dashboard equips participants to monitor and adapt their strategies for improved productivity and sustainability."),
    ], style={'padding': '20px'})
])
