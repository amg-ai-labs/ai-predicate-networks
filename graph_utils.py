# Contains graph-building utilities for predicate network visualization

import datetime
import pandas as pd
import networkx as nx
import plotly.graph_objects as go

# Traverse predecessors/successors to get connected subgraph

def get_subgraph_nodes_bfs(G, root):
    visited = set()
    stack = [root]
    while stack:
        current = stack.pop()
        if current not in visited and current in G:
            visited.add(current)
            neighbors = list(G.predecessors(current)) + list(G.successors(current))
            stack.extend(neighbors)
    return visited

# Build the Plotly figure from a DataFrame (filtered by specialty, year, etc.)
def build_figure(df, fda_filter='all', year_range=None, highlight_node=None):
    if fda_filter != 'all':
        df = df[df['FDA'] == fda_filter]

    if year_range:
        start_year, end_year = year_range
        start_date = datetime.datetime(start_year, 1, 1)
        end_date = datetime.datetime(end_year, 12, 31)
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Build the graph
    G = nx.DiGraph()
    for _, row in df.iterrows():
        device_id = row['Submission_Number']
        G.add_node(device_id, **{
            'date': row['Date'],
            'family': row['family'],
            'fda': row['FDA'],
            'creep': row['Creep'],
            'predloc': row['Predicate_Location'],
            'device_name': row['Device_Name'],
            'device_summary': row['Device_Summary'],
            'classification': row['Classification'],
            'node_predicate': row['Predicate'],
            'company': row['Company'],
            'leadspec': row['Lead_Specialty'],
            'secondspec': row['Secondary_Specialty'],
            'shortdesc': row['Short_Description']
        })

    for _, row in df.iterrows():
        pred = row['Predicate']
        if pred and pred != "N/A" and pred in G.nodes and row['Submission_Number'] in G.nodes:
            G.add_edge(pred, row['Submission_Number'])

    pos = {}
    for node in G.nodes:
        node_row = df[df['Submission_Number'] == node]
        if not node_row.empty:
            fam = node_row['family'].iloc[0]
            dt_val = node_row['Date'].iloc[0]
            pos[node] = (fam, dt_val)

    highlight_nodes = set()
    if highlight_node and highlight_node in G:
        highlight_nodes = get_subgraph_nodes_bfs(G, highlight_node)

    # Color and symbol maps
    predicate_location_color_map = {
        'Specialty AI device': '#B0B0B0',
        'Other AI device': 'bisque',
        'Non AI device': 'firebrick',
        'No predicate': '#003366'
    }
    fda_symbol_map = {
        '510(k)': 'circle',
        'De Novo': 'triangle-up',
        'Premarket': 'cross'
    }

    def dim_color(base_color, is_hl):
        if not highlight_nodes:
            return base_color
        return base_color if is_hl else 'rgba(200,200,200,0.2)'

    # Build node trace
    node_x, node_y = [], []
    node_color, node_symbol, customdata = [], [], []

    for node in G.nodes:
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        attr = G.nodes[node]
        base_col = predicate_location_color_map.get(attr['predloc'], 'grey')
        is_highlighted = node in highlight_nodes
        final_col = dim_color(base_col, is_highlighted)

        node_symbol.append(fda_symbol_map.get(attr['fda'], 'circle'))
        node_color.append(final_col)

        customdata.append([
            node,
            attr['device_name'],
            attr['device_summary'],
            attr['classification'],
            attr['node_predicate'],
            attr['date'].strftime('%Y-%m-%d') if pd.notna(attr['date']) else '',
            attr['fda'],
            attr['creep'],
            attr['company'],
            attr['leadspec'],
            attr['secondspec'],
            attr['shortdesc']
        ])

    hovertemplate = (
        '<b>Submission Number:</b> %{customdata[0]}<br>'
        '<b>Device Name:</b> %{customdata[1]}<br>'
        '<b>Date of Final Decision:</b> %{customdata[5]}<br>'
        '<b></br>'
        'Click for more information<extra></extra>'
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        textposition="middle right",
        hovertemplate=hovertemplate,
        customdata=customdata,
        marker=dict(
            showscale=False,
            color=node_color,
            symbol=node_symbol,
            size=8,
            line=dict(width=1)
        ),
        showlegend=False
    )

    # Build edge traces
    edge_traces = []
    for src, tgt in G.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[tgt]
        tgt_loc = G.nodes[tgt]['predloc']
        base_edge_col = predicate_location_color_map.get(tgt_loc, 'black')

        if highlight_nodes and (src not in highlight_nodes or tgt not in highlight_nodes):
            edge_col = 'rgba(150,150,150,0.2)'
        else:
            edge_col = base_edge_col

        edge_traces.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=2, color=edge_col),
                hoverinfo='none',
                mode='lines',
                showlegend=False
            )
        )

    # Build legend traces for symbol and color explanations
    legend_traces = [
        # FDA pathways
        go.Scatter(x=[None], y=[None], mode='markers', name='510(k)',
                   marker=dict(symbol='circle', color='black', size=7), showlegend=True,
                   legendgroup='FDA', legendgrouptitle=dict(text='Approval Pathway')),
        go.Scatter(x=[None], y=[None], mode='markers', name='De Novo',
                   marker=dict(symbol='triangle-up', color='black', size=7), showlegend=True,
                   legendgroup='FDA'),
        go.Scatter(x=[None], y=[None], mode='markers', name='Premarket',
                   marker=dict(symbol='cross', color='black', size=7), showlegend=True,
                   legendgroup='FDA'),
        # Predicate types
        go.Scatter(x=[None], y=[None], mode='markers', name='Specialty AI device',
                   marker=dict(symbol='circle', color='#B0B0B0', size=7), showlegend=True,
                   legendgroup='Location', legendgrouptitle=dict(text='Predicate Type')),
        go.Scatter(x=[None], y=[None], mode='markers', name='Other AI device',
                   marker=dict(symbol='circle', color='bisque', size=7), showlegend=True,
                   legendgroup='Location'),
        go.Scatter(x=[None], y=[None], mode='markers', name='Non AI device',
                   marker=dict(symbol='circle', color='firebrick', size=7), showlegend=True,
                   legendgroup='Location'),
        go.Scatter(x=[None], y=[None], mode='markers', name='No predicate',
                   marker=dict(symbol='circle', color='#003366', size=7), showlegend=True,
                   legendgroup='Location')
    ]

    # Assemble figure
    fig = go.Figure(
        data=edge_traces + [node_trace] + legend_traces,
        layout=go.Layout(
            title='',
            showlegend=True,
            hovermode='closest',
            margin=dict(b=0, l=0, r=0, t=0),
            xaxis=dict(title='', showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(title='Date of Approval', showgrid=True, zeroline=False, tickformat='%Y'),
            plot_bgcolor='rgb(230,230,230)',
            paper_bgcolor='rgb(230,230,230)'
        )
    )

    fig.update_layout(
        legend=dict(x=1.02, y=0.5, xanchor='left', yanchor='middle')
    )

    return fig
