from dash import dash, dcc, html
from database import economic_collection, \
    business_collection, industry_collection
from dash.dependencies import Input, Output, State
import plotly.express as px
import numpy as np
import plotly.graph_objects as go


economic_indicator = sorted(economic_collection['Indicator'].unique())
economic_last_update = economic_collection['Last Updated'][0]

business_sector = sorted(business_collection['Sector'].unique())
business_last_updated = business_collection['Last Updated'][0]

industry_name = sorted(industry_collection['Sector'].unique())
industry_last_update = industry_collection['Last Updated'][0]


figure = {}

app = dash.Dash(__name__, title="Data Terminal", meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1, user-scalable=no, maximum-scale=2, minimum-scale=1.0"}])


app.layout= html.Div([
     html.Div([
        html.Img(src=app.get_asset_url('logo.png'), style={'height':'15%', 'width':'15%', 'float': 'left'}, \
            className="five columns"),
        html.H4("DATA TERMINAL", style={'textAlign':'right', 'float':'right'}, className="seven columns")
     ], className='row'),
    #  html.Br(),
    #  html.Br(),
     html.Div([
        html.H4("Bangladesh's First Data Portal \
            for Economic, Business & Company Data", style={'textAlign':'center', 'font-size': 25})
     ]),
     html.Br(),
     html.Br(),
     html.Div([
        html.Div([
            html.Div([
                html.H3("  Economic Dashboard", style={'font-size': 25, 'textAlign': 'left'}),
                # html.H5("  Here you can select any Indicator to see the analysis"),
                # html.Br(),
                html.Br(),
                html.H6("Select Indicator"),
                dcc.Dropdown(id='Economic_Indicator', options=[{'label':i, 'value': i} for i in economic_indicator], value='Select')
            ], className = "four columns"),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Yearly', children=[dcc.Graph(id="Economic_Graph", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})]),
                    dcc.Tab(label='Budget Yearly', children=[dcc.Graph(id="Economic_Graph1", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})]),
                    dcc.Tab(label='Monthly', children=[dcc.Graph(id="Economic_Graph2", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})])
                ])
            ], className = "eight columns")
        ], className='row')
     ]),
     html.Br(),
     html.Br(),
     html.Div([
        html.Div([
            html.Div([
                html.H3("Business Dashboard", style={'font-size': 25, 'textAlign': 'left'}),
                # html.H5("Please select all to get the graph"),
                html.Br(),
                html.H6("Select Sector"),
                dcc.Dropdown(id="Business_Sector", options=[{'label':i, "value":i} for i in business_sector], value='Select'),
                html.H6("Select Company"),
                dcc.Dropdown(id="Business_Company"),
                html.H6("Select Indicator"),
                dcc.Dropdown(id="Business_Indicator")
            ], className = "four columns"),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Yearly', children=[dcc.Graph(id="Business_Graph", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})]),
                    dcc.Tab(label='Budget Yearly', children=[dcc.Graph(id="Business_Graph1", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})]),
                    dcc.Tab(label='Monthly', children=[dcc.Graph(id="Business_Graph2", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})])
                ])
            ], className = "eight columns")
        ], className='row')
      
     ]),
     html.Br(),
     html.Br(),
     html.Div([
        html.Div([
            html.Div([
                html.H3("Industry Dashboard", style={'font-size': 25, 'textAlign': 'left'}),
                # html.H5("Please Select all to get the graph"),
                html.Br(),
                html.H5("Select Sector"),
                dcc.Dropdown(id="Industry_Sector", options=[{'label': i, 'value': i} for i in industry_name], value='Select'),
                html.H5("Select Indicator"),
                dcc.Dropdown(id="Industry_Indicator")
            ], className='four columns'),
            html.Div([
                dcc.Tabs([
                    dcc.Tab(label='Yearly', children=[dcc.Graph(id="Industry_Graph", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})]),
                    dcc.Tab(label='Budget Yearly', children=[dcc.Graph(id="Industry_Graph1", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})]),
                    dcc.Tab(label='Monthly', children=[dcc.Graph(id="Industry_Graph2", figure = {}, config={"displaylogo": False, 'modeBarButtonsToRemove':['toImage', 'pan2d', 'select2d', 'lasso2d']})])
                ])
            ], className='eight columns')
        ], className='row')
     ])

    ])



#-----------------Economic Dashboard Callback-----------------------------#
@app.callback(
    Output('Economic_Graph', 'figure'),
    Input('Economic_Indicator', 'value'))
