from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the TAPS Management data
taps_planting_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\2024_TAPS_management.xlsx', 
    sheet_name='Planting date', 
    skiprows=1
)
taps_irrigation_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\2024_TAPS_management.xlsx', 
    sheet_name='Irrigation amounts', 
    skiprows=1
)
taps_nitrogen_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\2024_TAPS_management.xlsx', 
    sheet_name='Nitrogen fertilizer', 
    skiprows=2
)

# Reshape and aggregate irrigation data
irrigation_long = taps_irrigation_data.melt(id_vars=['ID'], var_name='Date', value_name='Irrigation')
irrigation_long['Date'] = pd.to_datetime(irrigation_long['Date'], errors='coerce').dt.date
irrigation_long = irrigation_long.groupby(['ID', 'Date']).agg({'Irrigation': 'sum'}).reset_index()

# Summarize nitrogen data
nitrogen_totals = taps_nitrogen_data.groupby('ID')[' Total (lbs/ac)'].sum().reset_index()

# Layout for the Management Tab
management_tab_layout = dcc.Tab(label="TAPS Management", children=[
    html.H1("TAPS Management Overview"),
    html.Div([
        html.Label("Select Team ID(s):"),
        dcc.Dropdown(
            id='team-id-selector',
            options=[{'label': f"Team {id}", 'value': id} for id in taps_planting_data['ID'].unique()],
            value=[1, 7, 15, 34],  # Default to Team IDs 1, 7, 15, and 34
            multi=True,  # Enable multiple selections
            placeholder="Select one or more Team IDs",
            style={'width': '50%'}
        )
    ], style={'padding': '20px'}),

    # Seeding and Nitrogen Application Graphs
    html.Div([
        dcc.Graph(id='seeding-bar-plot', style={'display': 'inline-block', 'width': '45%'}),
        dcc.Graph(id='seeding-scatter-plot', style={'display': 'inline-block', 'width': '45%'}),
    ]),

    # Nitrogen Bar Chart and Irrigation Scatter Plot
    html.Div([
        dcc.Graph(id='nitrogen-bar-chart', style={'display': 'inline-block', 'width': '45%'}),
        dcc.Graph(id='irrigation-scatter-plot', style={'display': 'inline-block', 'width': '45%'}),
    ]),

    # Cumulative Irrigation Area Plot and Heatmap
    html.Div([
        dcc.Graph(id='cumulative-irrigation-area', style={'display': 'inline-block', 'width': '45%'}),
        dcc.Graph(id='irrigation-heatmap', style={'display': 'inline-block', 'width': '45%'}),
    ])
])
