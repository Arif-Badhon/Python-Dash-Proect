from dash import dash, dcc, html
from database import user_collection, economic_collection, \
    business_collection, industry_collection
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np


economic_indicator = sorted(economic_collection['Indicator'].unique())
economic_last_update = economic_collection['Last Updated'][0]

business_sector = sorted(business_collection['Sector'].unique())
business_last_updated = business_collection['Last Updated'][0]

industry_name = sorted(industry_collection['Sector'].unique())
industry_last_update = industry_collection['Last Updated'][0]

app = dash.Dash(__name__, title="Data Terminal")


app.layout= html.Div([
     html.Div([
        html.Img(src=app.get_asset_url('logo.jpeg'), style={'height':'15%', 'width':'15%'}, \
            className="three columns"),
        html.H4("BIZDATA DATA TERMINAL", style={'textAlign':'center'}, className="five columns"),
        html.Div([html.H4("Bangladesh's First Data Portal \
            for Economic, Business & Company Data", style={'textAlign':'right', 'font-size': 15}, \
                className="four columns")])
     ], className='row'),
     html.Br(),
     html.Br(),
     html.Div([
        html.P("Our Data Terminal is consists of 3 Dashboards which are: \
            Economic Dashboard, Business Dashboard & Industry Dashboard \
            You will get one of the most comprehensive data warehouse here", style={'font-size': 25, 'textAlign':'center'})
     ]),
     html.Br(),
     html.Br(),
     html.Div([
        html.Div([
            html.Div([
                html.H3("  Economic Dashboard", style={'font-size': 25, 'textAlign': 'left'}),
                html.H5("  Here you can select any Indicator to see the analysis"),
                html.Br(),
                html.Br(),
                dcc.Dropdown(id='Economic_Indicator', options=[{'label':i, 'value': i} for i in economic_indicator], value='Select')
            ], className = "five columns"),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Yearly', children=[dcc.Graph(id="Economic_Graph")]),
                    dcc.Tab(label='Budget Yearly', children=[dcc.Graph(id="Economic Graph1")]),
                    dcc.Tab(label='Monthly', children=[dcc.Graph(id="Economic Graph2")])
                ])
            ], className = "seven columns")
        ], className='row')
     ]),
     html.Br(),
     html.Br(),
     html.Div([
        html.Div([
            html.H3("  Business Dashboard", style={'font-size': 25, 'textAlign': 'left'}, className="five columns"),
            dcc.Graph(id="Business Graph", className="seven columns")
        ], className='row')
     ]),
     html.Br(),
     html.Br(),
     html.Div([
        html.Div([
            html.H3("  Industry Dashboard", style={'font-size': 25, 'textAlign': 'left'}, className="five columns"),
            dcc.Graph(id="Industry Graph", className="seven columns")
        ], className='row')
     ])

    ])



@app.callback(
    Output('Economic_Graph', 'figure'),
    Input('Economic_Indicator', 'value'))
def update_yearly_Economic_graph(Economic_Indicator):
    data = economic_collection[economic_collection['Indicator'] == Economic_Indicator]
    CalenderYearData = data[~data['Calendar Value'].isnull()]
    cdata = CalenderYearData[['Calendar Year', 'Calendar Value']]
    cdata = cdata.sort_values('Calendar Year')
    cdata['Calendar Year'] = cdata['Calendar Year'].map(str)
    figure = px.bar(cdata, x='Calendar Year', y='Calendar Value', text="Calendar Value")
    figure.update_layout(title={'text':Economic_Indicator,  'y':0.93,
            'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(CalenderYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(CalenderYearData['Unit'])[0]))
    for data in figure.data:
        data["width"] = 0.5
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)