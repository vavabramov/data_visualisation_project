import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px

path = 'data/processed_data_final.csv'
most_common = ['Transport accident', 'Flood', 'Storm', 'Epidemic',
       'Industrial accident', 'Miscellaneous accident', 'Earthquake',
       'Landslide', 'Extreme temperature', 'Drought', 'Wildfire']

disaster_group = ['ALL', 'Natural', 'Technological']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

my_font = 'Helvetica'

df = pd.read_csv(path)

country_options = [
    dict(label= country, value=country)
    for country in ['ALL'] + sorted(list(df['Country'].unique()))]

disaster_group_options = [
    dict(label=dis, value=dis)
    for dis in disaster_group]

disaster_type_options = [
    dict(label= country, value=country)
    for country in ['ALL'] + sorted(list(df['Disaster Type'].unique()))]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=country_options,
        value='ALL',
        multi=False,
        style={
            'font-family' : my_font
        }
    )

dropdown_disaster_group = dcc.Dropdown(
        id='disaster_group_drop',
        options=disaster_group_options,
        value='ALL',
        multi=False,
        style={
            'font-family' : my_font
        }
    )

dropdown_disaster_type = dcc.Dropdown(
        id='disaster_type_drop',
        options=disaster_type_options,
        value=['ALL'],
        multi=True,
        style={
            'font-family' : my_font
        }
    )

