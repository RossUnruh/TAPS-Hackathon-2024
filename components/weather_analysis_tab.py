from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import os

# Define the conversion factor from inches to millimeters
inches_to_mm = 25.4

# Folder path containing Excel files for weather-based data analysis
folder_path = r'C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\weather-based-data'

# Get list of teams and their file paths
team_files = {
    file_name.split("_")[0]: os.path.join(folder_path, file_name)
    for file_name in os.listdir(folder_path)
    if file_name.endswith("_budget.xlsx")
}

# Layout for the Weather Analysis Tab
weather_analysis_tab_layout = dcc.Tab(label="Weather-based Soil Water Analysis", children=[
    html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
        html.H1("KANSCHED (Weather)-based Soil Water Analysis", style={'text-align': 'center', 'font-weight': 'bold'}),

        html.H2("Daily Volumetric Water Content", style={'font-weight': 'bold', 'padding-top': '20px'}),
        html.Div([
            # Team 1 Section
            html.Div([
                html.Label("Select Team 1:"),
                dcc.Dropdown(
                    id='weather-team1-selector',
                    options=[{'label': f"Team {team}", 'value': team} for team in team_files.keys()],
                    value='1',  # Default to Team 1
                    placeholder="Select a team",
                    style={'width': '70%', 'display': 'inline-block'}
                ),
                dcc.Graph(id='weather-soil-water-plot-team1')
            ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-right': '1%'}),

            # Team 2 Section
            html.Div([
                html.Label("Select Team 2:"),
                dcc.Dropdown(
                    id='weather-team2-selector',
                    options=[{'label': f"Team {team}", 'value': team} for team in team_files.keys()],
                    value='2',  # Default to Team 2
                    placeholder="Select a team",
                    style={'width': '70%', 'display': 'inline-block'}
                ),
                dcc.Graph(id='weather-soil-water-plot-team2')
            ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-left': '1%'})
        ], style={'display': 'flex', 'justify-content': 'space-around'}),

        html.H2("SW Management Chart", style={'font-weight': 'bold', 'padding-top': '20px'}),
        html.Div([
            # Team 1 SW Management Chart
            html.Div([
                dcc.Graph(id='weather-sw-management-chart-team1')
            ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-right': '1%'}),

            # Team 2 SW Management Chart
            html.Div([
                dcc.Graph(id='weather-sw-management-chart-team2')
            ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top', 'padding-left': '1%'})
        ], style={'display': 'flex', 'justify-content': 'space-around'})
    ])
])

# Helper function to create Soil Water plot for a selected team
def create_soil_water_plot(team_number):
    file_path = team_files.get(team_number)
    if file_path is None:
        return go.Figure()  # Return empty figure if no file found

    # Read data from the Excel file
    df = pd.read_excel(file_path, sheet_name="Sheet2", skiprows=16)
    
    # Extract x_data (Date) and y_data (Soil Water Data)
    x_data = df.iloc[:, 14].dropna()  # Column 'O' (Date)
    y_data = df.iloc[:, 21].dropna()  # Column 'V' (Soil Water Data)

    # Ensure x_data and y_data have the same length
    min_length = min(len(x_data), len(y_data))
    x_data = x_data[:min_length]
    y_data = y_data[:min_length]

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        line=dict(color='blue'),
        name=f"Team {team_number}"
    ))
    fig.update_layout(
        title=f"Team {team_number} - KANSCHED (Weather) Based Soil Available Water",
        xaxis_title="Date",
        yaxis_title="Volumetric Soil Water Content",
        xaxis_tickformat="%Y-%m-%d"
    )
    return fig

# Helper function to create SW Management Chart for a selected team
def create_sw_management_chart(team_number):
    file_path = team_files.get(team_number)
    if file_path is None:
        return go.Figure()  # Return empty figure if no file found

    # Read data from the Excel file
    df = pd.read_excel(file_path, sheet_name="Sheet2", header=16)

    # Extract and convert data to mm
    dates = df.iloc[:, 14].dropna()  # Column 'O' (Date)
    sw_fc = df.iloc[:, 16].dropna() * inches_to_mm  # Column 'Q' - SW Storage @ FC
    sw_mad = df.iloc[:, 19].dropna() * inches_to_mm  # Column 'T' - SW Storage @ MAD
    sw_pwp = df.iloc[:, 17].dropna() * inches_to_mm  # Column 'R' - SW Storage @ PWP
    sw_avail = df.iloc[:, 20].dropna() * inches_to_mm  # Column 'U' - Available Soil Water

    # Create the Plotly figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=sw_fc, mode='lines', line=dict(color='brown'), name="SW Storage @ FC"))
    fig.add_trace(go.Scatter(x=dates, y=sw_mad, mode='lines', line=dict(color='red', dash='dash'), name="SW Storage @ MAD"))
    fig.add_trace(go.Scatter(x=dates, y=sw_pwp, mode='lines', line=dict(color='orange', dash='dot'), name="SW Storage @ PWP"))
    fig.add_trace(go.Scatter(x=dates, y=sw_avail, mode='lines+markers', line=dict(color='blue'), name="Available Soil Water"))

    fig.update_layout(
        title=f"SW Management Chart for Team {team_number} (Weather-based)",
        xaxis_title="Date",
        yaxis_title="Water Content (mm)",
        legend_title="Parameters"
    )
    return fig


# Register Callbacks for Weather Analysis Tab
def register_weather_analysis_callbacks(app):
    @app.callback(
        [Output('weather-soil-water-plot-team1', 'figure'), Output('weather-sw-management-chart-team1', 'figure')],
        Input('weather-team1-selector', 'value')
    )
    def update_team1_weather_plots(selected_team):
        return create_soil_water_plot(selected_team), create_sw_management_chart(selected_team)

    @app.callback(
        [Output('weather-soil-water-plot-team2', 'figure'), Output('weather-sw-management-chart-team2', 'figure')],
        Input('weather-team2-selector', 'value')
    )
    def update_team2_weather_plots(selected_team):
        return create_soil_water_plot(selected_team), create_sw_management_chart(selected_team)

