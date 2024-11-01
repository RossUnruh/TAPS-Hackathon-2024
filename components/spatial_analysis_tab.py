from dash import dcc, html
from dash.dependencies import Input, Output
from pathlib import Path
import base64
from datetime import datetime

# Paths to the images folders
NDVI_IMAGE_FOLDER = Path(r'C:\Priyanka\hackthone-kansas\Water-squad-dash\dataset\NDVI images')
SOIL_IMAGE_FOLDER = Path(r'C:\Priyanka\hackthone-kansas\Water-squad-dash\dataset\soil_data_analysis')

# Load NDVI images based on dates
def load_ndvi_images():
    ndvi_images = {}
    for image_file in NDVI_IMAGE_FOLDER.glob("*.jpg"):
        try:
            date = datetime.strptime(image_file.stem, '%Y%m%d').strftime('%Y-%m-%d')
            ndvi_images[date] = image_file
        except ValueError:
            continue
    return ndvi_images

# Load soil images with predefined types
soil_images = {
    "Clay": SOIL_IMAGE_FOLDER / "Clay.jpg",
    "Organic Matter Content": SOIL_IMAGE_FOLDER / "OrganicMatterContent.jpg",
    "Sand": SOIL_IMAGE_FOLDER / "Sand.jpg",
    "Silt": SOIL_IMAGE_FOLDER / "Silt.jpg"
}

# Encode image in base64
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return f"data:image/jpg;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"

# Load NDVI images and default selections
ndvi_images = load_ndvi_images()
ndvi_available_dates = list(ndvi_images.keys())
default_ndvi_date = "2024-07-06" if "2024-07-06" in ndvi_available_dates else ndvi_available_dates[0]
default_soil_type = "Clay"

# Layout for the Spatial Analysis tab
spatial_analysis_tab_layout = dcc.Tab(label='Spatial Analysis', children=[
    html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
        html.Div(style={'text-align': 'center', 'margin-bottom': '20px'}, children=[
            html.H1("Spatial Analysis"),
            html.P("Select a date and soil type to view the NDVI and soil data analysis images side by side.",
                   style={'font-size': '18px'})
        ]),

        # Flex container for headers, dropdowns, and images
        html.Div(style={'display': 'flex', 'justify-content': 'space-evenly', 'align-items': 'flex-start'}, children=[
            # Soil-based Map
            html.Div(style={'text-align': 'center', 'width': '45%'}, children=[
                html.H2("Soil Texture Surface Prediction Map", style={'font-size': '18px', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='soil-type-selector',
                    options=[{'label': soil_type, 'value': soil_type} for soil_type in soil_images.keys()],
                    value=default_soil_type,
                    placeholder="Select soil type",
                    clearable=False,
                    style={'width': '100%', 'font-size': '16px', 'height': '40px'}
                ),
                html.Div(id='soil-image', style={'margin-top': '10px', 'text-align': 'center'})
            ]),

            # NDVI-based Map
            html.Div(style={'text-align': 'center', 'width': '45%'}, children=[
                html.H2("NDVI Map", style={'font-size': '18px', 'margin-bottom': '5px'}),
                dcc.Dropdown(
                    id='ndvi-date-selector',
                    options=[{'label': date, 'value': date} for date in ndvi_available_dates],
                    value=default_ndvi_date,
                    placeholder="Select a date",
                    clearable=False,
                    style={'width': '100%', 'font-size': '16px', 'height': '40px'}
                ),
                html.Div(id='ndvi-image', style={'margin-top': '10px', 'text-align': 'center'})
            ])
        ])
    ])
])


