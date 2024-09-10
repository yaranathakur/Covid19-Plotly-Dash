import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Import data
patients = pd.read_csv(r"assets\IndividualDetails.csv")

# Card Values
total = patients.shape[0]
active = patients[patients["current_status"] == "Hospitalized"].shape[0]
recovered = patients[patients["current_status"] == "Recovered"].shape[0]
deaths = patients[patients["current_status"] == "Deceased"].shape[0]

# Dropdown options
options = [
    {"label": "All", "value": "All"},
    {"label": "Hospitalized", "value": "Hospitalized"},
    {"label": "Recovered", "value": "Recovered"},
    {"label": "Deceased", "value": "Deceased"},
]

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

# App layout
app.layout = dbc.Container(
    [
        html.H1(
            "Corona Virus Pandemic", style={"color": "white", "text-align": "center"}
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Total Cases", className="text-light"),
                                html.H4(total, className="text-light"),
                            ]
                        ),
                        className="bg-danger",
                    ),
                    md=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Active Cases", className="text-light"),
                                html.H4(active, className="text-light"),
                            ]
                        ),
                        className="bg-info",
                    ),
                    md=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Recovered", className="text-light"),
                                html.H4(recovered, className="text-light"),
                            ]
                        ),
                        className="bg-warning",
                    ),
                    md=3,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Deaths", className="text-light"),
                                html.H4(deaths, className="text-light"),
                            ]
                        ),
                        className="bg-success",
                    ),
                    md=3,
                ),
            ],
            className="mb-4",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dcc.Dropdown(id="picker", options=options, value="All"),
                            dcc.Graph(id="bar"),
                        ]
                    )
                ),
                md=12,
            ),
        ),
    ],
    fluid=True,
)


# Callback to update the graph based on dropdown selection
@app.callback(Output("bar", "figure"), [Input("picker", "value")])
def update_graph(selected_status):
    if selected_status == "All":
        patients_bar = patients["detected_state"].value_counts().reset_index()
    else:
        npat = patients[patients["current_status"] == selected_status]
        patients_bar = npat["detected_state"].value_counts().reset_index()

    # Ensure the DataFrame has the correct column names
    patients_bar.columns = ["detected_state", "count"]

    # Create the bar chart
    figure = {
        "data": [go.Bar(x=patients_bar["detected_state"], y=patients_bar["count"])],
        "layout": go.Layout(title="State Total Count"),
    }
    return figure


# Run the app
if __name__ == "__main__":
    app.run_server()
