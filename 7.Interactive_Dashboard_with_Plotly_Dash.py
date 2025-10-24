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
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'All Sites'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                ],
                                                value='All Sites',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'All Sites':
        fig = px.pie(data_frame=spacex_df[spacex_df["class"] == 1], 
        names="Launch Site", 
        title='Total Success Launches by Site')
    else:
        fig = px.pie(data_frame=spacex_df[spacex_df["Launch Site"] == entered_site], 
        names="class", 
        title='Total Success Launches by Site')
    
    return fig

# TASK 4:
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site, payload_mass):
    if entered_site == 'All Sites':
        fig = px.scatter(data_frame=spacex_df[spacex_df["Payload Mass (kg)"].between(payload_mass[0], payload_mass[1])], 
        title='Correlation between Payload and Success for all Sites',
        color="Booster Version Category",
        x="Payload Mass (kg)",
        y="class")
    else:
        selected_site = spacex_df[spacex_df['Launch Site']==str(entered_site)]
        fig = px.scatter(data_frame=selected_site[selected_site["Payload Mass (kg)"].between(payload_mass[0], payload_mass[1])], 
        title='Correlation between Payload and Success for all Sites',
        color="Booster Version Category",
        x="Payload Mass (kg)",
        y="class")

    return fig


# Run the app
if __name__ == '__main__':
    app.run()
