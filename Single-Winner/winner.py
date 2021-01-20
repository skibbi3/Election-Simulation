import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import SingleWinner
import pandas as pd
import numpy as np
import plotly.express as px


voter_number = 100
candidate_number = 5

voters = np.random.normal(0,1,(voter_number,2)).round(3).tolist()
candidate_coords = np.random.normal(0,1,(candidate_number,2)).round(3).tolist()
candidate_names = list(map(chr, range(65, 65+len(candidate_coords))))

candidates = {candidate_names[i]: candidate_coords[i] for i in range(len(candidate_names))}

df = pd.DataFrame(SingleWinner.alternative_vote(voters, candidates))

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])



app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)