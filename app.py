import dash
import re
import dash_html_components as html
import dash_core_components as dcc
import gunicorn

import dash_bootstrap_components as dbc
from Scripts import Random_restaurant

from dash.dependencies import Input,Output,State

app = dash.Dash(__name__)

server = app.server

dropdown = dcc.Dropdown(id="Open_or_not", options=[{"label":"Only Open Restaurants","value":"True"},{"label":"Also closed restaurants","value":"False"}], value = "False")
text_input = html.Div([dbc.Input(id="input",placeholder="Choose your city!",type="text",debounce=True,autoFocus =True,value="Leuven")])





app.layout = dbc.Container([html.Div(children = [html.H1(children = "Random Restaurants"),
html.H2(children = "Using the data from Deliveroo")], style = {'textAlign':'center', 'color':'blue'}),
    html.Hr(),
    dbc.Row([dbc.Col(dropdown,md=2),dbc.Col(html.Div(children = [html.P(id="Go_here",children = "The restaurant is...")]),md=10)]),
    dbc.Row([dbc.Col(text_input,md=10),html.Button(id="submit",type="submit",children="Again!",n_clicks=1)])
    ],fluid=True)


@app.callback(
    Output("input","value"),
    [Input("submit","n_clicks"),Input("input","value")]
)
def FireUpTest(nclick,inps):
    inps = re.findall("[^()]*",inps)
    return str(inps[0]) + "(" + str(nclick) + ")" 
    

@app.callback(
    Output("Go_here","children"),
    [
        Input("input","value"),
        Input("Open_or_not","value")
    ],
)
def what_restaurant(input_city,is_open):
    return Random_restaurant(input_city,is_open)



if __name__ == '__main__':
    app.run_server(debug=True)



#Creating an input group
