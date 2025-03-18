# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=
    [html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                    'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]
            ],
        value = 'ALL',
        placeholder = "Select a Launch Site",
        searchable=True
),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(
    children=[dcc.Graph(id='success-pie-chart')],
    style={'display': 'flex', 'justifyContent': 'center'}
),

    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    marks={i: str(i) for i in range(0, 10001, 500)},
                    value=[min_payload, max_payload]
    ),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
    ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value')
)

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        all_sites_df = spacex_df[spacex_df['class'] == 1].groupby('Launch Site')['class'].sum().reset_index()
        
        fig = px.pie(all_sites_df, values='class', names='Launch Site')

    else:
        spec_site_df = spacex_df[spacex_df['Launch Site'] == entered_site]['class'].value_counts().reset_index()
        fig = px.pie(spec_site_df, values='count', names='class')

    return fig



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
              Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')]
)

def get_scatter(entered_site1, entered_payload):
    
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= entered_payload[0]) & 
        (spacex_df['Payload Mass (kg)'] <= entered_payload[1])
    ]

    
    if entered_site1 != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site1]

    # scatter plot
    fig = px.scatter(
        filtered_df, 
        x='Payload Mass (kg)', 
        y='class',
        color='Booster Version Category',
        title=f'Success vs Payload for {entered_site1}'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()