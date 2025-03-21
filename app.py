# Entry file for Dash app
# This holds the Dash app setup, layout, and run_server()

from dash import Dash
import dash_bootstrap_components as dbc
from layout import create_layout
from callbacks import register_callbacks

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "FDA AI Devices Predicate Networks"

# Set the app layout using an external layout function
app.layout = create_layout(app)

# Register all Dash callbacks separately
register_callbacks(app)

# Run the Dash server when the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
