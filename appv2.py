#https://dash.plotly.com/dash-core-components/rangeslider
import os
import plotly.offline as py     
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import numpy as np
from sqlalchemy import create_engine



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Use the following function when accessing the value of 'my-range-slider'
# in callbacks to transform the output value to logarithmic

# Connect to database
engine = create_engine(os.environ['MYSQL_URL'@'MYSQLHOST':'MYSQLPORT'/'MYSQLDATABASE'])


app.layout = html.Div([

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
    ]),
    
    ])

@app.callback(
    Output('graph', 'figure'),
    Input('non-linear-range-slider', 'value'))
def update_output(value):
    all2_21_rev = pd.read_sql('all2_21_rev', engine)
    all2_sub=all2_21_rev[(all2_21_rev['log10_emissions_quantity']>=value[0])&(all2_21_rev['log10_emissions_quantity']<=value[1])] #could be result of sql query and the result is what's required
    #when run sql query only pull the columns that you need for the app code below
    # Create figure
    locations=[go.Scattermapbox(
                    lon = all2_sub['Lat'],
                    lat = all2_sub['Long'],
                    mode='markers',
                    #legendgroup = all2_sub['sector'],
                    #marker=
                    #dict(color=np.where(np.logical_and(all2_sub['sector']=='manufacturing', all2_sub['sector']=='power'), 'red', 'green')
    #),
                    #marker=dict(color = all2_sub['color']),
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

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            #clickmode= 'event+select',
            #hovermode='closest',
            #hoverdistance=2,
            title=dict(text="Carbon Emissions Sites Across the Globe, 2021",font=dict(size=50, color='green')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
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


    #'Linear Value: {}, Log Value: [{:0.2f}, {:0.2f}]'.format(
    #    str(value),
    #    transformed_value[0],
    #    transformed_value[1]
    #)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)


