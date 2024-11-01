# environment_analysis_tab.py
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go

# Load mesonet data
mesonet = pd.read_excel('C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\colby_station_kansas_mesonet_with_ETO.xlsx')
mesonet["TIMESTAMP"] = pd.to_datetime(mesonet["TIMESTAMP"])

# Calculate total precipitation
total_precip = round(mesonet["PRECIP"].sum(), 3)
daily_precip = mesonet.groupby("TIMESTAMP")["PRECIP"].sum()

# Define the layout for the Environment Analysis Tab
environment_analysis_tab_layout = dcc.Tab(label="Environment Parameters", children=[
    html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
        html.H1("Environment Parameters (Weather Data from Mesonet)"),

        # Temperature Time Series Plot
        dcc.Graph(id='temperature-time-series'),

        # Precipitation Bar Chart with total precipitation annotation
        dcc.Graph(id='precipitation-bar'),

        # Relative Humidity Time Series Plot
        dcc.Graph(id='humidity-time-series'),

        # Evapotranspiration (ETO) Time Series Plot
        dcc.Graph(id='eto-time-series')
    ])
])

# Define the callback functions here (without registering them with app directly)
def update_temperature_time_series():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mesonet["TIMESTAMP"],
        y=mesonet["TEMP2MAVG"],
        mode='lines',
        name="Mean Temperature (°C)",
        line=dict(color='firebrick')
    ))
    fig.update_layout(
        title="Daily Mean Temperature (°C)",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)"
    )
    return fig

def update_precipitation_bar():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily_precip.index,
        y=daily_precip,
        name="Daily Precipitation",
        marker_color='royalblue'
    ))
    fig.update_layout(
        title="Daily Precipitation (mm)",
        xaxis_title="Date",
        yaxis_title="Precipitation (mm)"
    )
    fig.add_annotation(
        x=daily_precip.index[-1], y=daily_precip.max(),
        text=f"Total precipitation: {total_precip} mm",
        showarrow=False, yshift=10
    )
    return fig

def update_humidity_time_series():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mesonet["TIMESTAMP"],
        y=mesonet["RELHUM2MAVG"],
        mode='lines',
        name="Relative Humidity",
        line=dict(color='darkgreen')
    ))
    fig.update_layout(
        title="Daily Mean Relative Humidity (%) ",
        xaxis_title="Date",
        yaxis_title="Relative Humidity (%)"
    )
    return fig

def update_eto_time_series():
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=mesonet["TIMESTAMP"],
        y=mesonet['ET0'],
        mode='lines',
        name="Evapotranspiration (ETO)",
        line=dict(color='purple')
    ))
    fig.update_layout(
        title="Daily Evapotranspiration (ETo) using FAO Penman-Monteith Equation (mm)",
        xaxis_title="Date",
        yaxis_title="ETO (mm)"
    )
    return fig
