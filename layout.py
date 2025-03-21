# Defines the layout of the Dash app, including navbar, filters, graph, and offcanvas panel

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
        info_offcanvas
    ])