def update_yearly_Economic_graph(Economic_Indicator):
    data = economic_collection[economic_collection['Indicator'] == Economic_Indicator]
    CalenderYearData = data[~data['Calendar Value'].isnull()]
    if CalenderYearData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig
    cdata = CalenderYearData[['Calendar Year', 'Calendar Value']]
    cdata = cdata.sort_values('Calendar Year')
    cdata['Calendar Year'] = cdata['Calendar Year'].map(int).map(str)
    figure = px.bar(cdata, x='Calendar Year', y='Calendar Value', text="Calendar Value")
    figure.update_layout(title={'text':Economic_Indicator,  'y':0.93,
            'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(CalenderYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(CalenderYearData['Unit'])[0]))
    for data in figure.data:
        data["width"] = 0.5
    return figure

@app.callback(
    Output('Economic_Graph1', 'figure'),
    Input('Economic_Indicator', 'value'))
def update_budget_yearly_graph(Economic_Indicator):
    data = economic_collection[economic_collection['Indicator'] == Economic_Indicator]
    BudgetYearData = data[~data['Budget Value'].isnull()]
    if BudgetYearData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig   
    cdata = BudgetYearData[['Budget Year', 'Budget Value']]
    cdata = cdata.sort_values('Budget Year')
    figure = px.bar(cdata, x='Budget Year', y='Budget Value', text="Budget Value")
    figure.update_layout(title={'text':Economic_Indicator,  'y':0.93,
        'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(BudgetYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(BudgetYearData['Unit'])[0]))
    for data in figure.data:
        data["width"] = 0.5
    return figure

@app.callback(
    Output('Economic_Graph2', 'figure'),
    Input('Economic_Indicator', 'value'))
def update_monthly_graph(Economic_Indicator):
    data = economic_collection[economic_collection['Indicator'] == Economic_Indicator]
    MonthlyData = data[~data['Calendar Year'].isnull() & data['Calendar Value'].isnull()]
    if MonthlyData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig
    cdata = MonthlyData[["Calendar Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
    cdata = cdata.sort_values('Calendar Year')
    cdata['Calendar Year'] = cdata['Calendar Year'].map(int).map(str)
    Year = cdata["Calendar Year"]
    January = cdata["Jan"]
    February = cdata["Feb"]
    March = cdata["Mar"]
    April = cdata["Apr"]
    May = cdata["May"]
    June = cdata["Jun"]
    July = cdata["Jul"]
    August = cdata["Aug"]
    September = cdata["Sep"]
    October = cdata["Oct"]
    November = cdata["Nov"]
    December = cdata["Dec"]

    figure = go.Figure(data=[
        go.Bar(name='January', x=Year, y=January),
        go.Bar(name='February', x=Year, y=February),
        go.Bar(name='March', x=Year, y=March),
        go.Bar(name='April', x=Year, y=April),
        go.Bar(name='May', x=Year, y=May),
        go.Bar(name='June', x=Year, y=June),
        go.Bar(name='July', x=Year, y=July),
        go.Bar(name='August', x=Year, y=August),
        go.Bar(name='September', x=Year, y=September),
        go.Bar(name='October', x=Year, y=October),
        go.Bar(name='November', x=Year, y=November),
        go.Bar(name='December', x=Year, y=December)
    ])
    figure.update_layout(barmode='group')
    figure.update_layout(title={'text':Economic_Indicator,  'y':0.93,
    'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(MonthlyData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(MonthlyData['Unit'])[0]))
    return figure

#-------------- Business Dashboard callback----------------------#
@app.callback(
    Output('Business_Company', 'options'),
    Input('Business_Sector', 'value')
)
def business_company(Business_Sector):
    data = business_collection[business_collection['Sector'] == Business_Sector]
    company = data["Company"]
    return [{'label': i, 'value': i} for i in np.unique(company)]

@app.callback(
    Output('Business_Indicator', 'options'),
    Input('Business_Sector', 'value'),
    Input('Business_Company', 'value')
)
def business_indicator(Business_Sector, Business_Company):
    data = business_collection[business_collection['Sector'] == Business_Sector]
    data = data[data['Company'] == Business_Company]
    Business_Indicator = data['Indicator']
    return [{'label': i, 'value': i} for i in np.unique(Business_Indicator)]

@app.callback(
    Output('Business_Graph', 'figure'),
    Input('Business_Sector', 'value'),
    Input('Business_Company', 'value'),
    Input('Business_Indicator', 'value')
)
def business_graph(Business_Sector, Business_Company, Business_Indicator):
    data = business_collection[business_collection['Sector'] == Business_Sector]
    data = data[data['Company'] == Business_Company]
    data = data[data['Indicator'] == Business_Indicator]

    CalenderYearData = data[~data['Calendar Value'].isnull()]
    if CalenderYearData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig
    cdata = CalenderYearData[['Year', 'Calendar Value']]
    cdata = cdata.sort_values('Year')
    cdata['Year'] = cdata['Year'].map(int).map(str)
    figure = px.bar(cdata, x='Year', y='Calendar Value', text="Calendar Value")
    figure.update_layout(title={'text':Business_Indicator + " by " + Business_Company,  'y':.93,
        'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(CalenderYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(CalenderYearData['Unit'])[0]))
    for data in figure.data:
        data["width"] = 0.5
    return figure

@app.callback(
    Output('Business_Graph1', 'figure'),
    Input('Business_Sector', 'value'),
    Input('Business_Company', 'value'),
    Input('Business_Indicator', 'value')
)
def business_graph1(Business_Sector, Business_Company, Business_Indicator):
        data = business_collection[business_collection['Sector'] == Business_Sector]
        data = data[data['Company'] == Business_Company]
        data = data[data['Indicator'] == Business_Indicator]

        BudgetYearData = data[~data['Budget Value'].isnull()]
        if BudgetYearData.empty:
            fig = go.Figure()
            fig.update_layout(
                xaxis =  { "visible": False },
                yaxis = { "visible": False },
                annotations = [
                    {   
                        "text": "Please select the relevant Timeline",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 17
                        }
                    }
                ]
            )
            return fig 
        cdata = BudgetYearData[['Budget Year', 'Budget Value']]
        cdata = cdata.sort_values('Budget Year')
        figure = px.bar(cdata, x='Budget Year', y='Budget Value', text="Budget Value")
        figure.update_layout(title={'text':Business_Indicator + " by " + Business_Company,  'y':.93,
        'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(BudgetYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(BudgetYearData['Unit'])[0]))
        for data in figure.data:
            data["width"] = 0.5
        return figure

@app.callback(
    Output('Business_Graph2', 'figure'),
    Input('Business_Sector', 'value'),
    Input('Business_Company', 'value'),
    Input('Business_Indicator', 'value')
)
def business_graph2(Business_Sector, Business_Company, Business_Indicator):
    data = business_collection[business_collection['Sector'] == Business_Sector]
    data = data[data['Company'] == Business_Company]
    data = data[data['Indicator'] == Business_Indicator]
    MonthlyData = data[~data['Year'].isnull() & data['Calendar Value'].isnull()]
    if MonthlyData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig
    
    cdata = MonthlyData[["Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
    cdata = cdata.sort_values('Year')
    cdata['Year'] = cdata['Year'].map(int).map(str)
    Year = cdata["Year"]
    January = cdata["Jan"]
    February = cdata["Feb"]
    March = cdata["Mar"]
    April = cdata["Apr"]
    May = cdata["May"]
    June = cdata["Jun"]
    July = cdata["Jul"]
    August = cdata["Aug"]
    September = cdata["Sep"]
    October = cdata["Oct"]
    November = cdata["Nov"]
    December = cdata["Dec"]

    figure = go.Figure(data=[
        go.Bar(name='January', x=Year, y=January),
        go.Bar(name='February', x=Year, y=February),
        go.Bar(name='March', x=Year, y=March),
        go.Bar(name='April', x=Year, y=April),
        go.Bar(name='May', x=Year, y=May),
        go.Bar(name='June', x=Year, y=June),
        go.Bar(name='July', x=Year, y=July),
        go.Bar(name='August', x=Year, y=August),
        go.Bar(name='September', x=Year, y=September),
        go.Bar(name='October', x=Year, y=October),
        go.Bar(name='November', x=Year, y=November),
        go.Bar(name='December', x=Year, y=December)
    ])
    figure.update_layout(barmode='group')
    figure.update_layout(title={'text':Business_Indicator + " by " + Business_Company,  'y':0.93,
    'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(MonthlyData['Source'])[0]), yaxis_title=" Unit of Measurement: " + str(np.unique(MonthlyData['Unit'])[0]))
    return figure


#-----------------Industry Dashboard------------------------###

@app.callback(
    Output('Industry_Indicator', 'options'),
    Input('Industry_Sector', 'value')
)
def industry_indicator(Industry_Sector):
    data = industry_collection[industry_collection['Sector'] == Industry_Sector]
    Industry_Indicator = data['Indicator']
    return [{'label': i, 'value': i} for i in np.unique(Industry_Indicator)]

@app.callback(
    Output('Industry_Graph', 'figure'),
    Input('Industry_Sector', 'value'),
    Input('Industry_Indicator', 'value')
)
def industry_graph(Industry_Sector, Industry_Indicator):
    data = industry_collection[industry_collection['Sector'] == Industry_Sector]
    data = data[data['Indicator'] == Industry_Indicator]

    CalenderYearData = data[~data['Calendar Value'].isnull()]
    if CalenderYearData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig
    cdata = CalenderYearData[['Calendar Year', 'Calendar Value']]
    cdata = cdata.sort_values('Calendar Year')
    cdata['Calendar Year'] = cdata['Calendar Year'].map(int).map(str)
    figure = px.bar(cdata, x='Calendar Year', y='Calendar Value', text="Calendar Value")
    figure.update_layout(title={'text':Industry_Indicator,  'y':0.93,
                'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(CalenderYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(CalenderYearData['Unit'])[0]))
    for data in figure.data:
        data["width"] = 0.5
    return figure

@app.callback(
    Output('Industry_Graph1', 'figure'),
    Input('Industry_Sector', 'value'),
    Input('Industry_Indicator', 'value')
)
def industry_graph1(Industry_Sector, Industry_Indicator):
    data = industry_collection[industry_collection['Sector'] == Industry_Sector]
    data = data[data['Indicator'] == Industry_Indicator]

    BudgetYearData = data[~data['Budget Value'].isnull()]
    if BudgetYearData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig
    cdata = BudgetYearData[['Budget Year', 'Budget Value']]
    cdata = cdata.sort_values('Budget Year')
    figure = px.bar(cdata, x='Budget Year', y='Budget Value', text='Budget Value')
    figure.update_layout(title={'text':Industry_Indicator,  'y':0.93,
        'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(BudgetYearData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(BudgetYearData['Unit'])[0]))
    for data in figure.data:
        data["width"] = 0.5
    return figure

@app.callback(
    Output('Industry_Graph2', 'figure'),
    Input('Industry_Sector', 'value'),
    Input('Industry_Indicator', 'value')
)
def industry_graph2(Industry_Sector, Industry_Indicator):
    data = industry_collection[industry_collection['Sector'] == Industry_Sector]
    data = data[data['Indicator'] == Industry_Indicator]

    MonthlyData = data[~data['Calendar Year'].isnull() & data['Calendar Value'].isnull()]
    if MonthlyData.empty:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "Please select the relevant Timeline",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 17
                    }
                }
            ]
        )
        return fig

    cdata = MonthlyData[["Calendar Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
    cdata = cdata.sort_values('Calendar Year')
    cdata['Calendar Year'] = cdata['Calendar Year'].map(int).map(str)
    Year = cdata["Calendar Year"]
    January = cdata["Jan"]
    February = cdata["Feb"]
    March = cdata["Mar"]
    April = cdata["Apr"]
    May = cdata["May"]
    June = cdata["Jun"]
    July = cdata["Jul"]
    August = cdata["Aug"]
    September = cdata["Sep"]
    October = cdata["Oct"]
    November = cdata["Nov"]
    December = cdata["Dec"]

    figure = go.Figure(data=[
        go.Bar(name='January', x=Year, y=January),
        go.Bar(name='February', x=Year, y=February),
        go.Bar(name='March', x=Year, y=March),
        go.Bar(name='April', x=Year, y=April),
        go.Bar(name='May', x=Year, y=May),
        go.Bar(name='June', x=Year, y=June),
        go.Bar(name='July', x=Year, y=July),
        go.Bar(name='August', x=Year, y=August),
        go.Bar(name='September', x=Year, y=September),
        go.Bar(name='October', x=Year, y=October),
        go.Bar(name='November', x=Year, y=November),
        go.Bar(name='December', x=Year, y=December)
    ])
    figure.update_layout(barmode='group')
    figure.update_layout(title={'text':Industry_Indicator,  'y':0.93,
        'x':0.5,'xanchor':'center', 'yanchor':'top'}, xaxis_title="Source: " + str(np.unique(MonthlyData['Source'])[0]), yaxis_title="Unit of Measurement: " + str(np.unique(MonthlyData['Unit'])[0]))
    return figure




if __name__ == '__main__':
    app.run_server(debug=True)