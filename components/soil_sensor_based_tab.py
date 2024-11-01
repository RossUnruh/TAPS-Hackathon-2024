from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load team data
file_path = r"C:\Priyanka\hackthone-kansas\Water-squad-dash\dataset\Sentek_Moisture_in_cm_All_Sheets_aw.xlsx"
team_data_files = {
    "Team 3": "Team #3 Data",
    "Team 9": "Team #9 Data",
    "Team 10": "Team #10 Data",
    "Team 16": "Team #16 Data",
    "Team 17": "Team #17 Data",
    "Team 23": "Team #23 Data",
    "Team 29": "Team #29 Data",
    "Team 30": "Team #30 Data",
    "Team 32": "Team #32 Data",
    "Team 33": "Team #33 Data",
    "Team 34": "Team #34 Data"
}
team_data = {team: pd.read_excel(file_path, sheet_name=sheet_name) for team, sheet_name in team_data_files.items()}

# Define the layout for the Soil Sensor-Based Analysis tab
soil_sensor_based_tab_layout = dcc.Tab(label="Sensor-based Soil water Analysis", children=[
    html.Div([
        html.H1("Sentek Soil Moisture Sensor data"),
        
        # Dropdown to select team
        html.Label("Select Team:"),
        dcc.Dropdown(
            id='team-selector',
            options=[{'label': team, 'value': team} for team in team_data.keys()],
            value='Team 3',  # Default selection
            style={'width': '50%'}
        ),
        
        # Plots for soil moisture and plant available water
        html.Div([
            dcc.Graph(id='plant-available-water-plot'),
            dcc.Graph(id='soil-moisture-plot')

        ])
    ])
])

# Callback functions
def register_callbacks(app):
    @app.callback(
        Output('soil-moisture-plot', 'figure'),
        Input('team-selector', 'value')
    )
    def update_soil_moisture_plot(selected_team):
        data = team_data[selected_team]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data["Timestamp"], y=data["FC"], mode='lines', name='Field Capacity'))
        fig.add_trace(go.Scatter(x=data["Timestamp"], y=data["PWP"], mode='lines', name='Permanent Wilting Point'))
        fig.add_trace(go.Scatter(x=data["Timestamp"], y=data["MAD"], mode='lines', name='Management Allowable Depletion'))
        fig.add_trace(go.Scatter(x=data["Timestamp"], y=data["soil_moisture_mm"], mode='lines', name='Current Soil Moisture'))

        fig.update_layout(
            title=f"Soil Moisture Levels for {selected_team}",
            xaxis_title="Date",
            yaxis_title="Soil Moisture (mm)",
            xaxis=dict(tickformat="%Y-%m-%d"),
            template="plotly_white"
        )
        return fig

    @app.callback(
        Output('plant-available-water-plot', 'figure'),
        Input('team-selector', 'value')
    )
    def update_plant_available_water_plot(selected_team):
        data = team_data[selected_team]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data["Timestamp"], y=data["AW"], mode='lines', name='Plant Available Water'))

        fig.update_layout(
            title=f"Plant Available Water for {selected_team}",
            xaxis_title="Date",
            yaxis_title="Plant Available Soil Moisture (mm)",
            xaxis=dict(tickformat="%Y-%m-%d"),
            template="plotly_white"
        )
        return fig