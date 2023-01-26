#!/usr/bin/env python
# coding: utf-8

import os
import plotly.offline as py     
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


# In[5]:


#https://dash.plotly.com/dash-core-components/rangeslider

#https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Dash_Interactive_Graphs/Scatter_mapbox/recycling.py

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__) #, external_stylesheets=external_stylesheets

# Use the following function when accessing the value of 'my-range-slider'
# in callbacks to transform the output value to logarithmic

#def transform_value(value):
#    return 10 ** value

blackbold={'color':'black', 'font-weight': 'bold'}


# Connect to database
engine = create_engine('mysql+py'+os.environ['MYSQL_URL'])
all2_21_rev = pd.read_sql('all2_21_rev', engine)

app.layout = html.Div([
                html.Div([
                    html.Div([
            # Map-legend
            html.Ul([
                html.Li("agriculture", className='circle', style={'background': '#ff00ff','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("minerals", className='circle', style={'background': '#0000ff','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                html.Li("power", className='circle', style={'background': '#FF0000','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("buildings", className='circle', style={'background': '#00ff00','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("waste",  className='circle', style={'background': '#824100','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("manufacturing", className='circle', style={'background': '#00bfff','color':'black',
                    'list-style':'none','text-indent': '17px'}),    
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),

            # Borough_checklist
            html.Label(children=['sector: '] , style=blackbold),
            dcc.Checklist(id='sector_name',
                    options=[{'label':str(b),'value':b} for b in sorted(all2_21_rev['sector'].unique())],
                    value=[b for b in sorted(all2_21_rev['sector'].unique())],
            ),

            # Recycling_type_checklist
            html.Label(children=['Gas: '] , style=blackbold),
            dcc.Checklist(id='gas_type',
                    options=[{'label':str(b),'value':b} for b in sorted(all2_21_rev['gas'].unique())],
                    value=[b for b in sorted(all2_21_rev['gas'].unique())],
            ),

        ],
        
        ),
    html.Div([
            dcc.Graph(id='graph')
    ]),
    
    html.Div([
        dcc.RangeSlider(
        id='non-linear-range-slider',
        marks={i: '{}'.format(10 ** i) for i in range(10)},
        min=0,
        max=9,
        value=[0,9],
        dots=False,
        #step=1000,
        #updatemode='drag'
        ),
     ], className='nine columns'
        ),

    ], className='row'
    ),

], className='ten columns offset-by-one'
)


@app.callback(
    Output('graph', 'figure'),
    [Input('non-linear-range-slider', 'value'),
    Input('sector_name','value'),
    Input('gas_type', 'value')])

def update_output(value, chosen_sector, chosen_gas):
	all2_sub1=all2_21_rev[(all2_21_rev['log10_emissions_quantity']>=value[0])&(all2_21_rev['log10_emissions_quantity']<=value[1])] #could be result of sql query and the result is what's required
	all2_sub=all2_sub1[(all2_sub1['sector'].isin(chosen_sector)) & (all2_sub1['gas'].isin(chosen_gas))]
    #when run sql query only pull the columns that you need for the app code below
    # Create figure
	locations=[go.Scattermapbox(
                    lon = all2_sub['Lat'],
                    lat = all2_sub['Long'],
                    mode='markers',
        #https://github.com/plotly/plotly.py/issues/2485
                    marker =go.scattermapbox.Marker(
		            size=4,
		            color = all2_sub['color'],
		            #colorscale='rainbow',
		            opacity=0.5,
		            showscale=True,), #I don't know why this doesn't work... 
                    #unselected={'marker' : {'opacity':1}},
                    #selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=all2_sub[['asset_name','emissions_quantity']],
                    #customdata=all2_sub['website']
    )]

    #Return figure:
	return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            #clickmode= 'event+select',
            #hovermode='closest',
            #hoverdistance=2,
            title=dict(text="Carbon Emissions Sites Across the Globe, 2021",font=dict(size=50, color='black')),
            mapbox=dict(
                accesstoken=os.environ['mapbox_access_token'],
                #bearing=25,
                style='light',
                center=dict(
                    lat=40.80105,
                    lon=-73.945155
                ),
                pitch=40,
                zoom=1
            ),
        )
    }


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)







