from dash import Dash
from dash import dcc, html
from pathlib import Path
import base64
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from PIL import Image
from components.layout import layout  # Ensure this import is correct
from components.neutron_analysis_tab import neutron_data, depth_columns  # Import necessary data
from components.management_tab import taps_planting_data, irrigation_long, nitrogen_totals  # Import necessary data
from components.environment_analysis_tab import environment_analysis_tab_layout
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.spatial_analysis_tab import soil_images, ndvi_images, encode_image
from components.overview_tab import overview_tab_layout  # Import the overview tab

from components.weather_analysis_tab import weather_analysis_tab_layout, register_weather_analysis_callbacks
from components.soil_sensor_based_tab import soil_sensor_based_tab_layout, register_callbacks as register_soil_callbacks



from components.environment_analysis_tab import (
    update_temperature_time_series,
    update_precipitation_bar,
    update_humidity_time_series,
    update_eto_time_series
)

from components.ndvi_based_vwc_analysis_tab import create_soil_water_plot, create_sw_management_chart


# Load mesonet data with ETO included
mesonet = pd.read_excel('C:\\Priyanka\\hackthone-kansas\\Water-squad-dash\\dataset\\colby_station_kansas_mesonet_with_ETO.xlsx')
mesonet["TIMESTAMP"] = pd.to_datetime(mesonet["TIMESTAMP"])


# # Initialize the Dash app
# app = Dash(__name__)

# # Set the layout for the app
# app.layout = layout

# Initialize the app with suppress_callback_exceptions set to True
app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = layout  # Set the layout for the app

# After initializing the app
register_weather_analysis_callbacks(app)
register_soil_callbacks(app) 

# Load neutron data
neutron_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\All excel data\\24 KSU_TAPS_Neutron_Tube Readings_VWC.xlsx',
    sheet_name='Sheet1',
    skiprows=2
)
neutron_data['Date'] = pd.to_datetime(neutron_data['Date'], errors='coerce')
depth_columns = [6, 18, 30, 42, 54, 66, 78, 90, 102, 114]


# Tab 1 allbacks for interactivity for the tabs management data

# Bar plot for seeding rate by plot ID
@app.callback(
    Output('seeding-bar-plot', 'figure'),
    [Input('team-id-selector', 'value')]
)
def update_seeding_bar(selected_farms):
    filtered_data = taps_planting_data[taps_planting_data['ID'].isin(selected_farms)]
    fig = px.bar(filtered_data, x='Seeding Rate (plants/ac)', y='ID', color='Company',
                 title="Seeding Rate by Team ID with Company Labels")
    fig.update_layout(xaxis_title='Seeding Rate (plants/ac)', yaxis_title='Team ID')
    return fig

# Scatter plot for seeding rate by planting date
@app.callback(
    Output('seeding-scatter-plot', 'figure'),
    [Input('team-id-selector', 'value')]
)
def update_seeding_scatter(selected_farms):
    filtered_data = taps_planting_data[taps_planting_data['ID'].isin(selected_farms)]
    fig = px.scatter(filtered_data, x='Planting Date', y='Seeding Rate (plants/ac)', color='Company',
                     hover_data=['ID'], title="Seeding Rate vs Planting Date with Company Labels")
    return fig

# # Pie chart for total nitrogen application
# @app.callback(
#     Output('nitrogen-pie-chart', 'figure'),
#     [Input('team-id-selector', 'value')]
# )
# def update_nitrogen_pie(selected_farms):
#     filtered_nitrogen = nitrogen_totals[nitrogen_totals['ID'].isin(selected_farms)]
#     fig = px.pie(filtered_nitrogen, names='ID', values=' Total (lbs/ac)',
#                  title="Total Nitrogen Application by Team")
#     return fig