year_slider = dcc.RangeSlider(
        id='year_slider',
        min=1993,
        max=2023,
        value=[1993, 2023],
        marks={'1993': '1993',
               '': '1995',
               '1997': '1997',
               '': '1999',
               '2001': '2001',
               '': '2003',
               '2005': '2005',
               '': '2007',
               '2009': '2009',
               '': '2011',
               '2013': '2013',
               '': '2015',
               '2017': '2017',
               '': '2019',
               '2021': '2021',
               '': '2023'},
        step=1
    )


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        children='Data Visualisation Project',
        style={'textAlign': 'left'}
    ),
    
    html.Div(className="Disclaimer", 
                children=[
                    html.P(
                    children=[html.Br(),
                              'This visualization comes from our interest in understanding different kind of disaster', html.Br(),
                              'that happen around the world during the last 30 years. For us it is important to' , html.Br(),
                              'understand the evolution of the number of disasters, the different type of disasters' , html.Br(),
                              'that exists and the consequences related to reconstructions costs, deaths, etc.'],
                    style={
                        'font-family' : my_font,
                        'font-size' : '10px',
                        'margin-left': '10px',
                        'margin-top': '40px',
                        'color' : 'white'}), 
                ],
             style={
                 'margin-left': '20px',
                 'background-color':'#1C4E80',
                 'width' : '400px',
                 'height' : '70px',
                 'border-radius':'10px', 
        }
    ),
    
    html.H3(
        children='Select parameters',
        style={
            'textAlign': 'left',
            'font-family' : my_font,
            'margin-top': '30px'
        }
    ),

    html.Div(className='Dropdown Labels', children=[
        html.Div([
            html.Label(['Country'], 
                    style={'font-weight': 'bold',
                            "text-align": "left",
                            "offset":1,
                            'font-family' : my_font,
                            "margin-left": "20px"}),
        ], style=dict(width='10%')),

        html.Div([
            html.Label(['Disaster Group'],
                    style={'font-weight':'bold',
                            "text-align":"left",
                            'font-family':my_font,
                            "margin-left": "40px"}),
        ], style=dict(width='10%')),

        html.Div([
            html.Label(['Disaster Type'],
                    style={'font-weight':'bold',
                            "text-align":"left",
                            'font-family':my_font,
                            "margin-left": "60px"}),
        ], style=dict(width='40%')),

        html.Div([
            html.Label(['Years'],
                    style={'font-weight':'bold',
                            "text-align":"left",
                            'font-family':my_font,
                            "margin-left": "80px"}),
        ], style=dict(width='30%')),

    ],style=dict(display='flex',
                 justifyContent='left')),

    html.Div(className="Selections", 
             children=[
            html.Div(className='Country', 
                     children=[dropdown_country], 
                     style={"width": "10%", "margin-left": "20px"}),
                 
            html.Div(className='Disaster Group', 
                     children=[dropdown_disaster_group], 
                     style={"width": "10%", "margin-left": "20px"}),

            html.Div(className='Disaster Type',
                     children=[dropdown_disaster_type],
                     style={"width": "40%", "margin-left": "20px"}),

            html.Div(className='Year selector',
                     children=[year_slider],
                     style={"width": "30%", "margin-left": "20px"})
        ],
             style={"display": 'flex'}),

    html.Br(),
    html.H3(
        children='Number of Disasters',
        style={
            'textAlign': 'left',
            'font-family' : my_font
        }
    ),

    html.P(
        children='''These plots show the frequency of the events at country 
        and year level. Below it is exposed the frequency per type of disaster.''',
        style={
            'textAlign': 'left',
            'font-family' : my_font
        }
    ),

    html.Div(className="Selections", children=[
        dcc.Graph(id='update_bar_0', style={"margin-left": "20px", 'border-radius':'15px', 'background-color':'white'}),
        dcc.Graph(id='map_figure', style={"margin-left": "10px", 'border-radius':'15px', 'background-color':'white'})],
             style = {"display" : "flex"}),

    html.Br(),
    
    html.Div(
        dcc.Graph(
            id='bar_1_figure',
            style={"margin-left": "20px",
                   "margin-right": "50px",
                   'border-radius':'15px', 
                   'background-color':'white',
                   })
    ),
    html.Br(),
    html.Br(),
    html.H3(
        children='Number of Deaths',
        style={
            'textAlign': 'left',
            'font-family' : my_font
        }
    ),

    html.P(
        children='''
        One of the effects of a disaster correspond to the total number of 
        deaths. The pie chart shows the proportion for each disaster group, 
        and the barplot, the proportion for each type.''',
        
        style={
            'textAlign': 'left',
            'font-family' : my_font
        }
    ),    
    html.Br(),  
    html.Div(className="Number of Deaths Charts", children=[
        dcc.Graph(id='pie_figure', style={"margin-left": "20px",
                                          'border-radius':'15px',
                                          'background-color':'white'}),
        
        dcc.Graph(id='bar_2_figure', style={"margin-left": "10px",
                                            'border-radius':'15px',
                                            'background-color':'white'})],
             style=dict(display='flex')),
    html.Br(),
    html.Br(),
    html.H3(
        children='Damages & Reconstruction',
        style={
            'textAlign': 'left',
            'font-family' : my_font
        }
    ),

    html.P(
        children='''
        A yearly comparison between the damages caused by the disaster versus
        the Reconstruction Costs to compensate the damages. It is possible to
        see the details at continent and country level.''',
        style={
            'textAlign': 'left',
            'font-family' : my_font
        }
    ),
    html.Br(),
    dcc.Graph(id='bar_3_figure', style={"margin-left": "20px",
                                        "margin-right": "50px",
                                        'border-radius':'15px',
                                        'background-color':'white'}),
    html.Br(),
    html.Footer(className="Footer", 
                children=[
                    html.P(children= [html.Br(), 
                                      'Made with ❤ by Diego Torres (20221648) and Vladislav Abramov (20220729)'],
                           style={"margin-left": "20px",
                                  'textAlign': 'left',
                                  'font-family' : my_font,
                                  'color': 'white'}),
                    
                    html.A(href="https://public.emdat.be/", children= 'Data source',
                           style={"margin-left": "20px",
                                  'textAlign': 'left',
                                  'font-family' : my_font,
                                  'color': '#EA6A47'})],
                
               style = {'margin-left': '20px',
                        'margin-right': '50px',
                        'background-color' : '#1C4E80',
                        'height' : '80px'})
])

def filters(data, country, disaster_gr, disaster_types, years):
    cdf = data.copy()
    if country!='ALL':
        cdf = cdf[cdf['Country'] == country].copy()

    if disaster_gr!='ALL':
        cdf = cdf[cdf['Disaster Group'] == disaster_gr]

    if (len(disaster_types) != 1) or ('ALL' not in disaster_types):
        cdf = cdf[cdf['Disaster Type'].isin(disaster_types)]
    cdf = cdf[(cdf['Year']>=years[0]) & (cdf['Year']<=years[1])]
    return cdf

