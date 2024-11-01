from dash import dcc, html
from components.management_tab import management_tab_layout
from components.environment_analysis_tab import environment_analysis_tab_layout
from components.overview_tab import overview_tab_layout
from components.neutron_analysis_tab import neutron_analysis_tab_layout
from components.ndvi_based_vwc_analysis_tab import ndvi_based_vwc_analysis_tab_layout
from components.weather_analysis_tab import weather_analysis_tab_layout  # New import
from components.spatial_analysis_tab import spatial_analysis_tab_layout  
from components.soil_sensor_based_tab import soil_sensor_based_tab_layout


# Combine all tabs into a single layout
layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.Div(style={'text-align': 'center', 'margin-bottom': '20px'}, children=[
        html.Img(src='/assets/kstatelogo.PNG', style={'height': '80px'}),
        html.H1("K-State Hackathon 2024 - Water Intelligence Dashboard for Sustainable Agriculture"),
        html.P("Contributors:[Ross Unruh, Raghav Joshi, Nishadini Widanagamage, Priyanka Gautam]", style={'font-size': '18px'}),
        html.A("Github Link", 
               href="https://github.com/RossUnruh/TAPS-Hackathon-2024",
               style={'font-size': '18px', 'color': '#007bff', 'text-decoration': 'none'}),
    ]),
    dcc.Tabs([
        overview_tab_layout,
        management_tab_layout,
        environment_analysis_tab_layout, 
        spatial_analysis_tab_layout,
        soil_sensor_based_tab_layout,
        ndvi_based_vwc_analysis_tab_layout,
        weather_analysis_tab_layout, 
        neutron_analysis_tab_layout,
    ])
])

