# neutron_analysis_tab.py

from dash import dcc, html
import pandas as pd

# Load neutron data
neutron_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\All excel data\\24 KSU_TAPS_Neutron_Tube Readings_VWC.xlsx',
    sheet_name='Sheet1',
    skiprows=2
)
neutron_data['Date'] = pd.to_datetime(neutron_data['Date'], errors='coerce')
depth_columns = [6, 18, 30, 42, 54, 66, 78, 90, 102, 114]

# Layout for the Neutron Analysis Tab
neutron_analysis_tab_layout = dcc.Tab(label='Neutron Probe Data Analysis', children=[
    html.Div([
        html.H2("Neutron Data Analysis"),

        # Dropdown to select multiple Plot IDs
        html.Label("Select Plot IDs for Analysis:"),
        dcc.Dropdown(
            id='plot-id-dropdown',
            options=[{'label': f"Plot {plot}", 'value': plot} for plot in neutron_data['Plot #'].unique()],
            value=[neutron_data['Plot #'].unique()[0]],  # Default to first plot
            multi=True,
            style={'width': '50%', 'display': 'inline-block'}
        ),

        # Checklist to select plots to display
        html.Label("Select Plots to Display:"),
        dcc.Checklist(
            id='plot-selector-checklist',
            options=[
                {'label': 'Time Series Analysis', 'value': 'time_series'},
                {'label': 'Depth Profile Analysis', 'value': 'depth_profile'},
                {'label': 'VWC Comparison Across Depths', 'value': 'vwc_comparison'},
                {'label': 'Seasonal Trends', 'value': 'seasonal_trend'}
            ],
            value=['time_series', 'depth_profile', 'vwc_comparison'],  # Default selected plots
            inline=True,
            style={'margin': '20px 0'}
        ),

        # First row of graphs (Time Series, Depth Profile, VWC Comparison)
        html.Div([
            dcc.Graph(id='time-series-graph', style={'display': 'inline-block', 'width': '33%'}),
            dcc.Graph(id='depth-profile-graph', style={'display': 'inline-block', 'width': '33%'}),
            dcc.Graph(id='vwc-comparison-graph', style={'display': 'inline-block', 'width': '33%'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-around', 'margin-top': '20px'}),

        # Dropdown for selecting depth for Seasonal Trends
        html.Label("Select Depths for Seasonal Trend Analysis:"),
        dcc.Dropdown(
            id='seasonal-trend-depth-dropdown',
            options=[{'label': f"{depth} inches", 'value': depth} for depth in depth_columns],
            value=[depth_columns[0]],  # Default to first depth
            multi=True,
            style={'width': '50%', 'display': 'inline-block'}
        ),

        # Seasonal Trends Graph (separate row)
        html.H3("Seasonal Trends in VWC"),
        dcc.Graph(id='seasonal-trend-graph', style={'width': '100%'})
    ])
])
