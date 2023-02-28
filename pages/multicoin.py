###############################################################################
# MultiCoin Dashboard - App Page with Plotly, Dash
###############################################################################

import dash
from dash import Dash, html, dcc, dash_table, Input, Output, State, callback, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# local
from data_master import*
import fig_format
import fig_plot


##############################################################################
# INITIALIZE DASH PAGE
##############################################################################
# dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.css"
# # app = Dash(__name__,external_stylesheets=[dbc.themes.SLATE, dbc_css],use_pages=True)
# load_figure_template('SLATE')

dash.register_page(
    __name__,
    path='/multicoin',
    title='Lumida - Multicoin',
)

##############################################################################
# SET UP - REQUIRED VARIABLES
##############################################################################
# Main coin list (make this selectable in Dash!)
coin_list = list(coin_price.columns)

# for buttons
trailing_dropdown = ['1d', '7d', '14d', '30d', '60d', '90d', '180d', '360d']

# Recession dates
# recession_2020_dates = dict(x0='2020-01-01', x1='2020-07-01',line_width=0, fillcolor="red", opacity=0.2)

# crypto_2018_crash_dates = dict(x0='2017-11-01', x1='2018-12-31',line_width=0, fillcolor="gray", opacity=0.2)

# blank figure for initial load - temporary workaround
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)', )
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig
##############################################################################
# DBC Components
##############################################################################

_FIXED = {
    "position": "fixed",
    "top":  '11em',
    "left": '1em',
    "bottom": 0,
    'font-size':'15px'

}

datepicker_range = dbc.Row(
    [
        dbc.Label("Date Range:"),
        dcc.DatePickerRange(
            min_date_allowed=coins_dict['btc'].time.iloc[0],
            max_date_allowed=coins_dict['btc'].time.iloc[-1],
            initial_visible_month=coins_dict['btc'].time.iloc[-61],
            start_date=coins_dict['btc'].time.iloc[0],
            end_date=coins_dict['btc'].time.iloc[-1],
            number_of_months_shown=1,
            id="date-picker-range",
        ),
    ],
)

dropdown_trailing = dbc.Row(
    [
        dbc.Label("Apply Trailing Days:"),
        dcc.Dropdown(
            trailing_dropdown,
            trailing_dropdown[0],
            clearable=False,
            maxHeight=400,
            id="trailing",

        ),
    ],
    className='mt-4'
)


dropdown_coins = html.Div(
    [
        dbc.Label("Search Coins:"),
        dcc.Dropdown(
            coin_list,
            ['btc','eth','ada'],
            placeholder="Select coins",
            maxHeight=500,
            multi=True,
            id="coins",
        ),
    ],
    className='mt-4'

)


# needs more work
# options_checklist = dbc.Row(
#     [
#         dbc.Label("Show following:"),
#         dcc.Checklist(
#             ['Recessions', 'Crypto Crashes'],
#             [],
#             id='checklist',
#         ),
#     ],
#     className='mt-4'

# )

table_of_contents = dbc.Row(
    [
        dbc.Label("Jump To Chart:", className='lead'),
        dbc.Nav(
            [
                dbc.NavLink("Price", href="#graph-1a",  external_link=True, active="exact"),
                dbc.NavLink("LogPrice", href="#graph-2a", external_link=True, active="exact"),
                dbc.NavLink("Returns", href="#graph-3a", external_link=True, active="exact"),
                dbc.NavLink("Volatility", href="#graph-4a", external_link=True, active="exact"),
                dbc.NavLink("DrawDowns", href="#graph-5a", external_link=True, active="exact"),
                dbc.NavLink("Correlations", href="#graph-6a", external_link=True, active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className='mt-4'
)

sidebar = dbc.Col(
    [
        datepicker_range,
        dropdown_trailing,
        dropdown_coins,
        table_of_contents,
        # options_checklist,
    ],
    style=_FIXED,
    width=1,
)
###############################################################################
# DASH APP LAYOUT
###############################################################################
layout = dbc.Container(
    [
        dbc.Col(
            [
                sidebar,
            ],
            className='d-none d-lg-block',
            width=1,
            # style=_FIXED,
        ),
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Price (USD)',className='mt-4'),
                                dcc.Graph(
                                    id='graph-1a',
                                    figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 m-4',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Log Price (USD)',className='mt-4'),
                                dcc.Graph(
                                    id='graph-2a',
                                    figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 m-4',
                        ),
                    ],
                    # className='m-1'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Returns Rolling (Default 30D)',className='mt-4'),
                                dcc.Graph(
                                    id='graph-3a',
                                    figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 m-4',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Volatility Rolling (Default 30D)',className='mt-4'),
                                dcc.Graph(
                                    id='graph-4a',
                                    figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 m-4',
                        ),
                    ],
                    # className='m-1'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Max Drawdowns',className='mt-4'),
                                dcc.Graph(
                                    id='graph-5a',
                                    figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 m-4',
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Correlations Rolling (Default 30D) - Select Coins to Activate',className='mt-4'),
                                dcc.Graph(
                                    id='graph-6a',
                                    figure = blank_fig(),
                                    style={'scroll-margin-top':'248px'},
                                    config={'displayModeBar': False}
                                ),
                            ],
                            className='border border-light rounded-3 m-4',
                        ),
                    ],
                    # className='m-1'
                ),
            ],
            # className='border d-flex flex-column justify-content-end flex-fill'
            className='flex-fill col-xl-10',
            # width=10,
        ),
    ],
    fluid=True,
    className=' dbc d-flex',
)


###############################################################################
# CALLBACKS - PLOTS
###############################################################################
@callback(
    Output("graph-1a", "figure"),
    Output("graph-2a", "figure"),
    Output("graph-3a", "figure"),
    Output("graph-4a", "figure"),
    Output("graph-5a", "figure"),
    Output("graph-6a", "figure"),
    Input('trailing','value'),
    Input('coins','value'),
    Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date'),
    # Input('checklist','value')
)
def graph(trailing, coin_list, start_date, end_date):
    # if not {'price'} <= coin_list[coin].columns:
    #
    return (
        fig_plot.plot_price(trailing, coin_list, start_date, end_date),
        fig_plot.plot_logprice(trailing, coin_list, start_date, end_date),
        fig_plot.plot_returns(trailing, coin_list, start_date, end_date),
        fig_plot.plot_volatility(trailing, coin_list, start_date, end_date),
        fig_plot.plot_drawdown(trailing, coin_list, start_date, end_date),
        fig_plot.plot_rollingcorr(trailing, coin_list, start_date, end_date),
    )