# # Line plot for irrigation over time
# @app.callback(
#     Output('irrigation-line-plot', 'figure'),
#     [Input('team-id-selector', 'value')]
# )
# def update_irrigation_line(selected_farms):
#     filtered_irrigation = irrigation_long[irrigation_long['ID'].isin(selected_farms)]
#     fig = go.Figure()
#     for farm_id, group in filtered_irrigation.groupby('ID'):
#         fig.add_trace(go.Scatter(
#             x=group['Date'], y=group['Irrigation'],
#             mode='lines+markers', name=f'Farm {farm_id}'
#         ))
#     fig.update_layout(title="Irrigation Over Time by Team", xaxis_title="Date", yaxis_title="Irrigation (inches)")
#     return fig

# # Stacked area plot for cumulative irrigation over time
# @app.callback(
#     Output('cumulative-irrigation-area', 'figure'),
#     [Input('team-id-selector', 'value')]
# )
# def update_cumulative_irrigation(selected_farms):
#     filtered_irrigation = irrigation_long[irrigation_long['ID'].isin(selected_farms)]
#     pivot_irrigation = filtered_irrigation.pivot(index='Date', columns='ID', values='Irrigation').fillna(0)
#     cumulative_irrigation = pivot_irrigation.cumsum()
#     fig = go.Figure()
#     for col in cumulative_irrigation.columns:
#         fig.add_trace(go.Scatter(
#             x=cumulative_irrigation.index, y=cumulative_irrigation[col],
#             mode='lines', stackgroup='one', name=f'Farm {col}'
#         ))
#     fig.update_layout(title="Cumulative Irrigation Over Time", xaxis_title="Date", yaxis_title="Cumulative Irrigation (inches)")
#     return fig

# # Heatmap for irrigation over time
# @app.callback(
#     Output('irrigation-heatmap', 'figure'),
#     [Input('team-id-selector', 'value')]
# )
# def update_irrigation_heatmap(selected_farms):
#     # Filter data for selected farms
#     filtered_irrigation = irrigation_long[irrigation_long['ID'].isin(selected_farms)]
#     pivot_irrigation = filtered_irrigation.pivot(index='ID', columns='Date', values='Irrigation')

#     # Create heatmap with annotations
#     fig = go.Figure(data=go.Heatmap(
#         z=pivot_irrigation.values,
#         x=pivot_irrigation.columns,
#         y=pivot_irrigation.index,
#         colorscale='YlGnBu',
#         colorbar=dict(title="Irrigation (inches)"),
#         zmin=0, zmax=pivot_irrigation.values.max()
#     ))

#     fig.update_layout(
#         title="Irrigation Application Heatmap by Date and Team ID",
#         xaxis=dict(title="Date", tickformat="%Y-%m-%d"),
#         yaxis=dict(title="Farm ID")
#     )

#     return fig


# Callbacks for plotting

@app.callback(
    Output('nitrogen-bar-chart', 'figure'),
    Input('team-id-selector', 'value')
)
def update_nitrogen_bar_chart(selected_teams):
    filtered_data = nitrogen_totals[nitrogen_totals['ID'].isin(selected_teams)]
    fig = px.bar(filtered_data, x='ID', y=' Total (lbs/ac)', title="Total Nitrogen Application by Team",
                    labels={'ID': 'Team ID', ' Total (lbs/ac)': 'Total Nitrogen (lbs/ac)'})
    fig.update_layout(xaxis_title="Team ID", yaxis_title="Total Nitrogen Applied (lbs/ac)")
    return fig

@app.callback(
    Output('irrigation-scatter-plot', 'figure'),
    Input('team-id-selector', 'value')
)
def update_irrigation_scatter_plot(selected_teams):
    filtered_data = irrigation_long[irrigation_long['ID'].isin(selected_teams)]
    fig = px.scatter(filtered_data, x='Date', y='Irrigation', color='ID', title="Irrigation Events by Date",
                        labels={'Date': 'Date', 'Irrigation': 'Irrigation (inches)'})
    fig.update_traces(mode='markers')
    fig.update_layout(xaxis_title="Date", yaxis_title="Irrigation Amount (inches)")
    return fig

