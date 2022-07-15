from dash import dash, dcc, html
from database import user_collection, economic_collection, \
    business_collection, industry_collection
from dash.dependencies import Input, Output, State


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
     html.Div([
        html.Div([
            html.H3("Economic Dashboard", style={'font-size': 30, 'textAlign': 'left'}, className="six columns")
        ])
     ])

    ])



if __name__ == '__main__':
    app.run_server(debug=True)