@app.callback(
    Output('update_bar_0', 'figure'),
    [Input('country_drop', 'value'),
     Input('disaster_group_drop', 'value'),
     Input('disaster_type_drop', 'value'),
     Input('year_slider', 'value')
    ]
)
def update_bar_0(country, disaster_gr, disaster_types, years):
    lin_colors = {'Natural' : "#1C4E80",
                  'Technological' : "#A5D8DD"}
    def make_line(dis_type):
        subframe = counts[counts['Disaster Group']==dis_type]
        fig.add_trace(
            go.Scatter(x=subframe['Year'],
                       y=subframe['Dis No'],
                       name=f"{dis_type} Disasters count",
                       mode="lines",
                       marker_color = lin_colors[dis_type]),
            secondary_y=True
        )

    cdf = filters(df, country, disaster_gr, disaster_types, years)

    a = cdf[['Year', 'Disaster Group', 'Total Deaths', 'Dis No']]
    deaths = a.groupby(by = ['Year']).sum().reset_index()
    counts = a.groupby(by = ['Year', 'Disaster Group'])['Dis No'].count().reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if disaster_gr=='ALL':
        make_line('Natural')
        make_line('Technological')
    elif disaster_gr=='Natural':
        make_line('Natural')
    else:
        make_line('Technological')

    fig.add_trace(
        go.Bar(x=deaths['Year'],
               y=deaths['Total Deaths'],
               name="Deaths",
               marker_color = "#EA6A47"),
        secondary_y=False
    )

    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Deaths Count", secondary_y=False, gridcolor='#F1F1F1')
    fig.update_yaxes(title_text="Disasters Count", secondary_y=True)
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=470, 
        width=850, 
        title_text="Number of disaster vs Deaths",
        font_color="#7E909A",
        title_font_color="#202020",
        legend_title_font_color="#7E909A")
    return fig

@app.callback(
    Output('map_figure', 'figure'),
    [Input('country_drop', 'value'),
     Input('disaster_group_drop', 'value'),
     Input('disaster_type_drop', 'value'),
     Input('year_slider', 'value')
    ]
)
def update_map(country, disaster_gr, disaster_types, years):
    cdf = filters(df, country, disaster_gr, disaster_types, years)
    countries = cdf[['ISO', 'Dis No']].groupby(by = ['ISO']).count().reset_index()
    countries['N of Disasters'] = countries['Dis No'].copy()
    countries['Dis No'] = np.log(countries['Dis No'])
    countries.rename(columns = {'Dis No' : 'Log (N of Disasters)'}, inplace = True)
    fig = px.choropleth(countries, 
                        locations="ISO",
                        color = "Log (N of Disasters)",
                        labels = 'N of Disasters',
                        title = "Number of disaster per country",
                        color_continuous_scale='Peach')
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500, 
        width=750, 
        title_text="Number of disaster per country",
        font_color="#7E909A",
        title_font_color="#202020",
        legend_title_font_color="#7E909A")
    return fig


@app.callback(
    Output('bar_1_figure', 'figure'),
    [Input('country_drop', 'value'),
     Input('disaster_group_drop', 'value'),
     Input('disaster_type_drop', 'value'),
     Input('year_slider', 'value')
    ]
)
def update_bar_1(country, disaster_gr, disaster_types, years):
    cdf = filters(df, country, disaster_gr, disaster_types, years)
    dis_types = cdf[['Disaster Type', 'Dis No']]
    dis_types = dis_types.groupby(by = 'Disaster Type').count()
    dis_types.sort_values(by = ['Dis No'], inplace = True)
    dis_types.rename(columns = {'Dis No' : 'Count'}, inplace = True)

    fig = go.Figure([go.Bar(x=dis_types['Count'],
                            y=dis_types.index,
                            orientation='h',
                            marker={'color': '#1C4E80'})])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_text="Type of disaster",
        font_color="#7E909A",
        title_font_color="#202020",
        legend_title_font_color="#7E909A")
    
    fig.update_xaxes(gridcolor='#F1F1F1')
    return fig