@app.callback(
    Output('cumulative-irrigation-area', 'figure'),
    Input('team-id-selector', 'value')
)
def update_cumulative_irrigation_area(selected_teams):
    filtered_data = irrigation_long[irrigation_long['ID'].isin(selected_teams)]
    filtered_data['Cumulative Irrigation'] = filtered_data.groupby('ID')['Irrigation'].cumsum()

    filtered_data['Cumulative Irrigation'] = filtered_data.groupby('ID')['Irrigation'].cumsum()
    fig = px.area(filtered_data, x='Date', y='Cumulative Irrigation', color='ID',
                    title="Cumulative Irrigation Over Time by Team")
    fig.update_layout(xaxis_title="Date", yaxis_title="Cumulative Irrigation (inches)")
    return fig

@app.callback(
    Output('irrigation-heatmap', 'figure'),
    Input('team-id-selector', 'value')
)
def update_irrigation_heatmap(selected_teams):
    filtered_data = irrigation_long[irrigation_long['ID'].isin(selected_teams)]
    irrigation_pivot = filtered_data.pivot(index='ID', columns='Date', values='Irrigation')
    fig = go.Figure(data=go.Heatmap(
        z=irrigation_pivot.values,
        x=irrigation_pivot.columns,
        y=irrigation_pivot.index,
        colorscale='Blues'
    ))
    fig.update_layout(title="Irrigation Heatmap by Team and Date",
                        xaxis_title="Date", yaxis_title="Team ID")
    return fig




# tab 3: Environment 


# Register callbacks for the environment analysis tab
@app.callback(
    Output('temperature-time-series', 'figure'),
    Input('temperature-time-series', 'id')
)
def render_temperature_time_series(_):
    return update_temperature_time_series()

@app.callback(
    Output('precipitation-bar', 'figure'),
    Input('precipitation-bar', 'id')
)
def render_precipitation_bar(_):
    return update_precipitation_bar()

@app.callback(
    Output('humidity-time-series', 'figure'),
    Input('humidity-time-series', 'id')
)
def render_humidity_time_series(_):
    return update_humidity_time_series()

@app.callback(
    Output('eto-time-series', 'figure'),
    Input('eto-time-series', 'id')
)
def render_eto_time_series(_):
    return update_eto_time_series()


# tab 4 : NDVI based VWC analysis

# Callbacks for NDVI Soil Water Analysis
@app.callback(
    [Output('soil-water-plot-team1', 'figure'), Output('sw-management-chart-team1', 'figure')],
    [Input('team1-selector', 'value')]
)
def update_team1_plots(selected_team):
    return create_soil_water_plot(selected_team), create_sw_management_chart(selected_team)

@app.callback(
    [Output('soil-water-plot-team2', 'figure'), Output('sw-management-chart-team2', 'figure')],
    [Input('team2-selector', 'value')]
)
def update_team2_plots(selected_team):
    return create_soil_water_plot(selected_team), create_sw_management_chart(selected_team)


# tab 5 weahther 


# Register Callbacks
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
    
    
    
#### tab for spatial analysis


@app.callback(
    Output('soil-image', 'children'),
    Input('soil-type-selector', 'value')
)
def display_soil_image(selected_soil_type):
    if selected_soil_type and selected_soil_type in soil_images:
        encoded_image = encode_image(soil_images[selected_soil_type])
        return html.Img(src=encoded_image, style={'max-width': '100%', 'height': 'auto', 'display': 'block', 'margin': '0 auto'})
    return html.P("Soil image not available.", style={'font-size': '18px', 'color': 'red'})

