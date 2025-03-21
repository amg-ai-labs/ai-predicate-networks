# Contains Dash callback functions for interactivity

from dash import Input, Output, State, callback_context, no_update, html
from data import all_sheets
from graph_utils import build_figure

# Register all Dash app callbacks
def register_callbacks(app):

    @app.callback(
        Output('predicate-network-graph', 'figure'),
        [
            Input('specialty-dropdown', 'value'),
            Input('fda_filter', 'value'),
            Input('year_slider', 'value'),
            Input('search-button', 'n_clicks'),
            Input('device-search', 'n_submit'),
            Input('clear-button', 'n_clicks')
        ],
        State('device-search', 'value')
    )
    def update_figure(specialty, fda_value, year_range,
                      search_clicks, enter_presses, clear_clicks,
                      device_id):
        df = all_sheets[specialty]
        ctx = callback_context
        if not ctx.triggered:
            return no_update

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'clear-button':
            return build_figure(df, fda_filter=fda_value, year_range=year_range, highlight_node=None)

        elif triggered_id in ('search-button', 'device-search'):
            if device_id and device_id in df['Submission_Number'].values:
                return build_figure(df, fda_filter=fda_value, year_range=year_range, highlight_node=device_id)
            else:
                return build_figure(df, fda_filter=fda_value, year_range=year_range, highlight_node=None)

        return build_figure(df, fda_filter=fda_value, year_range=year_range, highlight_node=None)

    @app.callback(
        Output('info-offcanvas', 'is_open'),
        Output('info-content', 'children'),
        Input('predicate-network-graph', 'clickData'),
        [State('info-offcanvas', 'is_open'), State('specialty-dropdown', 'value')]
    )
    def show_device_info_on_click(clickData, is_open, specialty):
        if not clickData:
            return False, no_update

        points = clickData['points']
        if not points:
            return False, no_update

        cdata = points[0]['customdata']
        device_id = cdata[0]
        device_name = cdata[1]
        device_summary = cdata[2]
        classification = cdata[3]
        node_pred = cdata[4]
        date_val = cdata[5]
        fda_val = cdata[6]
        creep_val = cdata[7]
        company_val = cdata[8]
        leadspec_val = cdata[9]
        sec_spec_val = cdata[10]
        short_desc_val = cdata[11]

        summary_link = html.A("Link to Summary", href=device_summary, target="_blank") \
            if device_summary else "No summary link."

        content = [
            html.P(f"Submission Number: {device_id}"),
            html.P(f"Device Name: {device_name}"),
            html.P(f"Date of Final Decision: {date_val}"),
            html.P(f"Company: {company_val}"),
            html.P(f"Short Description: {short_desc_val}"),
            html.P(f"Primary Product Code: {classification}"),
            html.P(f"FDA Designated Panel (lead): {leadspec_val}"),
            html.P(f"Specialty or Subspecialty: {sec_spec_val}"),
            html.P(f"FDA Pathway: {fda_val}"),
            html.P(f"Predicate: {node_pred if node_pred else 'None'}"),
            html.P(f"Potential Predicate Creep Risk: {creep_val}"),
            summary_link
        ]

        return True, content