@app.callback(
    Output('pie_figure', 'figure'),
    [Input('country_drop', 'value'),
     Input('disaster_group_drop', 'value'),
     Input('disaster_type_drop', 'value'),
     Input('year_slider', 'value')
    ]
)
def update_pie_chart(country, disaster_gr, disaster_types, years):
    colors = [
              '#A5D8DD', '#0091D5',
              '#EA6A47', '#1C4E80',
              '#7E909A', '#202020']
    
    cdf = filters(df, country, disaster_gr, disaster_types, years)
    cdf = cdf[~cdf['Disaster Subgroup'].isin(['Complex Disasters', 'Extra-terrestrial'])]
    deaths = cdf[['Disaster Subgroup', 'Total Deaths']].groupby(by = 'Disaster Subgroup').sum()
    affected = cdf[['Disaster Subgroup', 'No Affected']].groupby(by = 'Disaster Subgroup').sum()
    labels = deaths.index
    
    fig = make_subplots(rows=1,
                        cols=2, 
                        specs=[[{'type':'domain'},
                                {'type':'domain'}]])

    fig.add_trace(go.Pie(labels=labels, 
                         values=deaths['Total Deaths'],
                         name="Total Deaths", 
                         marker_colors=colors, 
                         textinfo='label+percent'), 1, 1)
    
    fig.add_trace(go.Pie(labels=labels, 
                         values=affected['No Affected'], 
                         name="Total Affected", 
                         marker_colors=colors, 
                         textinfo='label+percent'), 1, 2)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500, 
        width=800,
        title_text="Ratios of Victims & Affected people",
        annotations=[dict(text='Deaths', x=0.20, y=0.5, font_size=10, showarrow=False),
                     dict(text='Affected', x=0.81, y=0.5, font_size=10, showarrow=False)],
        font_color="#7E909A",
        title_font_color="#7E909A",
        legend_title_font_color="#7E909A"
    )

    return fig

@app.callback(
    Output('bar_2_figure', 'figure'),
    [Input('country_drop', 'value'),
     Input('disaster_group_drop', 'value'),
     Input('disaster_type_drop', 'value'),
     Input('year_slider', 'value')
    ]
)

def update_bar_2(country, disaster_gr, disaster_types, years):
    cdf = filters(df, country, disaster_gr, disaster_types, years)
    deaths = cdf[['Disaster Type', 'Total Deaths']].groupby(by = 'Disaster Type').sum()
    deaths.sort_values(by = 'Total Deaths', inplace = True)
    deaths = deaths[deaths['Total Deaths'] > 0]
    fig = go.Figure([go.Bar(x=deaths['Total Deaths'],
                            y=deaths.index, 
                            orientation='h',
                            marker={'color': '#1C4E80'})])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500, 
        width=800,
        title_text="Deaths per Disaster Type",
        font_color="#7E909A",
        title_font_color="#202020",
        legend_title_font_color="#7E909A")

    fig.update_xaxes(gridcolor='#F1F1F1')
    return fig

@app.callback(
    Output('bar_3_figure', 'figure'),
    [Input('country_drop', 'value'),
     Input('disaster_group_drop', 'value'),
     Input('disaster_type_drop', 'value'),
     Input('year_slider', 'value')
    ]
)
def update_bar_3(country, disaster_gr, disaster_types, years):
    cdf = filters(df, country, disaster_gr, disaster_types, years)
    costs = cdf[['Year', 'Reconstruction Costs, Adjusted (\'000 US$)', 'Total Damages, Adjusted (\'000 US$)']]
    gdps = cdf[['Year', 'GDP_per_capita']]
    gdps = gdps.groupby(by = ['Year']).mean()
    costs = costs.groupby(by = ['Year']).sum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=gdps.index, 
                y=gdps['GDP_per_capita'], 
                name=f"GDP per capita", 
                mode="lines",
                marker_color = "#0091D5"
                ),
        secondary_y=True)

    fig.add_trace(
        go.Bar(name='Reconstruction',
               x=costs.index,
               y=costs['Reconstruction Costs, Adjusted (\'000 US$)'],
               marker_color = '#1C4E80'),
        secondary_y=False)
        
    fig.add_trace(
        go.Bar(name='Damage',
               x=costs.index,
               y=costs['Total Damages, Adjusted (\'000 US$)'],
               marker_color = '#EA6A47'),
        secondary_y=False)

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='group',
        title_text="Damage & Reconstruction costs",
        font_color="#7E909A",
        title_font_color="#202020",
        legend_title_font_color="#7E909A")
    
    fig.update_yaxes(title_text="Costs", secondary_y=False, gridcolor='#F1F1F1')
    fig.update_yaxes(title_text="GDP per Capita", secondary_y=True)
    return fig

if __name__ == '__main__':
    app.run_server("0.0.0.0", 10000, debug=False)
    