@app.callback(
    Output('ndvi-image', 'children'),
    Input('ndvi-date-selector', 'value')
)
def display_ndvi_image(selected_date):
    if selected_date and selected_date in ndvi_images:
        encoded_image = encode_image(ndvi_images[selected_date])
        return html.Img(src=encoded_image, style={'max-width': '100%', 'height': 'auto', 'display': 'block', 'margin': '0 auto'})
    return html.P("NDVI image not available for the selected date.", style={'font-size': '18px', 'color': 'red'})


###tab for soil sensor based 




## Tab 5 call backs for the neutron data 


# Time Series Analysis for VWC at Different Depths
@app.callback(
    Output('time-series-graph', 'figure'),
    [Input('plot-id-dropdown', 'value'), Input('plot-selector-checklist', 'value')]
)
def update_time_series(plot_ids, selected_plots):
    if 'time_series' not in selected_plots:
        return go.Figure()  # Empty figure if not selected

    fig = go.Figure()
    for plot_id in plot_ids:
        plot_data = neutron_data[neutron_data['Plot #'] == plot_id]
        for depth in depth_columns:
            fig.add_trace(go.Scatter(x=plot_data['Date'], y=plot_data[depth], mode='lines', name=f"Plot {plot_id} - {depth} inches"))
    fig.update_layout(title="Time Series of VWC", xaxis_title="Date", yaxis_title="VWC (m3/m3)")
    return fig

# Depth Profile Analysis on Specific Dates
@app.callback(
    Output('depth-profile-graph', 'figure'),
    [Input('plot-id-dropdown', 'value'), Input('plot-selector-checklist', 'value')]
)
def update_depth_profile(plot_ids, selected_plots):
    if 'depth_profile' not in selected_plots:
        return go.Figure()  # Empty figure if not selected

    fig = go.Figure()
    for plot_id in plot_ids:
        date_data = neutron_data[neutron_data['Plot #'] == plot_id]
        date_data = date_data.melt(id_vars=['Date'], value_vars=depth_columns, var_name='Depth', value_name='VWC')
        fig.add_trace(go.Scatter(x=date_data['Depth'], y=date_data['VWC'], mode='lines+markers', name=f"Plot {plot_id}"))
    fig.update_layout(title="Depth Profile of VWC", xaxis_title="Depth (inches)", yaxis_title="VWC (m3/m3)")
    return fig

# VWC Comparison Across Depths
@app.callback(
    Output('vwc-comparison-graph', 'figure'),
    [Input('plot-id-dropdown', 'value'), Input('plot-selector-checklist', 'value')]
)
def update_vwc_comparison(plot_ids, selected_plots):
    if 'vwc_comparison' not in selected_plots:
        return go.Figure()  # Empty figure if not selected

    melted_data = neutron_data[neutron_data['Plot #'].isin(plot_ids)]
    melted_data = melted_data.melt(id_vars=['Date', 'Plot #'], value_vars=depth_columns, var_name='Depth', value_name='VWC')
    fig = px.box(melted_data, x='Depth', y='VWC', color='Plot #', title="Comparison of VWC Across Depths")
    fig.update_layout(xaxis_title="Depth (inches)", yaxis_title="VWC (m3/m3)")
    return fig

# Seasonal Trends in VWC
@app.callback(
    Output('seasonal-trend-graph', 'figure'),
    [Input('plot-id-dropdown', 'value'), Input('seasonal-trend-depth-dropdown', 'value')]
)
def update_seasonal_trend(plot_ids, depths):
    fig = go.Figure()
    for plot_id in plot_ids:
        for depth in depths:
            plot_data = neutron_data[neutron_data['Plot #'] == plot_id]
            fig.add_trace(go.Scatter(
                x=plot_data['Date'], y=plot_data[depth], mode='lines', 
                name=f"Plot {plot_id} - {depth} inches"
            ))
    fig.update_layout(
        title="Seasonal Trends in VWC", 
        xaxis_title="Date", 
        yaxis_title="Volumetric Water Content (m3/m3)",
        legend_title="Plot and Depth"
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
