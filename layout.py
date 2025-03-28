# Defines the layout of the Dash app, including navbar, filters, graph, and explanatory content

from dash import html, dcc
import dash_bootstrap_components as dbc
from data import all_sheets, min_year, max_year
from graph_utils import build_figure

# Get options for specialty dropdown
specialty_options = [{'label': name, 'value': name} for name in all_sheets.keys()]
specialty_default = list(all_sheets.keys())[0]

# Initial figure to load
initial_fig = build_figure(all_sheets[specialty_default])

# Navbar at the top of the app
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("FDA AI Devices Predicate Networks", className="mx-auto fs-2 fw-bold")
    ], fluid=True),
    color="primary",
    dark=True,
    className="mb-4"
)

# Offcanvas for displaying device info on node click
info_offcanvas = dbc.Offcanvas(
    id='info-offcanvas',
    title="Device Details",
    is_open=False,
    placement='end',
    children=[html.Div(id='info-content')],
    scrollable=True
)

def create_layout(app):
    return dbc.Container(fluid=True, children=[
        navbar,

        # Dropdowns and filters row
        dbc.Row([
            dbc.Col([
                html.Label("Select Specialty:", className="fw-bold"),
                dcc.Dropdown(
                    id='specialty-dropdown',
                    options=specialty_options,
                    value=specialty_default,
                    clearable=False,
                    style={"backgroundColor": "white", "color": "black"}
                )
            ], width=3),

            dbc.Col([
                html.Label("Filter by FDA Pathway:", className="fw-bold"),
                dcc.Dropdown(
                    id='fda_filter',
                    options=[
                        {'label': 'All', 'value': 'all'},
                        {'label': '510(k)', 'value': '510(k)'},
                        {'label': 'De Novo', 'value': 'De Novo'},
                        {'label': 'Premarket', 'value': 'Premarket'}
                    ],
                    value='all',
                    clearable=False,
                    style={"backgroundColor": "white", "color": "black"}
                )
            ], width=3),

            dbc.Col([
                html.Label("Filter by Approval Year:", className="fw-bold"),
                dcc.RangeSlider(
                    id='year_slider',
                    min=min_year,
                    max=max_year,
                    value=[min_year, max_year],
                    marks={y: str(y) for y in range(min_year, max_year+1, 2)},
                    step=1,
                    allowCross=False
                )
            ], width=6),
        ], className="mb-3"),

        # Search and clear highlight row
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Input(
                        id='device-search',
                        type='text',
                        placeholder='Search device ID, e.g. K123456',
                        className="me-2",
                        style={"width": "25%"},
                        n_submit=0
                    ),
                    html.Button(
                        'Search',
                        id='search-button',
                        n_clicks=0,
                        className="btn btn-success me-2"
                    ),
                    html.Button(
                        'Clear Highlight',
                        id='clear-button',
                        n_clicks=0,
                        className="btn btn-secondary"
                    ),
                ], className="d-flex justify-content-center align-items-center"),
                width=12
            )
        ], className="mb-3"),

        # Graph row
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='predicate-network-graph',
                    figure=initial_fig,
                    style={"height": "70vh"}
                )
            ], width=12)
        ]),

        # Offcanvas info panel
        info_offcanvas,

        # Explanation section
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P([
                        "This graph visualizes predicate relationships among ",
                        html.A("FDA-approved AI-ML-Enabled Medical Devices",
                               href="https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-and-machine-learning-aiml-enabled-medical-devices",
                               target="_blank",
                               style={"color": "#4ea8de", "textDecoration": "underline"}),
                        ". The FDA database is periodically updated, with the last update in December 2024."
                    ], style={"color": "#f8f9fa", "fontSize": "1.05rem"}),

                    html.P("The FDA uses three main regulatory pathways to approve AI-enabled medical devices:",
                           style={"color": "#f8f9fa", "fontSize": "1.05rem"}),

                    html.Ol([
                        html.Li("Premarket Approval (PMA) – rigorous review for high-risk devices, requires clinical evidence"),
                        html.Li("De Novo Classification - for first-of-a-kind, low/moderate-risk devices without a predicate"),
                        html.Li("Premarket Clearance or 510(k) – the most common, based on substantial equivalence to a previously approved device, termed the predicate")
                    ], style={"color": "#f8f9fa", "fontSize": "1.05rem"}),

                    html.P(
                        "Devices can be filtered by specialty, pathway used, and year of approval. A device can also be searched to isolate its predicate network. Devices can be hovered over in the graph to reveal details including a short summary, its predicate, an assigned risk of predicate creep, and a link to the official clearance summary.",
                        style={"color": "#f8f9fa", "fontSize": "1.05rem", "marginTop": "20px"}
                    ),

                    html.P(
                        "We aim to regularly update these graphs with more specialties, features and up to date devices.",
                        style={"color": "#f8f9fa", "fontSize": "1.05rem", "marginTop": "20px"}
                    ),

                    html.P("Hover over the terms below for definitions:",
                           style={"color": "#adb5bd", "fontStyle": "italic", "fontSize": "0.9rem",
                                  "marginTop": "30px"}),

                    html.Div([
                        html.Span("Predicate Device", id="tooltip-predicate-device",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Predicate Network", id="tooltip-predicate-network",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Graph Lines", id="tooltip-predicate-lines",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Vertical Axis", id="tooltip-vertical-axis",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Horizontal Axis", id="tooltip-horizontal-axis",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Submission Number", id="tooltip-submission-number",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Primary Product Code", id="tooltip-primary-product-code",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                        html.Span("Predicate Creep Risk", id="tooltip-predicate-creep-risk",
                                  style={"color": "#66c2ff", "cursor": "pointer", "fontWeight": "500"},
                                  className="mx-3"),
                    ], className="mb-5"),

                    dbc.Tooltip(
                        "A previously approved device used to support a new submission's safety and effectiveness.",
                        target="tooltip-predicate-device", placement="top"),
                    dbc.Tooltip("A visual map of how devices are connected by their predicate approvals.",
                                target="tooltip-predicate-network", placement="top"),
                    dbc.Tooltip(
                        "Visual links between a device and its primary predicate. If multiple devices have a common predicate, this is represented by both vertical and horizontal lines to the predicate.",
                        target="tooltip-predicate-lines", placement="top"),
                    dbc.Tooltip("Shows approval year — earlier devices appear lower.",
                                target="tooltip-vertical-axis", placement="top"),
                    dbc.Tooltip("Groups devices by numeric 'families' based on shared lineage.",
                                target="tooltip-horizontal-axis", placement="top"),
                    dbc.Tooltip("A unique FDA ID for each device application.",
                                target="tooltip-submission-number", placement="top"),
                    dbc.Tooltip("FDA-assigned classification indicating use and technology.",
                                target="tooltip-primary-product-code", placement="top"),
                    dbc.Tooltip("Clinician-assessed risk of innovation drift from original predicate.",
                                target="tooltip-predicate-creep-risk", placement="top")
                ], style={"padding": "25px", "borderRadius": "8px", "marginTop": "20px", "margin-bottom": "0px"})
            ]),
        ]),

        # Footer
        dbc.Row([
            dbc.Col([
                html.Footer("© 2025 amg-ai-labs",
                            style={
                                "textAlign": "center",
                                "backgroundColor": "white",
                                "color": "black",
                                "padding": "40px 0",
                                "marginTop": "20px",
                                "borderTop": "1px solid #dee2e6"
                            })
            ])
        ])
    ])
