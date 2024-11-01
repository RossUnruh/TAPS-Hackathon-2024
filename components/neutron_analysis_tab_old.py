from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the neutron data, skipping first two rows to get actual headers
neutron_data = pd.read_excel(
    'C:\\Priyanka\\hackthone-kansas\\Water-squad\\All excel data\\24 KSU_TAPS_Neutron_Tube Readings_VWC.xlsx',
    sheet_name='Sheet1',
    skiprows=2  # Adjust this if needed
)
neutron_data['Date'] = pd.to_datetime(neutron_data['Date'])  # Ensure Date is in datetime format

# Identify columns with depth information
# Adjust column selection based on actual column names containing 'inches'
depth_columns = [col for col in neutron_data.columns if isinstance(col, str) and 'inches' in col.lower()]

# Layout for Neutron Data Analysis Tab
neutron_analysis_tab_layout = dcc.Tab(label='Neutron Probe Data Analysis', children=[
    html.Div([
        html.H2("Neutron Probe Data Analysis"),

        # Dropdown for selecting plot
        html.Label("Select Plot:"),
        dcc.Dropdown(
            id='plot-selector',
            options=[{'label': f"Plot {plot}", 'value': plot} for plot in neutron_data['Plot #'].unique()],
            value=neutron_data['Plot #'].iloc[0],
            style={'width': '30%', 'display': 'inline-block'}
        ),

        # Date picker for selecting date
        html.Label("Select Date:"),
        dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=neutron_data['Date'].min(),
            max_date_allowed=neutron_data['Date'].max(),
            date=neutron_data['Date'].iloc[0],
            style={'display': 'inline-block', 'margin-left': '20px'}
        ),

        # Depth dropdown for seasonal trends
        html.Label("Select Depth for Seasonal Trends:"),
        dcc.Dropdown(
            id='depth-selector',
            options=[{'label': f"{depth} inches", 'value': depth} for depth in depth_columns],
            value=depth_columns[0] if depth_columns else None,
            style={'width': '30%', 'display': 'inline-block', 'margin-left': '20px'}
        ),

        # Graphs for Neutron Data
        html.Div([
            dcc.Graph(id='seasonal-trend-graph', style={'display': 'inline-block', 'width': '32%'}),
            dcc.Graph(id='depth-profile-graph', style={'display': 'inline-block', 'width': '32%'}),
            dcc.Graph(id='time-series-graph', style={'display': 'inline-block', 'width': '32%'})
        ])
    ], style={'margin-top': '20px'})
])

# Remember to define callbacks in `app.py` instead of importing `app` here to avoid circular import errors.
