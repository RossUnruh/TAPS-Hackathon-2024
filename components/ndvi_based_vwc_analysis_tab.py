# components/ndvi_based_vwc_analysis_tab.py
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import os

# Folder containing Excel files for NDVI-based VWC analysis
input_folder = r'C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\NDVI-data'
inches_to_mm = 25.4

# Get list of teams and their file paths
team_files = {
    file_name.split('_')[1].split('.')[0]: os.path.join(input_folder, file_name)
    for file_name in os.listdir(input_folder)
    if file_name.startswith("KANSCHED_") and file_name.endswith(".xlsx")
}

# Layout for the NDVI-based VWC analysis tab
ndvi_based_vwc_analysis_tab_layout = dcc.Tab(label="Satellite-based Soil Water Analysis", children=[
    html.H1("NDVI-based Soil Water Analysis", style={'text-align': 'center', 'font-weight': 'bold'}),
    
    html.H2("Daily Volumetric Water Content", style={'font-weight': 'bold', 'padding-top': '20px'}),
    html.Div([
        # Team 1 Section
        html.Div([
            html.Label("Select Team :"),
            dcc.Dropdown(
                id='team1-selector',
                options=[{'label': f"Team {team}", 'value': team} for team in team_files.keys()],
                value='1',  # Default to Team 1
                placeholder="Select a team",
                style={'width': '70%', 'display': 'inline-block'}
            ),
            dcc.Graph(id='soil-water-plot-team1')
        ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-right': '1%'}),

        # Team 2 Section
        html.Div([
            html.Label("Select Team :"),
            dcc.Dropdown(
                id='team2-selector',
                options=[{'label': f"Team {team}", 'value': team} for team in team_files.keys()],
                value='2',  # Default to Team 2
                placeholder="Select a team",
                style={'width': '70%', 'display': 'inline-block'}
            ),
            dcc.Graph(id='soil-water-plot-team2')
        ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-left': '1%'})
    ], style={'display': 'flex', 'justify-content': 'space-around'}),
    
    html.H2("SW Management Chart", style={'font-weight': 'bold', 'padding-top': '20px'}),
    html.Div([
        # Team 1 SW Management Chart
        html.Div([
            dcc.Graph(id='sw-management-chart-team1')
        ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-right': '1%'}),

        # Team 2 SW Management Chart
        html.Div([
            dcc.Graph(id='sw-management-chart-team2')
        ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-left': '1%'})
    ], style={'display': 'flex', 'justify-content': 'space-around'})
])

# Helper functions for generating plots
def create_soil_water_plot(team_number):
    file_path = team_files.get(team_number)
    if file_path is None:
        return go.Figure()
    
    df = pd.read_excel(file_path, sheet_name="Budget_", skiprows=16)
    x_data = df.iloc[:, 14].dropna()
    y_data = df.iloc[:, 21].dropna()

    min_length = min(len(x_data), len(y_data))
    x_data, y_data = x_data[:min_length], y_data[:min_length]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers', line=dict(color='blue')))
    fig.update_layout(
        title=f"Team {team_number} - Soil Available Water using NDVI-based Approach",
        xaxis_title="Date",
        yaxis_title="Volumetric Soil Water Content ",
        xaxis_title_font=dict(size=14, color='darkorange', family='Arial Black'),
        yaxis_title_font=dict(size=14, color='black', family='Arial Black')
    )
    return fig

def create_sw_management_chart(team_number):
    file_path = team_files.get(team_number)
    if file_path is None:
        return go.Figure()
    
    df = pd.read_excel(file_path, sheet_name="Budget_", header=16)
    dates = df.iloc[:, 14].dropna()
    sw_fc = df.iloc[:, 16].dropna() * inches_to_mm
    sw_mad = df.iloc[:, 19].dropna() * inches_to_mm
    sw_pwp = df.iloc[:, 17].dropna() * inches_to_mm
    sw_avail = df.iloc[:, 20].dropna() * inches_to_mm

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=sw_fc, mode='lines', name="SW Storage @ FC", line=dict(color='brown')))
    fig.add_trace(go.Scatter(x=dates, y=sw_mad, mode='lines', name="SW Storage @ MAD", line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=dates, y=sw_pwp, mode='lines', name="SW Storage @ PWP", line=dict(color='orange', dash='dot')))
    fig.add_trace(go.Scatter(x=dates, y=sw_avail, mode='lines', name="Available Soil Water", line=dict(color='blue')))
    fig.update_layout(
        title=f"SW Management Chart for Team {team_number}",
        xaxis_title="Date",
        yaxis_title="Water Content (mm)",
        xaxis_title_font=dict(size=14, color='darkorange', family='Arial Black'),
        yaxis_title_font=dict(size=14, color='darkgreen', family='Arial Black')
    )
    return fig
